from __future__ import annotations

from typing import Tuple

from app.config import CONFIG
from app.graph.router_bridge import LLMRouter, RuleBasedRouter
from app.llm.mock import MockLLM
from app.llm.openai_client import OpenAIIntentClassifier
from app.graph.state import SessionState, reset_context_on_intent_change


class RouterAgent:
    name = "router"

    def __init__(self) -> None:
        if CONFIG.router_backend == "openai":
            self.backend = LLMRouter(client=OpenAIIntentClassifier())
        elif CONFIG.router_backend == "llm":
            self.backend = LLMRouter(client=MockLLM())
        else:
            self.backend = RuleBasedRouter()

    def classify(self, text: str) -> Tuple[str, str, float]:
        result = self.backend.classify(text)
        return result["patient_type"], result["intent"], result["confidence"]

    def handle(self, state: SessionState, text: str) -> SessionState:
        patient_type, intent, confidence = self.classify(text)

        # Intent carry-forward for follow-up slots/fields
        if intent == "other" and state.intent in {"schedule", "report", "reschedule", "cancel"}:
            intent = state.intent
            confidence = max(confidence, 0.6)

        reset_context_on_intent_change(state, intent)
        state.patient_type = patient_type
        state.intent = intent
        state.intent_confidence = confidence
        state.last_agent = self.name
        return state
