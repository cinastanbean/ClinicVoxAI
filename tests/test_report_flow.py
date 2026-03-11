from __future__ import annotations

from app.graph.orchestrator import Orchestrator


def test_report_requires_verification() -> None:
    orch = Orchestrator()
    state = orch.new_state("S5", caller_phone="+15550000000")

    result = orch.handle_turn(state, "I want my lab results")
    assert "date of birth" in result["response"].lower()
