# Regression Checklist

## Core Flows
- New patient schedule flow completes
- Intent switch resets contexts
- Report request requires verification
- Verification failure triggers handoff
- Handoff tool invoked by Supervisor

## Observability
- Event log outputs per turn
- Trace export file generated

## Config
- Supervisor thresholds loaded from config
- Router backend switch works (rules default)
