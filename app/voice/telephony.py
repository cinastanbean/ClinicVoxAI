from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List


@dataclass
class CallEvent:
    session_id: str
    caller_phone: str
    audio_chunks: List[str]


class TelephonyGateway:
    def __init__(self, on_audio: Callable[[CallEvent], None]) -> None:
        self.on_audio = on_audio

    def simulate_call(self, session_id: str, caller_phone: str, audio_chunks: List[str]) -> None:
        event = CallEvent(session_id=session_id, caller_phone=caller_phone, audio_chunks=audio_chunks)
        self.on_audio(event)
