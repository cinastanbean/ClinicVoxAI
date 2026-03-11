from __future__ import annotations

import json
from pathlib import Path

from app.graph.orchestrator import Orchestrator


def run() -> None:
    orch = Orchestrator()
    transcript = [
        "I want to schedule an appointment",
        "My first name is Jane",
        "My last name is Doe",
        "My date of birth is 1990-01-01",
        "Wednesday morning works",
        "Actually, can you tell me my lab results?",
    ]
    result = orch.simulate_call(transcript, session_id="EXPORT-1")

    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "trace.json"
    out_file.write_text(json.dumps(result["trace"], indent=2))
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    run()
