from __future__ import annotations

from app.graph.orchestrator import Orchestrator


def test_intent_clarify_when_low_confidence() -> None:
    orch = Orchestrator()
    result = orch.simulate_call(["hello"], session_id="S1")
    assert "schedule" in result["responses"][0].lower() or "report" in result["responses"][0].lower()


def test_schedule_flow_minimum() -> None:
    orch = Orchestrator()
    transcript = [
        "I want to schedule an appointment",
        "My first name is Jane",
        "My last name is Doe",
        "My date of birth is 1990-01-01",
        "Wednesday morning works",
    ]
    result = orch.simulate_call(transcript, session_id="S2")
    assert result["responses"][-1].lower().startswith("you're all set")
