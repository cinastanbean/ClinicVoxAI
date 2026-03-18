# LangGraph Trace Integration

LangGraphRuntime records:
- turn_start
- node_duration (langgraph)
- state_diff (langgraph)
- task_response

These are included in the same `outputs/trace.json` format and compatible with swimlane/timeline renderers.

## Switch
Set `use_langgraph = True` in `app/config.py` and start the server.
