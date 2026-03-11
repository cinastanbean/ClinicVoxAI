# Voice -> Agent -> Tool Sequence (MVP)

## 1. Typical Scheduling Flow
1. Caller speaks
2. STT produces transcript
3. Router Agent classifies intent
4. Supervisor Agent validates confidence
5. Task Agent asks for missing fields
6. Task Agent calls Calendar Tool
7. Task Agent confirms slot
8. Notification Tool sends SMS
9. TTS responds to caller

## 2. Report Summary Flow
1. Caller asks about results
2. Router Agent selects report intent
3. Supervisor checks safety conditions
4. Task Agent calls Report Tool
5. Task Agent summarizes strictly from report text
6. If advice requested => Handoff Tool

## 3. Error Flow
- Tool error => append error => Supervisor decides retry/clarify/handoff
- Two failed clarifications => handoff

