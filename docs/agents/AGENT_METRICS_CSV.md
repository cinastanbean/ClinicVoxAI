# Agent Metrics (CSV Driven)

## Dataset
- CSV at `data/scenarios.csv`
- Columns:
  - scenario (required)
  - utterance (required)
  - expected_intent (optional)
  - expected_handoff (optional, use `none` for no handoff)

## Run
```bash
python scripts/eval_agent_metrics_csv.py
```

## Custom CSV
```bash
python scripts/eval_agent_metrics_csv.py --csv path/to/your.csv
```

## Output
- `outputs/agent_metrics_csv.json`
- Includes intent_ok and handoff_ok counts
