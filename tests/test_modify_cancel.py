from __future__ import annotations

from app.graph.orchestrator import Orchestrator


def test_cancel_flow_requires_appt_id() -> None:
    orch = Orchestrator()
    state = orch.new_state("C1", caller_phone="+15550000000")
    orch.handle_turn(state, "I want to cancel my appointment")
    response = orch.handle_turn(state, "My date of birth is 1990-01-01")["response"]
    assert "appointment id" in response.lower()


def test_report_flow_summary() -> None:
    orch = Orchestrator()
    state = orch.new_state("R1", caller_phone="+15550000000")
    orch.handle_turn(state, "I want to schedule an appointment")
    orch.handle_turn(state, "My first name is Jane")
    orch.handle_turn(state, "My last name is Doe")
    orch.handle_turn(state, "My date of birth is 1990-01-01")
    orch.handle_turn(state, "Wednesday morning works")
    response = orch.handle_turn(state, "I want my lab results")["response"]
    assert "summary" in response.lower()
