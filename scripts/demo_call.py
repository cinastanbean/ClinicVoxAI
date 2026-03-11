from __future__ import annotations

from dataclasses import asdict

from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()
    state = orch.new_state(session_id="DEMO-1", caller_phone="+15550000000")

    transcript = [
        "I want to schedule an appointment",
        "My first name is Jane",
        "My last name is Doe",
        "My date of birth is 1990-01-01",
        "Wednesday morning works",
        "Actually, can you tell me my lab results?",
    ]

    for text in transcript:
        result = orch.handle_turn(state, text)
        print("Caller:", text)
        print("Assistant:", result["response"])
        print("State snapshot:")
        print(asdict(result["state"]))
        print("-" * 60)


if __name__ == "__main__":
    run()
