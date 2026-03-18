# State Machine Diagram (Text)

## Overview
This diagram reflects the current Router -> Supervisor -> Task flow and the handoff/clarify paths.

```
[START]
   |
   v
[ROUTER]
   |
   v
[SUPERVISOR] --- handoff ---> [HANDOFF]
   |
   +--- clarify ---> [CLARIFY] -> [ROUTER]
   |
   +--- proceed ---> [TASK] ----> [END]
                   |   |
                   |   +-- tool error --> [SUPERVISOR]
                   |
                   +-- intent switch --> [ROUTER]
```

## Notes
- Clarify loops back to Router to re-classify intent.
- Task tool errors are escalated to Supervisor.
- Intent switching should trigger context reset.
