# Architecture Review - Multi-Agent Clinic Assistant

## Summary
This design is viable for learning multi-agent orchestration, but there are structural risks that can create hidden complexity and degrade reliability if not addressed early. Below are the key issues and recommended adjustments.

## Key Issues & Reflections

### 1. Agent Over-Segmentation
**Issue:** Too many specialized agents can lead to brittle handoffs and state loss. The more agents you add, the more you depend on perfect routing and shared state.

**Impact:** Higher failure rate in real calls; harder to debug; more latency from repeated LLM calls.

**Mitigation:**
- Start with 2–3 agents only (Router + Task Agent + Fallback) then split when you can demonstrate stable flows.
- Keep “Registration” and “Verification” as skills/tools inside a single Task Agent in MVP.

### 2. Ambiguous Ownership of Shared State
**Issue:** If multiple agents write to shared fields, you can get inconsistent or stale data (e.g., intent changes but appointment context not reset).

**Impact:** Incorrect actions (wrong slot booked, wrong patient ID used).

**Mitigation:**
- Enforce single-writer rules per state field.
- Adopt event-sourced updates or immutable snapshots per turn.

### 3. Router Accuracy as a Single Point of Failure
**Issue:** Router misclassification can send users to the wrong agent and poison the flow.

**Impact:** User frustration; higher handoff rate.

**Mitigation:**
- Use confidence thresholds with fallback to a general agent.
- Allow mid-conversation reroute when intent changes.

### 4. Report Agent Safety Risks
**Issue:** Even summarization can drift into advice if prompts are not constrained, especially with non-deterministic outputs.

**Impact:** Compliance and clinical risk.

**Mitigation:**
- Strict template + forced extraction from report text only.
- Add a “verbatim quote” mode for high-risk sections.

### 5. Latency From Multi-Agent Calls
**Issue:** Each agent call adds latency; voice UX tolerates little delay.

**Impact:** Calls feel sluggish; STT/TTS pipeline stalls.

**Mitigation:**
- Minimize LLM calls per turn.
- Use cheaper/faster models for routing.
- Cache resolved patient metadata in session.

### 6. Tooling Boundaries Are Under-Specified
**Issue:** The architecture mentions tools but not strict contract definitions.

**Impact:** Implementation ambiguity; inconsistent handling of errors.

**Mitigation:**
- Define tool schemas (inputs/outputs) and error codes before code.
- Add circuit-breakers and retries per tool.

### 7. HIPAA and Data Minimization Needs More Detail
**Issue:** “Don’t store audio” and “encrypt PHI” are necessary but not sufficient.

**Impact:** Audit failure risk.

**Mitigation:**
- Define retention periods and log redaction strategy.
- Separate PHI storage from logs.

## Recommendation for Learning Goals
If your goal is learning multi-agent cooperation, build a minimal but explicit collaboration pattern:
- Router decides intent
- Task Agent executes via tools and has sub-flows
- Supervisor Agent monitors confidence and decides handoff

This still demonstrates multi-agent coordination, but avoids fragile handoff chains.

## Next Document to Create (Suggested)
- Agent State Contract (schemas + ownership rules)
- Tool Interface Contracts (DB/Calendar/Notification)
- Evaluation plan for routing accuracy and handoff rate
