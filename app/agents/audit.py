from __future__ import annotations

from app.graph.state import SessionState


class AuditAgent:
    name = "audit"

    def handle(self, state: SessionState, text: str):
        _ = text
        state.meta["audit_note"] = "audit_branch"
        state.last_agent = self.name
        return state
