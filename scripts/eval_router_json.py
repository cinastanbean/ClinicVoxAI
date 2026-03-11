from __future__ import annotations

import csv
import json
from pathlib import Path

from app.agents.router import RouterAgent


def run() -> None:
    data_file = Path("data/router_eval.csv")
    if not data_file.exists():
        print("Missing data/router_eval.csv")
        return

    router = RouterAgent()
    total = 0
    correct = 0
    details = []

    with data_file.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            result = router.classify(row["text"])
            pred_intent = result[1]
            ok = pred_intent == row["intent"]
            if ok:
                correct += 1
            details.append({
                "text": row["text"],
                "gold": row["intent"],
                "pred": pred_intent,
                "correct": ok,
            })

    accuracy = correct / total if total else 0
    report = {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "details": details,
    }

    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "router_eval.json"
    out_file.write_text(json.dumps(report, indent=2))
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    run()
