from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from app.graph.orchestrator import Orchestrator


def load_scenarios(path: Path) -> tuple[dict[str, list[str]], dict[str, dict[str, str]]]:
    scenarios: dict[str, list[str]] = {}
    expectations: dict[str, dict[str, str]] = {}
    with path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = (row.get("scenario") or "").strip()
            utterance = (row.get("utterance") or "").strip()
            if not name or not utterance:
                continue
            scenarios.setdefault(name, []).append(utterance)

            expected_intent = (row.get("expected_intent") or "").strip()
            expected_handoff = (row.get("expected_handoff") or "").strip()
            if name not in expectations:
                expectations[name] = {}
            if expected_intent:
                expectations[name]["expected_intent"] = expected_intent
            if expected_handoff:
                expectations[name]["expected_handoff"] = expected_handoff
    return scenarios, expectations


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="data/scenarios.csv")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"Missing {csv_path}")
        return

    scenarios, expectations = load_scenarios(csv_path)
    orch = Orchestrator()

    results = []
    for name, transcript in scenarios.items():
        state = orch.new_state(session_id=f"CSV-{name}", caller_phone="+15550000000")
        turn_count = 0
        for text in transcript:
            orch.handle_turn(state, text)
            turn_count += 1

        expected_intent = expectations.get(name, {}).get("expected_intent")
        expected_handoff = expectations.get(name, {}).get("expected_handoff")

        intent_ok = expected_intent is None or expected_intent == "" or expected_intent == state.intent
        handoff_ok = (
            expected_handoff is None
            or expected_handoff == ""
            or expected_handoff == (state.handoff_reason or "none")
        )

        results.append(
            {
                "scenario": name,
                "turns": turn_count,
                "handoff_reason": state.handoff_reason,
                "intent": state.intent,
                "verification_status": state.verification_status,
                "expected_intent": expected_intent,
                "expected_handoff": expected_handoff,
                "intent_ok": intent_ok,
                "handoff_ok": handoff_ok,
            }
        )

    completed = sum(1 for r in results if not r["handoff_reason"])
    handoff = sum(1 for r in results if r["handoff_reason"])
    avg_turns = sum(r["turns"] for r in results) / len(results) if results else 0
    intent_ok_count = sum(1 for r in results if r["intent_ok"])
    handoff_ok_count = sum(1 for r in results if r["handoff_ok"])

    report = {
        "total": len(results),
        "completed": completed,
        "handoff": handoff,
        "avg_turns": avg_turns,
        "intent_ok": intent_ok_count,
        "handoff_ok": handoff_ok_count,
        "results": results,
        "source": str(csv_path),
    }

    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "agent_metrics_csv.json"
    out_file.write_text(json.dumps(report, indent=2))
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    run()
