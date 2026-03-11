from __future__ import annotations

import json
from pathlib import Path


HTML = """
<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>Trace Swimlane</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { font-size: 20px; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 6px; vertical-align: top; }
    th { background: #f4f4f4; text-align: left; }
    .lane { width: 140px; font-weight: bold; background: #fafafa; }
    .event { display: inline-block; margin: 3px 4px 0 0; padding: 4px 6px; border-radius: 6px; font-size: 11px; cursor: pointer; }
    .router { background: #d7e6ff; }
    .supervisor { background: #ffe1c6; }
    .task { background: #d7f5d7; }
    .context { background: #e1e1ff; }
    .audit { background: #ffe1f2; }
    .hook { background: #f6f0c1; }
    .diff { background: #e6f7ef; }
    .merge { background: #ffd8d8; }
    .duration { background: #e8f0ff; }
    .response { background: #fff3cd; }
    .small { font-size: 10px; color: #444; }
    .controls { margin: 10px 0; }
    .controls label { margin-right: 8px; }
    .hidden { display: none; }
    #detail { margin-top: 12px; padding: 8px; background: #f6f6f6; border: 1px solid #ddd; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>Trace Swimlane (By Turn)</h1>

  <div class=\"controls\">
    __FILTERS__
    <label><input type=\"checkbox\" id=\"toggle-empty\" checked> Show empty lanes</label>
  </div>

  <table id=\"swimlane\">
    <thead>
      <tr>
        <th>Lane</th>
        __TURN_HEADERS__
      </tr>
    </thead>
    <tbody>
      __ROWS__
    </tbody>
  </table>

  <div id=\"detail\">Click an event to see details.</div>

  <script>
    const filters = document.querySelectorAll('.lane-filter');
    const toggleEmpty = document.getElementById('toggle-empty');

    function applyFilters() {
      const active = new Set(Array.from(filters).filter(f => f.checked).map(f => f.value));
      document.querySelectorAll('tr[data-lane]').forEach(row => {
        const lane = row.getAttribute('data-lane');
        const hasEvents = row.getAttribute('data-has-events') === 'true';
        const showLane = active.has(lane) && (toggleEmpty.checked || hasEvents);
        row.style.display = showLane ? '' : 'none';
      });
    }

    filters.forEach(f => f.addEventListener('change', applyFilters));
    toggleEmpty.addEventListener('change', applyFilters);
    applyFilters();

    document.querySelectorAll('.event').forEach(el => {
      el.addEventListener('click', () => {
        const payload = el.getAttribute('data-payload');
        document.getElementById('detail').textContent = payload || 'No details';
      });
    });
  </script>
</body>
</html>
"""


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
            turns.setdefault(current_turn, [])
        turns.setdefault(current_turn, []).append(event)

    lanes = ["router", "supervisor", "task", "context", "audit", "langgraph", "hook", "diff", "merge", "duration", "response"]

    def fmt_event(css: str, label: str, payload: dict) -> str:
        escaped = json.dumps(payload, indent=2)
        return f"<span class=\"event {css}\" data-payload=\"{escaped.replace('"','&quot;')}\">{label}</span>"

    turn_headers = "".join([f"<th>Turn {t}</th>" for t in sorted(turns.keys())])

    rows = []
    for lane in lanes:
        cells = []
        has_events = False
        for t in sorted(turns.keys()):
            cell_events = []
            for event in turns[t]:
                name = event.get("event")
                if lane == "response" and name == "task_response":
                    cell_events.append(fmt_event("response", event.get("response", ""), event))
                elif lane == "router" and name == "router":
                    cell_events.append(fmt_event("router", f"intent:{event.get('intent')}", event))
                elif lane == "supervisor" and name == "supervisor":
                    cell_events.append(fmt_event("supervisor", f"{event.get('decision')}", event))
                elif lane == "task" and name == "task_response":
                    cell_events.append(fmt_event("task", "task_response", event))
                elif lane == "context" and name == "state_diff" and event.get("agent") == "context":
                    cell_events.append(fmt_event("context", "diff", event))
                elif lane == "audit" and name == "state_diff" and event.get("agent") == "audit":
                    cell_events.append(fmt_event("audit", "diff", event))
                elif lane == "langgraph" and name == "state_diff" and event.get("agent") == "langgraph":
                    cell_events.append(fmt_event("context", "diff", event))
                elif lane == "langgraph" and name == "node_duration" and event.get("agent") == "langgraph":
                    cell_events.append(fmt_event("duration", f"langgraph={event.get('ms')}ms", event))
                elif lane == "hook" and name == "hook":
                    cell_events.append(fmt_event("hook", event.get("event", "hook"), event))
                elif lane == "diff" and name == "state_diff":
                    cell_events.append(fmt_event("diff", f"{event.get('agent')}: {', '.join(event.get('diff', {}).keys())}", event))
                elif lane == "merge" and name == "merge_conflict":
                    cell_events.append(fmt_event("merge", "conflict", event))
                elif lane == "duration" and name == "node_duration":
                    cell_events.append(fmt_event("duration", f"{event.get('agent')}={event.get('ms')}ms", event))
            if cell_events:
                has_events = True
            cells.append(f"<td>{''.join(cell_events) or '<span class=\\"small\\">-</span>'}</td>")
        rows.append(f"<tr data-lane=\"{lane}\" data-has-events=\"{str(has_events).lower()}\"><td class=\"lane\">{lane}</td>{''.join(cells)}</tr>")

    filters = "".join([f"<label><input class=\"lane-filter\" type=\"checkbox\" value=\"{lane}\" checked> {lane}</label>" for lane in lanes])

    out = HTML.replace("__TURN_HEADERS__", turn_headers).replace("__ROWS__", "\n".join(rows)).replace("__FILTERS__", filters)
    out_path = Path("outputs/trace_swimlane.html")
    out_path.write_text(out)
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    run()
