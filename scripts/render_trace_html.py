from __future__ import annotations

import json
from pathlib import Path


HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Agent Trace</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { font-size: 20px; }
    pre { background: #f6f6f6; padding: 10px; white-space: pre-wrap; }
    table { border-collapse: collapse; width: 100%; margin-top: 10px; }
    th, td { border: 1px solid #ddd; padding: 6px; font-size: 12px; vertical-align: top; }
    th { background: #f0f0f0; }
    .event-turn { background: #eef; }
    .event-diff { background: #efe; }
    .event-merge { background: #fee; }
    .event-hook { background: #f9f4d0; }
    .tag { display: inline-block; padding: 2px 6px; border-radius: 4px; font-size: 11px; }
    .tag-turn { background: #cbd8ff; }
    .tag-diff { background: #cbeed3; }
    .tag-merge { background: #f4c6c6; }
    .tag-hook { background: #f0e2a6; }
  </style>
</head>
<body>
  <h1>Trace Events</h1>
  <table>
    <thead>
      <tr><th>#</th><th>Event</th><th>Payload</th></tr>
    </thead>
    <tbody>
      __ROWS__
    </tbody>
  </table>

  <h1>State Snapshots</h1>
  <pre>__SNAPSHOTS__</pre>
</body>
</html>
"""


def classify_event(event_name: str) -> str:
    if event_name.startswith("turn"):
        return "event-turn"
    if event_name in {"state_diff"}:
        return "event-diff"
    if event_name in {"merge_conflict"}:
        return "event-merge"
    if event_name == "hook":
        return "event-hook"
    return ""


def tag_for_event(event_name: str) -> str:
    if event_name.startswith("turn"):
        return "<span class=\"tag tag-turn\">turn</span>"
    if event_name in {"state_diff"}:
        return "<span class=\"tag tag-diff\">diff</span>"
    if event_name in {"merge_conflict"}:
        return "<span class=\"tag tag-merge\">merge</span>"
    if event_name == "hook":
        return "<span class=\"tag tag-hook\">hook</span>"
    return ""


def run() -> None:
    trace_path = Path("outputs/trace.json")
    if not trace_path.exists():
        print("Missing outputs/trace.json. Run scripts/export_events.py first.")
        return

    data = json.loads(trace_path.read_text())
    events = data.get("events", [])
    snapshots = data.get("snapshots", [])

    rows = []
    for i, event in enumerate(events, start=1):
        name = event.get("event", "")
        payload = {k: v for k, v in event.items() if k != "event"}
        cls = classify_event(name)
        tag = tag_for_event(name)
        rows.append(
            f"<tr class=\"{cls}\"><td>{i}</td><td>{name} {tag}</td><td><pre>{json.dumps(payload, indent=2)}</pre></td></tr>"
        )

    html = HTML_TEMPLATE.replace("__ROWS__", "\n".join(rows)).replace(
        "__SNAPSHOTS__", json.dumps(snapshots, indent=2)
    )
    out_path = Path("outputs/trace.html")
    out_path.write_text(html)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    run()
