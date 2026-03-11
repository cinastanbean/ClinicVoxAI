from __future__ import annotations

from app.graph.orchestrator import Orchestrator


def test_verification_failure_triggers_handoff() -> None:
    orch = Orchestrator()
    state = orch.new_state("S4", caller_phone="+15550000000")

    orch.handle_turn(state, "I want my lab results")
    orch.handle_turn(state, "My date of birth is 1970-01-01")
    orch.handle_turn(state, "My date of birth is 1970-01-01")

    assert state.handoff_reason == "verification_failed"
