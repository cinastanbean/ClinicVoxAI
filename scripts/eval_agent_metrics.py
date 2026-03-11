from __future__ import annotations

import json
from pathlib import Path

from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()

    scenarios = {
        "schedule": [
            "I want to schedule an appointment",
            "My first name is Jane",
            "My last name is Doe",
            "My date of birth is 1990-01-01",
            "Wednesday morning works",
        ],
        "report_unverified": [
            "I want my lab results",
        ],
        "verification_failure": [
            "I want my lab results",
            "My date of birth is 1970-01-01",
            "My date of birth is 1970-01-01",
        ],
        "intent_switch": [
            "I want to schedule an appointment",
            "My first name is Jane",
            "Actually I want my lab results",
            "My date of birth is 1990-01-01",
        ],
    }

    results = []
    for name, transcript in scenarios.items():
        state = orch.new_state(session_id=f"METRIC-{name}", caller_phone="+15550000000")
        turn_count = 0
        for text in transcript:
            orch.handle_turn(state, text)
            turn_count += 1
        results.append(
            {
                "scenario": name,
                "turns": turn_count,
                "handoff_reason": state.handoff_reason,
                "intent": state.intent,
                "verification_status": state.verification_status,
            }
        )

    completed = sum(1 for r in results if not r["handoff_reason"])
    handoff = sum(1 for r in results if r["handoff_reason"])
    avg_turns = sum(r["turns"] for r in results) / len(results)

    report = {
        "total": len(results),
        "completed": completed,
        "handoff": handoff,
        "avg_turns": avg_turns,
        "results": results,
    }

    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "agent_metrics.json"
    out_file.write_text(json.dumps(report, indent=2))
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    run()
