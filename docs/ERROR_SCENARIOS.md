# Error Scenarios (MVP)

## 1. Low Intent Confidence
- Router outputs confidence < threshold
- Supervisor returns clarify

## 2. Tool Errors
- TaskAgent appends to state.errors
- Supervisor handoffs if errors exceed max

## 3. Missing Patient ID for Report
- Task Agent requests verification

## 4. No Slots Available
- Task Agent offers handoff
