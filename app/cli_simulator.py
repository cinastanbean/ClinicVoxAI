from __future__ import annotations

import json
from dataclasses import asdict

from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()
    session_id = "CLI-1"
    print("Enter blank line to stop.")
    state = orch.new_state(session_id)
    while True:
        text = input("Caller: ").strip()
        if not text:
            break
        result = orch.handle_turn(state, text)
        state = result["state"]
        print("Assistant:", result["response"])
    print(json.dumps(asdict(state), indent=2, default=str))


if __name__ == "__main__":
    run()
