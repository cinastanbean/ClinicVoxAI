# LangGraph Usage (Runnable)

## Install
```
pip install langgraph
```

## Enable
Set in `app/config.py`:
- `use_langgraph = True`

## Run Demo
```
python scripts/demo_langgraph_run.py
```

## Notes
- Uses the same Router/Supervisor/Task agents.
- `state.meta["text"]` carries the current turn text.
