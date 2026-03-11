# Data Model Draft (MVP)

## 1. Patient
- patient_id (string, PK)
- first_name (string)
- last_name (string)
- dob (date)
- phone (string)
- email (string, nullable)
- insurance_provider (string, nullable)
- insurance_member_id (string, nullable)
- created_at (timestamp)
- updated_at (timestamp)

## 2. Appointment
- appointment_id (string, PK)
- patient_id (string, FK)
- provider_id (string)
- department (string)
- slot_time (timestamp)
- status (confirmed|rescheduled|cancelled)
- created_at (timestamp)
- updated_at (timestamp)

## 3. Report
- report_id (string, PK)
- patient_id (string, FK)
- report_type (lab|imaging|note)
- report_text (text)
- report_date (date)
- created_at (timestamp)

## 4. Call Session
- session_id (string, PK)
- caller_phone (string)
- patient_id (string, nullable)
- start_time (timestamp)
- end_time (timestamp)
- intent (string)
- handoff_reason (string, nullable)
- outcome (completed|handoff|failed)

## 5. Audit Log
- audit_id (string, PK)
- session_id (string)
- event_type (string)
- timestamp (timestamp)
- actor (agent/tool/system)
- details (json, redacted)

