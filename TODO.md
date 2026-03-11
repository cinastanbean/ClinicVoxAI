# TODO

## Product-grade Integrations (Needs Production Hardening)
- Twilio/Retell Media Stream: run with real credentials, webhooks, and production retry rules
- Real-time STT/TTS providers: tune latency/quality tradeoffs and failover
- Production LLM calls with guardrails and JSON validation
- Real DB + calendar/EHR integration (patient matching, consent, and audit trail)

## Compliance & Security (Beyond Mock)
- Formal BAA workflow and vendor management
- PHI retention policy enforcement
- Access control and audit trail hardening
 - Data minimization and PII redaction policy enforcement in logs

## Reliability & Ops
- Metrics pipeline (Prometheus/Grafana or equivalent)
- Alert routing to external system (PagerDuty/Slack)
- Background job system for retries
 - Circuit breakers per tool with backoff policies

## UX/Conversation Quality
- Better intent memory and slot-filling strategy
- More robust verification flows (fuzzy match, multi-factor)
 - Dynamic prompts per clinic policy (handoff thresholds, allowed info)

## Engineering Cleanups
- Consolidate `PYTHONPATH` handling for scripts (bootstrap helper or package install)
- Add schema versioning for state snapshots and traces
