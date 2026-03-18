# Handoff Policy

## Trigger Conditions
- Supervisor decision == handoff
- handoff_reason set by TaskAgent or Supervisor

## Current Reasons
- verification_failed
- tool_errors
- unspecified

## Flow
- Orchestrator calls HandoffTool.transfer(reason)
- User receives a standard handoff response

## Future
- Add queue selection by reason
- Include context summary
