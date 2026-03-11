from __future__ import annotations

import json
from pathlib import Path


def run() -> None:
    trace_path = Path("outputs/trace.json")
    if not trace_path.exists():
        print("Missing outputs/trace.json. Run scripts/export_events.py first.")
        return

    data = json.loads(trace_path.read_text())
    events = data.get("events", [])

    turns = {}
    current_turn = 0

    for event in events:
        name = event.get("event")
        if name == "turn_start":
            current_turn = event.get("turn_id")
            turns[current_turn] = {
                "intent": None,
                "agents": {},
                "response": None,
            }
        elif name == "router":
            if current_turn in turns:
                turns[current_turn]["intent"] = event.get("intent")
        elif name == "state_diff":
            agent = event.get("agent")
            diff = event.get("diff")
            turns[current_turn]["agents"].setdefault(agent, {})
            turns[current_turn]["agents"][agent]["writes"] = list(diff.keys())
        elif name == "node_duration":
            agent = event.get("agent")
            ms = event.get("ms")
            turns[current_turn]["agents"].setdefault(agent, {})
            turns[current_turn]["agents"][agent]["ms"] = ms
        elif name == "task_response":
            turns[current_turn]["response"] = event.get("response")

    out_lines = []
    out_lines.append("turn, intent, agent, writes, ms, response")
    for turn_id, info in turns.items():
        intent = info.get("intent")
        response = info.get("response")
        agents = info.get("agents")
        for agent, meta in agents.items():
            writes = ",".join(meta.get("writes", []))
            ms = meta.get("ms")
            out_lines.append(f"{turn_id}, {intent}, {agent}, {writes}, {ms}, {response}")

    out_path = Path("outputs/collab_summary.csv")
    out_path.write_text("\n".join(out_lines))
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    run()
