# Voice AI Clinic Assistant

This repo is a learning-oriented multi-agent voice assistant scaffold.

## Quick Start (Local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Note: when running `scripts/*.py` directly, set `PYTHONPATH=.` so imports resolve.

## Simulate a Call
```bash
curl -X POST http://127.0.0.1:8000/call/simulate \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"S1","caller_phone":"+15550000000","transcript":["I want to schedule an appointment","My name is Jane Doe and my birthday is 1990-01-01","I can do Wednesday morning"]}'
```

## CLI Simulator
```bash
python -m app.cli_simulator
```

## Demo Script
```bash
python scripts/demo_call.py
```

## Export Trace
```bash
python scripts/export_events.py
```

## Compare Snapshots
```bash
python scripts/compare_snapshots.py
```

## Intent Switch Demo
```bash
python scripts/demo_intent_switch.py
```

## Verification Demo (Example)
Use report intent and provide DOB to see verification occur.

## Verification Failure Demo
```bash
python scripts/demo_verification_failure.py
```

## Handoff Demo
```bash
python scripts/demo_handoff.py
```

## Full Flow Demo
```bash
python scripts/demo_full_flow.py
```

## Parallel/Branch Demo
```bash
python scripts/demo_parallel_branch.py
```

## Conflict Demo
```bash
python scripts/demo_conflict.py
```

## Voice Pipeline Demo (Mock)
```bash
python scripts/demo_voice_pipeline.py
```

## Fault Injection Demo
```bash
python scripts/demo_fault_injection.py
```

## Mock Voice API
```bash
curl -X POST http://127.0.0.1:8000/voice/mock \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"V1","caller_phone":"+15550000000","audio_chunks":["I want to schedule an appointment","My first name is Jane"]}'
```

## OpenAI STT/TTS (Scaffold)
```bash
curl -X POST http://127.0.0.1:8000/stt/openai -F "file=@sample.wav"
```

## Twilio/Retell Stream Simulation
```bash
python scripts/demo_twilio_stream_sim.py
python scripts/demo_retell_stream_sim.py
```

## Merge Twilio WAV Segments + SRT
```bash
python scripts/merge_twilio_segments.py
```

## LangGraph Demo
```bash
python scripts/demo_langgraph_run.py
```

## OpenAI Stub Demo
```bash
python scripts/demo_openai_stub.py
```

## Run All Demos
```bash
python scripts/run_all_demos.py
```

## Trace Visualization
```bash
python scripts/export_events.py
python scripts/render_trace_html.py
```

## Trace Timeline
```bash
python scripts/export_events.py
python scripts/render_trace_timeline.py
```

## Trace Swimlane
```bash
python scripts/export_events.py
python scripts/render_trace_swimlane.py
```

## Collaboration Summary
```bash
python scripts/export_events.py
python scripts/render_collab_summary.py
```

## Configuration
- app/config.py
  - set `router_backend = "openai"` to use OpenAI for routing
  - LangGraph is the default orchestrator (the `use_langgraph` flag is now deprecated)

## Tests
```bash
python -m pytest -q
```

## Regression Checklist
- docs/REGRESSION_CHECKLIST.md

## Rules Configuration
- app/rules.py

## Collaboration Rules
- docs/AGENT_COLLABORATION_RULES.md

## Graph Visualization
- docs/GRAPHVIZ_DOT.md
- docs/GRAPH_SVG.svg

## Router Evaluation
```bash
python scripts/eval_router.py
```

## Router Evaluation (JSON)
```bash
python scripts/eval_router_json.py
```

## Agent Metrics
```bash
python scripts/eval_agent_metrics.py
```

## Agent Metrics (CSV)
```bash
python scripts/eval_agent_metrics_csv.py
```

## Docs
- `docs/PROJECT_PLAN.md`
- `docs/ARCHITECTURE_REVIEW.md`
- `docs/AGENT_STATE_CONTRACT.md`
- `docs/TOOL_INTERFACES.md`
- `docs/LANGGRAPH_ORCHESTRATION.md`
- `docs/TECHNICAL_DESIGN.md`
- `docs/DEMO_REPORT.md`
- `docs/SEQUENCE_FLOW.md`
- `docs/FULL_FLOW_WITH_MOCKS.md`
- `docs/VOICE_PIPELINE.md`
- `docs/COMPLIANCE_MOCKS.md`
- `docs/MONITORING_MOCKS.md`
- `docs/RECOVERY_MOCKS.md`
- `docs/FLOW_COVERAGE.md`
- `docs/LLM_MOCK_PIPELINE.md`
- `docs/ALERT_RECOVERY_DEMO.md`
- `docs/CONFIG_SWITCHES.md`
- `docs/ALERT_PATHS.md`
- `docs/FAULT_INJECTION.md`
- `docs/SWIMLANE_TRACE.md`
- `docs/COLLAB_SUMMARY.md`
- `docs/DURATION_TRACE.md`
- `docs/REAL_INTEGRATIONS.md`
- `docs/OPENAI_USAGE.md`
- `docs/OPENAI_STT_TTS.md`
- `docs/WEBHOOKS.md`
- `docs/LANGGRAPH_USAGE.md`
- `docs/REALTIME_STREAMING.md`
- `docs/TWILIO_MEDIA_STREAMS.md`
- `docs/RETELL_STREAMING.md`
- `docs/TWILIO_NGROK.md`
- `docs/REALTIME_PIPELINE_END2END.md`
- `docs/TWILIO_REALTIME_AUDIO.md`
- `docs/LANGGRAPH_TRACE.md`
- `docs/SEGMENT_MERGE_AND_SRT.md`
