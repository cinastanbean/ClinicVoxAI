# Agent State Contract (MVP)

## Purpose
Define a single shared state for LangGraph agents. Enforce clear ownership and update rules to prevent conflicting writes and stale context.

## 1. State Object (Schema)
```json
{
  "session_id": "uuid",
  "turn_id": 0,
  "caller_phone": "+1XXXXXXXXXX",
  "patient_id": "string|null",
  "patient_type": "new|existing|unknown",
  "intent": "registration|schedule|reschedule|cancel|report|insurance|medication|other|unknown",
  "intent_confidence": 0.0,
  "verification_status": "unverified|partial|verified|failed",
  "collected_fields": {
    "first_name": "string|null",
    "last_name": "string|null",
    "dob": "YYYY-MM-DD|null",
    "email": "string|null",
    "insurance_provider": "string|null",
    "insurance_member_id": "string|null",
    "reason_for_visit": "string|null"
  },
  "appointment_context": {
    "provider_id": "string|null",
    "department": "string|null",
    "slot_candidates": ["ISO-8601"],
    "selected_slot": "ISO-8601|null",
    "appointment_id": "string|null"
  },
  "report_context": {
    "report_id": "string|null",
    "report_type": "lab|imaging|note|null",
    "report_text": "string|null",
    "summary": "string|null"
  },
  "handoff_reason": "string|null",
  "last_agent": "string",
  "errors": [
    {"source":"agent|tool","code":"string","message":"string"}
  ]
}
```

## 2. Ownership Rules (Single Writer)
- `Router Agent`:
  - writes: `patient_type`, `intent`, `intent_confidence`, `last_agent`
- `Registration Agent`:
  - writes: `collected_fields`, `patient_id` (after DB create), `last_agent`
- `Verification Agent`:
  - writes: `verification_status`, `patient_id` (after DB match), `last_agent`
- `Scheduling Agent`:
  - writes: `appointment_context`, `last_agent`
- `Report Agent`:
  - writes: `report_context`, `last_agent`
- `General Agent`:
  - writes: `last_agent`, may append `errors` only
- `Supervisor/Guard Agent` (if used):
  - writes: `handoff_reason`, may override `intent` if confidence low

## 3. Update Rules
- Every turn increments `turn_id`.
- If `intent` changes, reset `appointment_context` and `report_context`.
- If `patient_id` changes, reset `verification_status` to `unverified`.
- All agents must append errors rather than overwrite.

## 4. Validation & Invariants
- `patient_type` cannot be `existing` unless `verification_status` is not `unverified`.
- `selected_slot` must be in `slot_candidates`.
- `report_text` must be present before `summary` is written.

## 5. State Reset Triggers
- New call => state reset except `caller_phone` and `session_id`.
- Human handoff => freeze state, stop agent writes.

