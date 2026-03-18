# Agent Collaboration Flow (Detailed)

## Step-by-step (Scheduling + Switch Example)
1. Router reads caller text and sets intent + confidence.
2. Supervisor validates confidence or errors.
3. Task Agent executes current intent.
   - Extracts fields from text.
   - Calls tools if minimum required fields exist.
4. If caller changes intent mid-call, Router updates intent and resets context.
5. Task Agent switches flow based on new intent.

## Error Escalation
- Tool errors -> append to state.errors -> Supervisor decides clarify/handoff.
- Low confidence -> clarify loop back to Router.

## Why This Matters
This shows how agents cooperate via shared state rather than direct calls between agents.
