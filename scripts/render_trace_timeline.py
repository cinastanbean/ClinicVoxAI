from __future__ import annotations

import json
from pathlib import Path


HTML = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Trace Timeline</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { font-size: 20px; }
    .lane { margin: 10px 0; }
    .lane-title { font-weight: bold; margin-bottom: 6px; }
    .event { display: inline-block; margin: 4px; padding: 6px 8px; border-radius: 6px; background: #f2f2f2; font-size: 12px; }
    .router { background: #d7e6ff; }
    .supervisor { background: #ffe1c6; }
    .task { background: #d7f5d7; }
    .hook { background: #f6f0c1; }
    .diff { background: #e6f7ef; }
    .merge { background: #ffd8d8; }
    .langgraph { background: #cfe6ff; border: 2px solid #1e66ff; }
  </style>
</head>
<body>
  <h1>Trace Timeline</h1>
  __LANES__
</body>
</html>
"""


def classify(event_name: str) -> str:
    if event_name == "router":
        return "router"
    if event_name == "supervisor":
        return "supervisor"
    if event_name == "task_response":
        return "task"
    if event_name == "hook":
        return "hook"
    if event_name == "state_diff":
        return "diff"
    if event_name == "merge_conflict":
        return "merge"
    if event_name == "node_duration":
        return "langgraph"
    return ""


def run() -> None:
    trace_path = Path("outputs/trace.json")
    if not trace_path.exists():
        print("Missing outputs/trace.json. Run scripts/export_events.py first.")
        return

    data = json.loads(trace_path.read_text())
    events = data.get("events", [])

    lanes = {
        "Router": [],
        "Supervisor": [],
        "Task": [],
        "Hooks": [],
        "Diffs": [],
        "Conflicts": [],
        "LangGraph": [],
        "Other": [],
    }

    for event in events:
        name = event.get("event", "")
        cls = classify(name)
        label = name
        if name == "state_diff":
            label = f"diff:{event.get('agent')}"
        if name == "hook":
            label = f"hook:{event.get('event')}"
        if name == "merge_conflict":
            label = "merge_conflict"
        if name == "node_duration" and event.get("agent") == "langgraph":
            label = f"langgraph {event.get('ms')}ms"

        html = f"<span class=\"event {cls}\">{label}</span>"
        if name == "router":
            lanes["Router"].append(html)
        elif name == "supervisor":
            lanes["Supervisor"].append(html)
        elif name == "task_response":
            lanes["Task"].append(html)
        elif name == "hook":
            lanes["Hooks"].append(html)
        elif name == "state_diff":
            lanes["Diffs"].append(html)
        elif name == "merge_conflict":
            lanes["Conflicts"].append(html)
        elif name == "node_duration" and event.get("agent") == "langgraph":
            lanes["LangGraph"].append(html)
        else:
            lanes["Other"].append(html)

    lane_html = []
    for title, items in lanes.items():
        if not items:
            continue
        lane_html.append(
            f"<div class=\"lane\"><div class=\"lane-title\">{title}</div>{''.join(items)}</div>"
        )

    out = HTML.replace("__LANES__", "\n".join(lane_html))
    out_path = Path("outputs/trace_timeline.html")
    out_path.write_text(out)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    run()
