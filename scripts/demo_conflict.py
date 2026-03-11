from __future__ import annotations

from app.config import CONFIG
from app.graph.orchestrator import Orchestrator


def run() -> None:
    CONFIG.enable_parallel_demo = True
    orch = Orchestrator()
    state = orch.new_state(session_id="CONFLICT-1")

    transcript = [
        "I want to schedule an appointment",
    ]

    for text in transcript:
        result = orch.handle_turn(state, text)
        print("Caller:", text)
        print("Assistant:", result["response"])
        print("Merge conflicts:", result["state"].meta.get("merge_conflicts"))
        print("Meta:", result["state"].meta)
        print("-" * 60)


if __name__ == "__main__":
    run()
