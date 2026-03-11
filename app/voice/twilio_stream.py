from __future__ import annotations

import asyncio
import audioop
import base64
import json
import time
import wave
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import WebSocket

from app.voice.audio_filters import apply_soft_gate
from app.voice.openai_realtime import OpenAIRealtimeClient


class TwilioStreamBridge:
    def __init__(
        self,
        websocket: WebSocket,
        max_queue: int = 100,
        idle_flush_s: float = 0.6,
        max_utterance_s: float = 12.0,
        segment_seconds: float = 30.0,
    ) -> None:
        self.websocket = websocket
        self.realtime: OpenAIRealtimeClient | None = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.queue: asyncio.Queue[str] = asyncio.Queue(maxsize=max_queue)
        self.idle_flush_s = idle_flush_s
        self.last_media_time = time.time()
        self._idle_task: Optional[asyncio.Task] = None
        self.stream_sid: Optional[str] = None
        self.utterance_start = time.time()
        self.max_utterance_s = max_utterance_s
        self.output_ulaw = bytearray()
        self.avg_gap = idle_flush_s
        self.first_audio_time: Optional[float] = None
        self.segment_seconds = segment_seconds

    async def _sender(self) -> None:
        while True:
            msg = await self.queue.get()
            if msg == "__close__":
                break
            await self.websocket.send_text(msg)

    def _queue_send(self, payload: dict) -> None:
        if not self.loop:
            return
        try:
            self.queue.put_nowait(json.dumps(payload))
        except asyncio.QueueFull:
            # Drop oldest to reduce latency and clear Twilio buffer
            try:
                _ = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            if self.stream_sid:
                clear_msg = {"event": "clear", "streamSid": self.stream_sid}
                self.queue.put_nowait(json.dumps(clear_msg))
            self.queue.put_nowait(json.dumps(payload))

    async def _idle_flush(self) -> None:
        while True:
            await asyncio.sleep(self.idle_flush_s)
            if time.time() - self.last_media_time >= self.idle_flush_s:
                if self.realtime:
                    self.realtime.send_event({"type": "input_audio_buffer.commit"})
                    self.realtime.send_event({"type": "response.create"})

    def _write_output_wav(self) -> None:
        if not self.output_ulaw:
            return
        out_dir = Path("outputs")
        out_dir.mkdir(parents=True, exist_ok=True)
        sid = self.stream_sid or f"twilio_{int(time.time())}"
        pcm = audioop.ulaw2lin(bytes(self.output_ulaw), 2)
        samples_per_segment = int(self.segment_seconds * 8000)
        segments = []
        total_samples = len(self.output_ulaw)
        segment_index = 0
        start_time = self.first_audio_time or time.time()

        for offset in range(0, total_samples, samples_per_segment):
            seg_ulaw = self.output_ulaw[offset : offset + samples_per_segment]
            seg_pcm = audioop.ulaw2lin(bytes(seg_ulaw), 2)
            seg_start_s = offset / 8000.0
            seg_end_s = seg_start_s + (len(seg_ulaw) / 8000.0)
            ts = datetime.fromtimestamp(start_time + seg_start_s, tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            wav_path = out_dir / f"twilio_out_{sid}_{segment_index:03d}_{ts}.wav"

            with wave.open(str(wav_path), "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(8000)
                wf.writeframes(seg_pcm)

            segments.append(
                {
                    "index": segment_index,
                    "file": str(wav_path),
                    "start_offset_s": round(seg_start_s, 3),
                    "end_offset_s": round(seg_end_s, 3),
                    "start_time_utc": ts,
                }
            )
            segment_index += 1

        meta_path = out_dir / f"twilio_out_{sid}_segments.json"
        meta = {
            "stream_sid": sid,
            "total_duration_s": round(total_samples / 8000.0, 3),
            "segment_seconds": self.segment_seconds,
            "segments": segments,
        }
        meta_path.write_text(json.dumps(meta, indent=2))

    def _update_adaptive_vad(self, gap: float) -> None:
        # Exponential moving average for silence gap
        self.avg_gap = 0.9 * self.avg_gap + 0.1 * gap
        # Dynamic idle flush window: 2x avg gap clamped
        self.idle_flush_s = max(0.3, min(1.2, self.avg_gap * 2.0))

    async def handle(self) -> None:
        await self.websocket.accept()
        self.loop = asyncio.get_event_loop()
        sender_task = asyncio.create_task(self._sender())
        self._idle_task = asyncio.create_task(self._idle_flush())

        def on_openai_event(event: dict) -> None:
            event_type = event.get("type", "")
            audio_delta = event.get("delta") or event.get("audio") or event.get("output_audio")
            if "response.output_audio.delta" in event_type or "response.audio.delta" in event_type:
                if audio_delta and self.stream_sid:
                    try:
                        self.output_ulaw.extend(base64.b64decode(audio_delta))
                    except Exception:
                        pass
                    payload = {
                        "event": "media",
                        "streamSid": self.stream_sid,
                        "media": {"payload": audio_delta},
                    }
                    self.loop.call_soon_threadsafe(self._queue_send, payload)  # type: ignore

        self.realtime = OpenAIRealtimeClient(on_event=on_openai_event)
        self.realtime.connect(instructions="You are a clinic assistant.")

        while True:
            msg = await self.websocket.receive_text()
            data = json.loads(msg)
            event = data.get("event")
            if event == "start":
                self.stream_sid = data.get("start", {}).get("streamSid")
                self.utterance_start = time.time()
            if event == "media":
                payload = data.get("media", {}).get("payload")
                if payload and self.realtime:
                    # Soft gate drop for low-energy frames
                    gated = apply_soft_gate(payload)
                    if gated is None:
                        continue

                    now = time.time()
                    if self.first_audio_time is None:
                        self.first_audio_time = now
                    gap = now - self.last_media_time
                    self.last_media_time = now
                    self._update_adaptive_vad(gap)

                    # Length limit
                    if (time.time() - self.utterance_start) > self.max_utterance_s:
                        self.realtime.send_event({"type": "input_audio_buffer.commit"})
                        self.realtime.send_event({"type": "response.create"})
                        self.utterance_start = time.time()

                    self.realtime.send_event(
                        {"type": "input_audio_buffer.append", "audio": gated}
                    )
            elif event == "stop":
                if self.realtime:
                    self.realtime.send_event({"type": "input_audio_buffer.commit"})
                    self.realtime.send_event({"type": "response.create"})
                break

        if self.realtime:
            self.realtime.close()
        if self._idle_task:
            self._idle_task.cancel()
        await self.queue.put("__close__")
        await sender_task
        self._write_output_wav()
        await self.websocket.close()
