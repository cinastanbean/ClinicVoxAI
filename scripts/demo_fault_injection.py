from __future__ import annotations

from app.fault_injection import FAULTS
from app.graph.orchestrator import Orchestrator


def run() -> None:
    FAULTS.fail_db = True
    FAULTS.fail_calendar = True
    FAULTS.fail_notify = True

    orch = Orchestrator()
    state = orch.new_state("FAULT-1", caller_phone="+15550000000")

    transcript = [
        "I want to schedule an appointment",
        "My first name is Jane",
        "My last name is Doe",
        "My date of birth is 1990-01-01",
        "Wednesday morning works",
    ]

    for text in transcript:
        result = orch.handle_turn(state, text)
        print("Caller:", text)
        print("Assistant:", result["response"])
        print("Errors:", [e.code for e in result["state"].errors])
        print("-" * 60)


if __name__ == "__main__":
    run()
