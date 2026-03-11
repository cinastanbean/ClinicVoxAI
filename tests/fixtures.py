from __future__ import annotations

from app.graph.orchestrator import Orchestrator


def make_orchestrator() -> Orchestrator:
    return Orchestrator()


def make_state(session_id: str = "T-1"):
    orch = Orchestrator()
    return orch, orch.new_state(session_id)
