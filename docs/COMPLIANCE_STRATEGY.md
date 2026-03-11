# Compliance Strategy (HIPAA-Oriented, MVP)

## 1. Data Minimization
- Store only necessary PHI (demographics, appointment info).
- Do not store raw audio; only store transcripts if needed for QA.

## 2. Encryption & Access
- TLS in transit, AES-256 at rest.
- Role-based access to PHI tables.
- Separate logs from PHI storage.

## 3. Retention
- Session logs: 30-90 days (configurable).
- Transcripts: optional, default 30 days.
- Audit logs: 1-6 years depending on clinic policy.

## 4. Vendor Compliance
- Sign BAA with telephony, STT, TTS, LLM, and hosting vendors.
- Maintain a vendor inventory with compliance status.

## 5. Patient Disclaimers
- Opening HIPAA notice.
- AI is not providing medical advice.
- Clear handoff mechanism.

## 6. Monitoring
- Track access to PHI.
- Alert on anomalous access patterns.

