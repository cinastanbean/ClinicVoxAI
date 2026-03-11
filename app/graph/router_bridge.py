from __future__ import annotations

from typing import Dict, Protocol

from app.rules import INTENT_KEYWORDS, PATIENT_TYPE_KEYWORDS


class RouterBackend(Protocol):
    def classify(self, text: str) -> Dict:
        ...


class RuleBasedRouter:
    def classify(self, text: str) -> Dict:
        t = text.lower()
        intent = "other"
        for key, keywords in INTENT_KEYWORDS.items():
            if any(k in t for k in keywords):
                intent = key
                break

        patient_type = "unknown"
        for key, keywords in PATIENT_TYPE_KEYWORDS.items():
            if any(k in t for k in keywords):
                patient_type = key
                break

        confidence = 0.75 if intent != "other" else 0.4
        return {"patient_type": patient_type, "intent": intent, "confidence": confidence}


class LLMRouter:
    def __init__(self, client: object) -> None:
        self.client = client

    def classify(self, text: str) -> Dict:
        if hasattr(self.client, "classify"):
            return self.client.classify(text)
        return self.client.classify_intent(text)
