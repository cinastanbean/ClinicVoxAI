from __future__ import annotations

import os

from openai import OpenAI


class OpenAISTTClient:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    def transcribe_file(self, audio_path: str) -> str:
        with open(audio_path, "rb") as f:
            transcript = self.client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=f,
            )
        return transcript.text
