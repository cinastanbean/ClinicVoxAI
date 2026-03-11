from __future__ import annotations

from typing import Dict, List

from app.graph.langgraph_runtime import LangGraphRuntime
from app.graph.state import SessionState


class Orchestrator:
    """LangGraph-backed orchestrator (replaces legacy engine)."""

    def __init__(self) -> None:
        self.runtime = LangGraphRuntime()

    def handle_turn(self, state: SessionState, text: str) -> Dict:
        return self.runtime.handle_turn(state, text)

    def new_state(self, session_id: str, caller_phone: str | None = None) -> SessionState:
        return self.runtime.new_state(session_id, caller_phone)

    def simulate_call(self, transcript: List[str], session_id: str, caller_phone: str | None = None) -> Dict:
        return self.runtime.simulate_call(transcript, session_id, caller_phone)
