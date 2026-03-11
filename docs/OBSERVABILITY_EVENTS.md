# Observability Events

## Event Types
- turn_start: new user turn
- router: intent + confidence
- supervisor: decision + handoff_reason
- task_response: outgoing message

## Sample Log
[event=turn_start] {'turn_id': 1, 'text': 'I want to schedule an appointment'}
[event=router] {'intent': 'schedule', 'confidence': 0.75}
[event=supervisor] {'decision': 'proceed', 'handoff_reason': None}
[event=task_response] {'response': 'Please tell me your first name, last name, date of birth.'}

## Notes
- Logs are console-only in MVP.
- PHI should be redacted in production.
