from __future__ import annotations

from app.graph.orchestrator import Orchestrator


def test_intent_switch_resets_context() -> None:
    orch = Orchestrator()
    state = orch.new_state("S3")

    orch.handle_turn(state, "I want to schedule an appointment")
    orch.handle_turn(state, "My first name is Jane")

    prev_appt = state.appointment_context

    orch.handle_turn(state, "Actually I want my lab results")

    assert state.intent == "report"
    assert state.appointment_context != prev_appt
