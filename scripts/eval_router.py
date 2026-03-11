from __future__ import annotations

import csv
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

    with data_file.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            result = router.classify(row["text"])
            pred_intent = result[1]
            if pred_intent == row["intent"]:
                correct += 1

    accuracy = correct / total if total else 0
    print(f"Router accuracy: {accuracy:.2%} ({correct}/{total})")


if __name__ == "__main__":
    run()
