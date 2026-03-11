from __future__ import annotations

import json
import os
import threading
from typing import Callable, Optional

import websocket


class OpenAIRealtimeClient:
    def __init__(
        self,
        on_event: Optional[Callable[[dict], None]] = None,
        model: str = "gpt-realtime",
        input_audio_format: str = "g711_ulaw",
        output_audio_format: str = "g711_ulaw",
        voice: str = "alloy",
        enable_server_vad: bool = True,
    ) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.url = f"wss://api.openai.com/v1/realtime?model={model}"
        self.headers = ["Authorization: Bearer " + api_key]
        self.on_event = on_event
        self.ws: websocket.WebSocketApp | None = None
        self._thread: threading.Thread | None = None
        self.input_audio_format = input_audio_format
        self.output_audio_format = output_audio_format
        self.voice = voice
        self.enable_server_vad = enable_server_vad

    def connect(self, instructions: str | None = None) -> None:
        def on_open(ws):
            session = {
                "type": "realtime",
                "input_audio_format": self.input_audio_format,
                "output_audio_format": self.output_audio_format,
                "voice": self.voice,
            }
            if self.enable_server_vad:
                session["turn_detection"] = {"type": "server_vad", "create_response": True}
            if instructions:
                session["instructions"] = instructions
            ws.send(json.dumps({"type": "session.update", "session": session}))

        def on_message(ws, message):
            try:
                data = json.loads(message)
            except json.JSONDecodeError:
                return
            if self.on_event:
                self.on_event(data)

        self.ws = websocket.WebSocketApp(
            self.url,
            header=self.headers,
            on_open=on_open,
            on_message=on_message,
        )
        self._thread = threading.Thread(target=self.ws.run_forever, daemon=True)
        self._thread.start()

    def send_event(self, event: dict) -> None:
        if self.ws:
            self.ws.send(json.dumps(event))

    def close(self) -> None:
        if self.ws:
            self.ws.close()
            self.ws = None
