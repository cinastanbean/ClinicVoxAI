# Evaluation Plan (MVP)

## Goals
Measure routing accuracy, task completion, and handoff effectiveness.

## Metrics
- Router accuracy (new vs existing)
- Intent accuracy (top-1)
- Task completion rate without handoff
- Handoff rate with reason codes
- Mean turn count per task
- End-to-end latency per turn

## Test Sets
- 50 scripted calls (new patient)
- 50 scripted calls (existing patient)
- 20 edge cases (mumbling, missing DOB, intent switches)

## Acceptance Criteria
- Router accuracy >= 90%
- Intent accuracy >= 85%
- Simple scheduling completion >= 80%
- Latency <= 2s on average

## Logging Requirements
- Capture: session_id, intent, confidence, handoff_reason, tool errors
- Redact PHI in analysis exports
