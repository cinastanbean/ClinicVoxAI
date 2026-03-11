from __future__ import annotations

import json
import os
from typing import Dict

from openai import OpenAI


class OpenAIIntentClassifier:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    def classify(self, text: str) -> Dict:
        system = (
            "Classify patient_type and intent. Return JSON with keys: "
            "patient_type, intent, confidence."
        )
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": text},
            ],
        )
        content = response.output_text.strip()
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"patient_type": "unknown", "intent": "other", "confidence": 0.0}


class OpenAIReportSummarizer:
    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    def summarize(self, report_text: str) -> str:
        system = (
            "Summarize the report in plain language. Do not add any diagnosis. "
            "Only restate what is written."
        )
        response = self.client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": system},
                {"role": "user", "content": report_text},
            ],
        )
        return response.output_text.strip()
