from __future__ import annotations

from dataclasses import asdict

from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()

    scenarios = {
        "registration_schedule": [
            "I want to schedule an appointment",
            "My first name is Jane",
            "My last name is Doe",
            "My date of birth is 1990-01-01",
            "Wednesday morning works",
        ],
        "report_verified": [
            "I want my lab results",
            "My date of birth is 1990-01-01",
        ],
        "intent_switch": [
            "I want to schedule an appointment",
            "My first name is Jane",
            "Actually I want my lab results",
            "My date of birth is 1990-01-01",
        ],
        "verification_failure": [
            "I want my lab results",
            "My date of birth is 1970-01-01",
            "My date of birth is 1970-01-01",
        ],
    }

    for name, transcript in scenarios.items():
        print("=" * 80)
        print("Scenario:", name)
        state = orch.new_state(session_id=f"FULL-{name}", caller_phone="+15550000000")
        for text in transcript:
            result = orch.handle_turn(state, text)
            print("Caller:", text)
            print("Assistant:", result["response"])
            print("State:", asdict(result["state"]))
            print("-" * 60)


if __name__ == "__main__":
    run()
