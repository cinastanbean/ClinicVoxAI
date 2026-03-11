from __future__ import annotations

from app.compliance.audit import AuditLogger
from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()
    audit = AuditLogger()

    transcript = [
        "I want to schedule an appointment",
        "My first name is Jane",
        "My last name is Doe",
        "My date of birth is 1990-01-01",
        "Wednesday morning works",
        "Actually I want my lab results",
        "My date of birth is 1990-01-01",
    ]

    state = orch.new_state("E2E-1", caller_phone="+15550000000")
    for text in transcript:
        result = orch.handle_turn(state, text)
        audit.write("turn", {"text": text, "response": result["response"]})
        print("Assistant:", result["response"])


if __name__ == "__main__":
    run()
