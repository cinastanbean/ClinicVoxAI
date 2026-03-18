# Technical Design: Voice AI Clinic Assistant (Learning Demo)

## 1) Goals
- Teach multi-agent collaboration patterns in a clinic call center domain.
- Provide an end-to-end flow that can run without real telephony, while keeping interfaces compatible with Twilio/Retell and OpenAI Realtime.
- Make orchestration and state transitions visible via trace + swimlane outputs.

## 2) Non-goals
- Production HIPAA compliance, vendor BAAs, or audited security controls.
- Real EHR integration or medical decision-making.
- Fully natural conversation policy for all edge cases.

## 3) System Architecture (Text Diagram)
```
Inbound (HTTP/WebSocket)
  -> Twilio/Retell Media Stream (optional)
  -> Realtime bridge (OpenAI Realtime WS) OR text simulator
  -> LangGraph Orchestrator (Router -> Supervisor -> Task)
  -> Tools (DB / Calendar / Reports / Notifications)
  -> State + Trace Recorder
  -> Outputs (trace.html / swimlane.html / timeline.html / collab_summary.csv)
```

## 4) Key Modules
- `app/main.py`
  - FastAPI server. Exposes endpoints for mock calls and streaming demos.
- `app/graph/langgraph_flow.py`
  - LangGraph nodes: `router`, `supervisor`, `task`.
- `app/graph/langgraph_runtime.py`
  - Orchestration runtime: invokes LangGraph, records diffs, writes traces.
- `app/agents/router.py`
  - Intent classification and context reset on intent switch.
- `app/agents/supervisor.py`
  - Confidence and error-based escalation rules.
- `app/agents/task.py`
  - Slot-filling, verification, scheduling, report summarization.
- `app/voice/twilio_stream.py`
  - Media Stream -> OpenAI Realtime bridge, adaptive VAD, audio capture.
- `app/voice/openai_realtime.py`
  - OpenAI Realtime WS client configuration.
- `app/graph/recorder.py`
  - Trace capture for every turn, agent output, diffs, and durations.

## 5) Agent Collaboration Flow
### 5.1 Router Agent
- Input: user text (or transcript from speech).
- Output: `state.intent`, `state.patient_type`, `state.intent_confidence`.
- Behavior: if user intent changes, reset context objects and increment context versions.

### 5.2 Supervisor Agent
- Evaluates intent confidence and error conditions.
- Outputs `state.meta.decision`.
  - `proceed`: task agent handles.
  - `clarify`: ask a clarifying question and possibly loop.
  - `handoff`: stop automation and hand off.

### 5.3 Task Agent
- Implements domain logic and tool calls.
- Decision flow:
  - `schedule/registration`: collect basic info, create patient, find slots, book.
  - `cancel/reschedule`: verify identity, request appointment ID, update schedule.
  - `report`: verify identity, fetch report, summarize.

### 5.4 State Synchronization
- `SessionState` is the single source of truth.
- After each LangGraph invocation, `apply_state` deep-copies the updated state into the in-memory session.
- Every turn is diffed (`state_diff`) to show what fields were written.

## 6) State Model
Main state object: `app/graph/state.py`
- `SessionState`
  - `intent`, `patient_type`, `verification_status`, `handoff_reason`, `last_agent`.
  - `collected_fields` (first/last name, DOB, email, insurance, reason).
  - `appointment_context` (slots, selection, appointment id, version).
  - `report_context` (report text/summary, version).
  - `meta` for per-turn scratch data (text, decision, last_response).

The `version` field in contexts increments on intent switch to make resets visible in traces and tests.

## 7) Message Handling Pipeline
### 7.1 Text Mode (No Voice)
- Input: transcript text string.
- Flow: `LangGraphRuntime.handle_turn()`
  - updates `state.turn_id`
  - sets `state.meta.text`
  - invokes graph
  - records `state_diff`, `task_response`, `node_duration`

### 7.2 Voice Mode (Twilio Media Stream)
- Input: Twilio WebSocket with base64 G.711 µ-law frames.
- Steps:
  - `twilio_stream.py` buffers audio and forwards to OpenAI Realtime.
  - Adaptive VAD detects speech end.
  - OpenAI Realtime returns audio chunks + transcripts.
  - Output audio is queued and sent back to Twilio as `media` frames.

### 7.3 Audio Recording Outputs
- Each outbound chunk is recorded into WAV segments.
- Files:
  - `outputs/twilio_out_<callSid>_<index>_<timestamp>.wav`
  - `outputs/twilio_out_<callSid>_segments.json`
- Merging:
  - `scripts/merge_twilio_segments.py` produces `*_merged.wav` and `*.srt`.

## 8) Tools and External Integrations
- `SQLitePatientDB` and `SQLiteCalendar` are local scaffolds.
- `SQLiteReportStore` seeds demo report content.
- `NotificationTool` is a stub that logs SMS sends.
- Twilio/Retell endpoints are implemented as demo-ready, not production-hardened.

## 9) Observability and Tracing
- `EventRecorder` captures per-turn events:
  - `turn_start`, `router`, `supervisor`, `task_response`, `state_diff`, `node_duration`.
- Renderers:
  - `scripts/render_trace_html.py` -> `outputs/trace.html`
  - `scripts/render_trace_swimlane.py` -> `outputs/trace_swimlane.html`
  - `scripts/render_trace_timeline.py` -> `outputs/trace_timeline.html`
  - `scripts/render_collab_summary.py` -> `outputs/collab_summary.csv`

The swimlane view is the best teaching artifact: each lane is an agent or system function and each turn is a column.

### How to Read the Swimlane
1. Each column is a turn (one user input + one system response).
2. Each row (lane) is an agent or system role:
   - `router`: intent detection and context reset
   - `supervisor`: decide clarify / proceed / handoff
   - `task`: domain handling and tool calls
   - `langgraph`: orchestration wrapper and state diff
   - `diff`: field-level updates recorded per turn
3. Colored badges in each cell represent events recorded during that turn.
4. The `duration` badges show approximate per-node execution time in ms.
5. Context resets are visible when `appointment_context.version` or `report_context.version` increments.

## 10) Conflict Handling and Parallel Branching
- Parallel demo scripts use forked copies of state.
- After parallel branches, a merge phase detects conflicts based on field-level diffs.
- Conflicts are recorded as `merge_conflict` events and visualized in traces.

## 11) Failure Handling
- Tool calls go through `ResilientCall` for a single retry wrapper.
- Fault injection toggles let you simulate tool failures to test handoff logic.
- Supervisor’s `handoff` decision is used for irrecoverable errors.

## 12) Configuration
- `app/config.py` controls:
  - routing backend (rules vs mock LLM vs OpenAI)
  - storage backend (sqlite / sqlalchemy / memory)
  - enabling OpenAI summarizer

Note: LangGraph is the default orchestrator in this demo.

## 13) Example Sequence (Schedule -> Report)
1. User: “I want to schedule an appointment.”
2. Router -> intent `schedule`, reset context.
3. Supervisor -> `proceed`.
4. Task -> asks for name + DOB.
5. User provides details -> Task creates patient.
6. Task proposes time slots.
7. User selects a slot -> Task books appointment and sends SMS.
8. User asks for report -> Router switches to `report`, resets appointment context.
9. Task verifies identity and summarizes report.

## 14) Extensibility Patterns
- Add new intent:
  - update `app/rules.py` keywords.
  - extend task handler for new intent.
  - update tests and evaluation datasets.
- Add new agent:
  - create agent class and hook into LangGraph.
  - log `state_diff` for visibility.

## 15) Known Limitations (Demo-Specific)
- Router rules are simple keyword-based and can misclassify ambiguous phrases.
- Verification is strict phone + DOB match without fuzzy logic.
- Audio pipelines are functional but not tuned for latency or call quality.

## 16) Entry Points
- API server: `uvicorn app.main:app --reload`
- Test suite: `pytest -q`
- Demos: `python scripts/run_all_demos.py`
- Trace export: `python scripts/export_events.py`
