# Voice AI Clinic Assistant - Project Plan (PRD Style)

## 1. Overview
**Goal:** Build a phone-based AI voice assistant for small US clinics to handle common patient calls (new patient registration, scheduling, report explanation, FAQs) with HIPAA-aligned safeguards and seamless human handoff.

**Primary outcomes (MVP):**
- >= 80% of simple scheduling/report queries completed without human transfer
- Patient satisfaction >= 4.0/5 (post-call survey)
- HIPAA baseline audit readiness (encryption, access control, audit logs)

## 2. Scope
**In scope (MVP):**
- English (US) voice calls only
- New patient registration (basic demographics + insurance fields)
- Existing patient verification (phone + DOB or name + DOB)
- Scheduling (book/reschedule/cancel)
- Report summaries (non-diagnostic, restate provider notes)
- Human handoff

**Out of scope (MVP):**
- Full EHR write-back (beyond minimal patient profile)
- Multi-language support
- Advanced triage or clinical decision support
- Billing or payment collection

## 3. User Flows (High-Level)
### 3.1 New Patient
1. HIPAA consent disclosure
2. Collect identity + contact + insurance + reason for visit
3. Match to department/provider
4. Offer available slots and confirm
5. Send confirmation SMS/email

### 3.2 Existing Patient
1. Verify identity (phone + DOB, or name + DOB)
2. Intent routing
   - Schedule/reschedule/cancel
   - Report explanation
   - Other FAQ
3. If low confidence or out-of-scope => human transfer

## 4. Architecture (Text Diagram)
```
Caller
  -> Telephony (Twilio/Retell)
  -> Streaming STT
  -> LangGraph Orchestrator
       -> Router Agent
          -> Registration Agent
          -> Verification Agent
          -> Scheduling Agent
          -> Report Agent
          -> General Agent
       -> Tools: DB, Calendar, Notification, Handoff
  -> TTS
  -> Caller

Observability + Compliance
  -> Audit logs, PHI encryption, access policies
```

## 5. Multi-Agent Design (LangGraph)
**Shared State:**
- session_id
- caller_phone
- patient_id (if resolved)
- patient_type (new/existing)
- intent + confidence
- verification_status
- collected_fields
- handoff_reason

**Agents:**
- Router Agent: classify new/existing + primary intent
- Registration Agent: gather fields, validate, store
- Verification Agent: match identity, return patient_id
- Scheduling Agent: slot search, booking workflow
- Report Agent: retrieve report, summarize, enforce safety rules
- General Agent: clarifications, repeats, fallback

## 6. Non-Functional Requirements
- End-to-end latency <= 2s typical
- Concurrency: 50-100 calls with scale-out
- Security: TLS in transit, AES-256 at rest, PHI access controls
- Compliance: BAA for vendors, audit logs, data minimization

## 7. Risk Register & Mitigations
1. **STT errors during verification**
   - Mitigation: multi-turn confirmation, alternate verification paths, fallback to human
2. **Hallucinated medical advice**
   - Mitigation: strict prompt constraints, retrieval-only summaries, disclaimers
3. **High latency in long calls**
   - Mitigation: streaming, caching, restrict LLM usage, model tiering
4. **Calendar integration mismatch**
   - Mitigation: implement adapter interface; start with one provider
5. **PHI leakage in logs**
   - Mitigation: PHI redaction and encrypted storage with strict access

## 8. MVP Roadmap (Phased)
**Phase 0: Foundations**
- Define data schema (patient, appointment, report)
- Decide vendor stack and compliance approach
- Set up repo structure and docs

**Phase 1: Voice loop + Router**
- Telephony ingress
- Streaming STT/TTS
- Router Agent with intent classification

**Phase 2: New patient flow**
- Registration Agent
- Appointment booking
- SMS/email confirmation

**Phase 3: Existing patient flow**
- Verification Agent
- Reschedule/cancel flows
- Report Agent summaries

**Phase 4: Quality & Compliance**
- Call metrics + audit logging
- Retry/failure handling
- Handoff rules

## 9. Prompt Templates (Initial Draft)
### 9.1 Router Agent
```
System: You are a clinic phone assistant.
Task: classify caller as NEW or EXISTING and choose intent from:
[registration, schedule, reschedule, cancel, report, insurance, medication, other].
Return JSON only.

User: "I need to move my appointment from next week."
Assistant (JSON): {"patient_type":"existing","intent":"reschedule","confidence":0.86}
```

### 9.2 Report Agent
```
System:
You summarize medical reports in plain language.
Rules:
- Do not add new diagnosis.
- Only restate what the doctor wrote.
- If asked for advice, suggest speaking to a clinician.

User:
Report: "Impression: Mild degenerative changes in L4-L5..."

Assistant:
"The report says there are mild age-related changes in the lower spine (L4-L5).
No urgent findings were noted. If you want medical advice, I can connect you to a clinician."
```

## 10. Open Questions (to resolve during Phase 0)
- Which telephony vendor is preferred (Twilio vs Retell)?
- Which calendar system is in use at pilot clinic?
- Is report access via DB or EHR export?
- Preferred notification channel (SMS vs email vs both)?

## 11. Analysis Notes (Working)
- Focus on scheduling and report summaries yields highest ROI in front-desk load reduction.
- HIPAA risk is best reduced by minimizing stored PHI and limiting retention.
- If EHR integration is too heavy, MVP should use a shadow DB keyed by phone + DOB.
