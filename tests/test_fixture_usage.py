from __future__ import annotations

from tests.fixtures import make_state


def test_fixture_creates_state() -> None:
    orch, state = make_state("FX-1")
    result = orch.handle_turn(state, "I want to schedule an appointment")
    assert result["state"].intent == "schedule"
