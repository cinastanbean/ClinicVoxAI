# LangGraph Orchestration Design (MVP)

## 1. Design Goals
- Demonstrate multi-agent collaboration with minimal fragility.
- Keep agent count low while preserving clear responsibility.
- Enforce state ownership rules from AGENT_STATE_CONTRACT.md.

## 2. Proposed Graph (Minimal)
Agents:
- Router Agent (classification only)
- Task Agent (executes flows with tool calls)
- Supervisor/Guard Agent (handoff decisions, confidence checks)

Rationale: This still demonstrates multi-agent coordination but avoids brittle handoffs.

## 3. Node Flow (Text Diagram)
```
Start
 -> Router Agent
 -> Supervisor Agent
    -> If handoff: Handoff Tool -> End
    -> Else: Task Agent
       -> Tool Calls (DB/Calendar/Report/Notify)
       -> If error/low confidence: Supervisor Agent
       -> Else: End
```

## 4. State Update Rules (Applied)
- Router updates `patient_type`, `intent`, `intent_confidence` only.
- Supervisor can override intent on low confidence and set `handoff_reason`.
- Task Agent updates domain fields only (registration/scheduling/report).

## 5. Tool Error Strategy
- Errors are appended to `errors` array.
- Supervisor decides whether to retry, ask for clarification, or transfer.

## 6. Intent Switching
If user changes intent mid-call:
- Router re-evaluates intent
- Task Agent resets context fields according to rules

## 7. Fallback Rules
- 2 consecutive ASR failures => transfer
- 3 consecutive misunderstandings => transfer
- Any prohibited request => transfer

