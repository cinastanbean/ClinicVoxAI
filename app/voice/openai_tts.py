from __future__ import annotations

import os

from openai import OpenAI


class OpenAITTSClient:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    def synthesize_to_file(self, text: str, output_path: str) -> str:
        audio = self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="alloy",
            input=text,
        )
        audio.stream_to_file(output_path)
        return output_path
