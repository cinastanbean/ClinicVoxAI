from __future__ import annotations

import json
from pathlib import Path


def run() -> None:
    trace_path = Path("outputs/trace.json")
    if not trace_path.exists():
        print("No trace file found. Run scripts/export_events.py first.")
        return

    data = json.loads(trace_path.read_text())
    snapshots = data.get("snapshots", [])

    for i in range(1, len(snapshots)):
        prev = snapshots[i - 1]
        curr = snapshots[i]
        print(f"--- Snapshot {i} ---")
        for key, value in curr.items():
            if prev.get(key) != value:
                print(f"{key}: {prev.get(key)} -> {value}")


if __name__ == "__main__":
    run()
