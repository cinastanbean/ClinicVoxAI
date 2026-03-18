# Supervisor Policy

## Overview
SupervisorAgent uses a simple policy to decide whether to proceed, clarify, or handoff.

## Current Parameters
- low_confidence_threshold: 0.5
- max_errors_before_handoff: 2

## Behavior
- If intent_confidence < threshold => clarify
- If error count >= max_errors_before_handoff => handoff
- If handoff_reason is set => handoff
- Otherwise => proceed

## Extension Ideas
- Add ASR failure counter
- Add maximum turns before handoff
- Add escalation for prohibited medical advice
