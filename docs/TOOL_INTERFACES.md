# Tool Interface Contracts (MVP)

This document defines tool schemas and error contracts for agent calls.

## 1. Patient DB Tool
### 1.1 Create Patient
**Input**
```json
{
  "first_name": "string",
  "last_name": "string",
  "dob": "YYYY-MM-DD",
  "phone": "+1...",
  "email": "string|null",
  "insurance_provider": "string|null",
  "insurance_member_id": "string|null"
}
```
**Output**
```json
{"patient_id":"string"}
```
**Errors**
- `DUPLICATE_PATIENT`
- `INVALID_DOB`
- `MISSING_REQUIRED`

### 1.2 Find Patient
**Input**
```json
{"phone":"+1...","dob":"YYYY-MM-DD"}
```
**Output**
```json
{"patient_id":"string|null","match_confidence":0.0}
```
**Errors**
- `MISSING_REQUIRED`

## 2. Calendar Tool
### 2.1 Get Available Slots
**Input**
```json
{
  "provider_id":"string|null",
  "department":"string|null",
  "date_range":{"start":"YYYY-MM-DD","end":"YYYY-MM-DD"}
}
```
**Output**
```json
{"slots":["ISO-8601"]}
```
**Errors**
- `NO_AVAILABILITY`
- `INVALID_RANGE`

### 2.2 Book Appointment
**Input**
```json
{"patient_id":"string","slot":"ISO-8601"}
```
**Output**
```json
{"appointment_id":"string","status":"confirmed"}
```
**Errors**
- `SLOT_TAKEN`
- `INVALID_PATIENT`

### 2.3 Reschedule Appointment
**Input**
```json
{"appointment_id":"string","new_slot":"ISO-8601"}
```
**Output**
```json
{"appointment_id":"string","status":"rescheduled"}
```
**Errors**
- `APPT_NOT_FOUND`
- `SLOT_TAKEN`

### 2.4 Cancel Appointment
**Input**
```json
{"appointment_id":"string"}
```
**Output**
```json
{"appointment_id":"string","status":"cancelled"}
```
**Errors**
- `APPT_NOT_FOUND`

## 3. Report Tool
### 3.1 Get Report
**Input**
```json
{"patient_id":"string","report_id":"string|null","report_type":"lab|imaging|note|null"}
```
**Output**
```json
{"report_id":"string","report_type":"string","report_text":"string"}
```
**Errors**
- `REPORT_NOT_FOUND`
- `INVALID_PATIENT`

## 4. Notification Tool
### 4.1 Send SMS
**Input**
```json
{"phone":"+1...","message":"string"}
```
**Output**
```json
{"status":"sent"}
```
**Errors**
- `DELIVERY_FAILED`

## 5. Handoff Tool
### 5.1 Transfer to Human
**Input**
```json
{"reason":"string","context":"string"}
```
**Output**
```json
{"status":"transferred"}
```
**Errors**
- `HUMAN_UNAVAILABLE`

## 6. Error Handling Standard
All tools must return errors using:
```json
{"error":{"code":"STRING","message":"STRING"}}
```

## 7. Retry Strategy
- `SLOT_TAKEN`, `NO_AVAILABILITY`: re-query once
- `DELIVERY_FAILED`: retry once, then log
- `HUMAN_UNAVAILABLE`: fallback to voicemail flow

