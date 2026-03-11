from __future__ import annotations

from app.graph.state import SessionState


class ContextAgent:
    name = "context"

    def handle(self, state: SessionState, text: str):
        _ = text
        summary = {
            "intent": state.intent,
            "patient_type": state.patient_type,
            "verified": state.verification_status == "verified",
        }
        state.meta["context_summary"] = summary
        state.last_agent = self.name
        return state
