# Repository Skeleton & Conventions

## Purpose
Define a clean, testable structure for a multi-agent voice system without implementing business logic yet.

## Top-level
- `docs/` architecture, contracts, and analysis
- `app/` source code (to be implemented)
- `infra/` deployment and config (to be implemented)

## Proposed `app/` Structure
- `app/main.py` entrypoint (wire-up only)
- `app/graph/` LangGraph definitions
- `app/agents/` Router, Task, Supervisor
- `app/tools/` DB, Calendar, Report, Notification, Handoff
- `app/voice/` STT, TTS, Telephony adapters
- `app/compliance/` audit, encryption helpers
- `app/prompts/` prompt templates

## Naming Conventions
- snake_case for functions and modules
- JSON schemas in `docs/` for contracts

## Testing Strategy (placeholder)
- `tests/` for unit + contract tests
- Add fixtures for transcripts and tool responses

