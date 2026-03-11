from __future__ import annotations

from typing import Dict


class MockLLM:
    def classify_intent(self, text: str) -> Dict:
        t = text.lower()
        if "schedule" in t or "appointment" in t:
            return {"patient_type": "unknown", "intent": "schedule", "confidence": 0.8}
        if "report" in t or "results" in t:
            return {"patient_type": "unknown", "intent": "report", "confidence": 0.8}
        if "cancel" in t:
            return {"patient_type": "unknown", "intent": "cancel", "confidence": 0.8}
        return {"patient_type": "unknown", "intent": "other", "confidence": 0.4}

    def summarize_report(self, report_text: str) -> str:
        return f"Summary: {report_text}"

    def draft_response(self, intent: str, state_summary: Dict) -> str:
        if intent == "schedule":
            return "Let me help schedule your appointment."
        if intent == "report":
            return "I can summarize your report once you are verified."
        return "How can I assist you today?"
