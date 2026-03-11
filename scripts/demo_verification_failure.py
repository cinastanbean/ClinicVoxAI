from __future__ import annotations

from dataclasses import asdict

from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()
    state = orch.new_state(session_id="VERIFY-FAIL", caller_phone="+15550000000")

    transcript = [
        "I want my lab results",
        "My date of birth is 1970-01-01",
        "My date of birth is 1970-01-01",
    ]

    for text in transcript:
        result = orch.handle_turn(state, text)
        print("Caller:", text)
        print("Assistant:", result["response"])
        print("Verification attempts:", result["state"].verification_attempts)
        print("Handoff reason:", result["state"].handoff_reason)
        print(asdict(result["state"]))
        print("-" * 60)


if __name__ == "__main__":
    run()
