# Intent Switch Example

## Scenario
Caller starts with scheduling, then asks about report mid-call.

## Transcript
1. "I want to schedule an appointment."
2. "My first name is Jane."
3. "Actually, can you tell me my lab results?"

## Expected State Transitions
- Turn 1: intent = schedule, appointment_context initialized
- Turn 2: collect fields (first_name)
- Turn 3: Router updates intent to report
  - reset appointment_context
  - set report_context

## Outcome
- Task Agent switches to report flow
- If verification is incomplete, ask for identity confirmation
