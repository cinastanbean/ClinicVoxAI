from __future__ import annotations

from dataclasses import dataclass

from app.graph.state import SessionState
from app.config import CONFIG


@dataclass
class SupervisorPolicy:
    low_confidence_threshold: float = 0.5
    max_errors_before_handoff: int = 2


class SupervisorAgent:
    name = "supervisor"

    def __init__(self, policy: SupervisorPolicy | None = None) -> None:
        self.policy = policy or SupervisorPolicy(
            low_confidence_threshold=CONFIG.supervisor_low_confidence_threshold,
            max_errors_before_handoff=CONFIG.supervisor_max_errors,
        )

    def decide(self, state: SessionState) -> str:
        if state.intent_confidence < self.policy.low_confidence_threshold:
            return "clarify"
        if len(state.errors) >= self.policy.max_errors_before_handoff:
            state.handoff_reason = "tool_errors"
            return "handoff"
        if state.handoff_reason:
            return "handoff"
        return "proceed"

    def handle(self, state: SessionState) -> SessionState:
        state.last_agent = self.name
        return state
