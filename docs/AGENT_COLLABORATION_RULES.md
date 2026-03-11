# Agent Collaboration Rules (Enforced)

## Ownership
Each agent is allowed to write only specific fields:
- router: patient_type, intent, intent_confidence
- supervisor: handoff_reason
- task: patient_id, verification_status, verification_attempts, collected_fields, appointment_context, report_context

## Enforcement
- GraphEngine compares state before/after a node.
- Writes outside ownership are recorded as errors and logged as `ownership_violation`.

## Purpose
This makes collaboration explicit and debuggable for learning.
