from __future__ import annotations

import asyncio
import base64
import time
from typing import Optional

from fastapi import WebSocket

from app.voice.openai_realtime import OpenAIRealtimeClient


class RetellStreamBridge:
    def __init__(self, websocket: WebSocket, max_queue: int = 100, idle_flush_s: float = 0.6) -> None:
        self.websocket = websocket
        self.realtime: OpenAIRealtimeClient | None = None
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self.queue: asyncio.Queue[bytes] = asyncio.Queue(maxsize=max_queue)
        self.idle_flush_s = idle_flush_s
        self.last_media_time = time.time()
        self._idle_task: Optional[asyncio.Task] = None
        self.avg_gap = idle_flush_s

    async def _sender(self) -> None:
        while True:
            data = await self.queue.get()
            if data == b"__close__":
                break
            await self.websocket.send_bytes(data)

    def _queue_send(self, payload: bytes) -> None:
        if not self.loop:
            return
        try:
            self.queue.put_nowait(payload)
        except asyncio.QueueFull:
            try:
                _ = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
            self.queue.put_nowait(payload)

    def _update_adaptive_vad(self, gap: float) -> None:
        self.avg_gap = 0.9 * self.avg_gap + 0.1 * gap
        self.idle_flush_s = max(0.3, min(1.2, self.avg_gap * 2.0))

    async def _idle_flush(self) -> None:
        while True:
            await asyncio.sleep(self.idle_flush_s)
            if time.time() - self.last_media_time >= self.idle_flush_s:
                if self.realtime:
                    self.realtime.send_event({"type": "input_audio_buffer.commit"})
                    self.realtime.send_event({"type": "response.create"})

    async def handle(self) -> None:
        await self.websocket.accept()
        self.loop = asyncio.get_event_loop()
        sender_task = asyncio.create_task(self._sender())
        self._idle_task = asyncio.create_task(self._idle_flush())

        def on_openai_event(event: dict) -> None:
            event_type = event.get("type", "")
            audio_delta = event.get("delta") or event.get("audio") or event.get("output_audio")
            if "response.output_audio.delta" in event_type or "response.audio.delta" in event_type:
                if audio_delta:
                    try:
                        audio_bytes = base64.b64decode(audio_delta)
                        self.loop.call_soon_threadsafe(self._queue_send, audio_bytes)  # type: ignore
                    except Exception:
                        pass

        self.realtime = OpenAIRealtimeClient(on_event=on_openai_event)
        self.realtime.connect(instructions="You are a clinic assistant.")

        while True:
            data = await self.websocket.receive_bytes()
            if not data:
                break
            now = time.time()
            gap = now - self.last_media_time
            self.last_media_time = now
            self._update_adaptive_vad(gap)
            if self.realtime:
                self.realtime.send_event(
                    {"type": "input_audio_buffer.append", "audio": base64.b64encode(data).decode("utf-8")}
                )

        if self.realtime:
            self.realtime.send_event({"type": "input_audio_buffer.commit"})
            self.realtime.send_event({"type": "response.create"})
            self.realtime.close()
        if self._idle_task:
            self._idle_task.cancel()
        await self.queue.put(b"__close__")
        await sender_task
        await self.websocket.close()
