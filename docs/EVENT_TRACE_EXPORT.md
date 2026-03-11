# Event Trace Export

## Purpose
Export structured events + state snapshots for learning and debugging.

## Output
- `outputs/trace.json`
- Contains:
  - events: ordered event list
  - snapshots: state after each turn

## How to Run
```bash
python scripts/export_events.py
```
