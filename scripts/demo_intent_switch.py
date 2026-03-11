from __future__ import annotations

from dataclasses import asdict

from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()
    state = orch.new_state(session_id="SWITCH-1")

    transcript = [
        "I want to schedule an appointment",
        "My first name is Jane",
        "My last name is Doe",
        "Actually I want my lab results",
    ]

    for text in transcript:
        result = orch.handle_turn(state, text)
        print("Caller:", text)
        print("Assistant:", result["response"])
        print("Intent:", result["state"].intent)
        print("Appointment context:", asdict(result["state"].appointment_context))
        print("Report context:", asdict(result["state"].report_context))
        print("-" * 60)


if __name__ == "__main__":
    run()
