from __future__ import annotations

import re
from typing import Optional

from app.config import CONFIG
from app.fault_injection import FAULTS
from app.graph.state import SessionState, append_error
from app.llm.mock import MockLLM
from app.llm.openai_client import OpenAIReportSummarizer
from app.monitoring.alerts import send_alert
from app.tools.calendar import CalendarTool
from app.tools.calendar_sqlalchemy import SQLAlchemyCalendar
from app.tools.calendar_sqlite import SQLiteCalendar
from app.tools.db import PatientDBTool
from app.tools.db_sqlalchemy import SQLAlchemyPatientDB
from app.tools.db_sqlite import SQLitePatientDB
from app.tools.faulty import maybe_fail_calendar, maybe_fail_db, maybe_fail_notify
from app.tools.notifications import NotificationTool
from app.tools.report_sqlalchemy import SQLAlchemyReportStore
from app.tools.report_store import SQLiteReportStore
from app.tools.reports import ReportTool
from app.tools.resilient import ResilientCall
from app.tools.verification import VerificationTool


class TaskAgent:
    name = "task"

    def __init__(
        self,
        db: PatientDBTool | SQLitePatientDB | SQLAlchemyPatientDB,
        calendar: CalendarTool | SQLiteCalendar | SQLAlchemyCalendar,
        reports: ReportTool | SQLiteReportStore | SQLAlchemyReportStore,
        notify: NotificationTool,
        verifier: VerificationTool,
        llm: MockLLM | None = None,
    ) -> None:
        self.db = db
        self.calendar = calendar
        self.reports = reports
        self.notify = notify
        self.verifier = verifier
        self.llm = llm or MockLLM()
        self.resilient = ResilientCall()
        self.openai_summarizer = OpenAIReportSummarizer() if CONFIG.use_openai_llm else None

    def handle(self, state: SessionState, text: str) -> str:
        state.last_agent = self.name
        self._extract_fields(state, text)

        if state.intent in {"registration", "schedule"}:
            return self._handle_registration_or_schedule(state)
        if state.intent in {"reschedule", "cancel"}:
            return self._handle_modify(state)
        if state.intent == "report":
            return self._handle_report(state)
        if CONFIG.task_use_llm_draft:
            return self.llm.draft_response(state.intent, {"verified": state.verification_status})
        return "I can help with scheduling, registration, or reports. Which would you like?"

    def _handle_registration_or_schedule(self, state: SessionState) -> str:
        fields = state.collected_fields
        missing = []
        if not fields.first_name:
            missing.append("first name")
        if not fields.last_name:
            missing.append("last name")
        if not fields.dob:
            missing.append("date of birth")

        if missing:
            return f"Please tell me your {', '.join(missing)}."

        if not state.patient_id:
            try:
                if FAULTS.fail_db:
                    maybe_fail_db()
                if isinstance(self.db, (SQLitePatientDB, SQLAlchemyPatientDB)):
                    state.patient_id = self.resilient.call(
                        "db.create_patient",
                        lambda: self.db.create_patient(fields, state.caller_phone),
                    )
                    if isinstance(self.reports, (SQLiteReportStore, SQLAlchemyReportStore)):
                        self.reports.seed_report(
                            state.patient_id,
                            "Impression: Mild degenerative changes in L4-L5. No acute findings.",
                        )
                else:
                    state.patient_id = self.resilient.call(
                        "db.create_patient",
                        lambda: self.db.create_patient(fields),
                    )
            except Exception as exc:  # noqa: BLE001
                send_alert("db_create_patient_failed")
                append_error(state, "tool", "DB_ERROR", str(exc))
                return "I had trouble saving your information. Let me connect you to a person."

        if not state.appointment_context.selected_slot:
            try:
                if FAULTS.fail_calendar:
                    maybe_fail_calendar()
                slots = self.resilient.call("calendar.get_slots", self.calendar.get_available_slots)
            except Exception as exc:  # noqa: BLE001
                send_alert("calendar_get_slots_failed")
                append_error(state, "tool", "CALENDAR_ERROR", str(exc))
                return "I'm having trouble accessing the schedule. Let me connect you to a person."
            if not slots:
                return "I do not see any available times right now. Would you like me to transfer you to a person?"
            state.appointment_context.slot_candidates = slots
            if len(slots) == 1:
                return f"I have {slots[0]} available. Does that work for you?"
            return f"I have {slots[0]} or {slots[1]}. Which works for you?"

        try:
            if FAULTS.fail_calendar:
                maybe_fail_calendar()
            if isinstance(self.calendar, (SQLiteCalendar, SQLAlchemyCalendar)):
                appt_id = self.resilient.call(
                    "calendar.book",
                    lambda: self.calendar.book(state.patient_id, state.appointment_context.selected_slot),
                )
            else:
                appt_id = self.resilient.call(
                    "calendar.book",
                    lambda: self.calendar.book_appointment(state.patient_id, state.appointment_context.selected_slot),
                )
            state.appointment_context.appointment_id = appt_id
        except Exception as exc:  # noqa: BLE001
            send_alert("calendar_book_failed")
            append_error(state, "tool", "CALENDAR_ERROR", str(exc))
            return "I'm having trouble booking. Let me connect you to a person."

        try:
            if FAULTS.fail_notify:
                maybe_fail_notify()
            self.resilient.call(
                "notify.sms",
                lambda: self.notify.send_sms(
                    state.caller_phone,
                    f"Your appointment is confirmed for {state.appointment_context.selected_slot}.",
                ),
            )
        except Exception as exc:  # noqa: BLE001
            send_alert("notify_sms_failed")
            append_error(state, "tool", "NOTIFY_ERROR", str(exc))
        return "You're all set. I have confirmed your appointment and sent a text message."

    def _handle_modify(self, state: SessionState) -> str:
        verified = self._ensure_verified(state)
        if not verified and state.verification_status == "failed" and state.intent == "cancel":
            return "Please provide your appointment ID so I can update it."
        if not verified:
            return "Please provide your date of birth so I can verify your identity."
        if not state.appointment_context.appointment_id:
            return "Please provide your appointment ID so I can update it."
        if state.intent == "cancel":
            self.calendar.cancel_appointment(state.appointment_context.appointment_id)
            return "Your appointment has been cancelled."
        if not state.appointment_context.selected_slot:
            slots = self.calendar.get_available_slots()
            state.appointment_context.slot_candidates = slots
            return f"I can move you to {slots[0]} or {slots[1]}. Which do you prefer?"
        self.calendar.reschedule_appointment(
            state.appointment_context.appointment_id, state.appointment_context.selected_slot
        )
        return "Your appointment has been rescheduled."

    def _handle_report(self, state: SessionState) -> str:
        if not self._ensure_verified(state):
            return "Please provide your date of birth so I can verify your identity."
        if isinstance(self.reports, (SQLiteReportStore, SQLAlchemyReportStore)):
            report = self.resilient.call("report.get", lambda: self.reports.get_latest(state.patient_id))
            if not report:
                self.reports.seed_report(
                    state.patient_id,
                    "Impression: Mild degenerative changes in L4-L5. No acute findings.",
                )
                report = self.reports.get_latest(state.patient_id)
        else:
            report = self.resilient.call(
                "report.get", lambda: self.reports.get_latest_report(state.patient_id)
            )
        if not report:
            return "I could not find a report. Would you like to speak with a person?"
        state.report_context.report_text = report
        summary = (
            self.openai_summarizer.summarize(report)
            if self.openai_summarizer is not None
            else self.llm.summarize_report(report)
        )
        return (
            "Here is a plain-language summary: "
            + summary
            + " If you want advice, I can connect you to a clinician."
        )

    def _ensure_verified(self, state: SessionState) -> bool:
        if state.verification_status == "verified":
            return True
        if state.verification_attempts >= CONFIG.max_verification_attempts:
            state.handoff_reason = "verification_failed"
            return False
        patient_id = self.verifier.verify(state.caller_phone, state.collected_fields.dob)
        state.verification_attempts += 1
        if patient_id:
            state.patient_id = patient_id
            state.verification_status = "verified"
            return True
        state.verification_status = "failed"
        return False

    def _extract_fields(self, state: SessionState, text: str) -> None:
        t = text.strip()
        fields = state.collected_fields

        match = re.search(r"first name is\s+(\w+)", t, re.IGNORECASE)
        if match and not fields.first_name:
            fields.first_name = match.group(1)

        match = re.search(r"last name is\s+(\w+)", t, re.IGNORECASE)
        if match and not fields.last_name:
            fields.last_name = match.group(1)

        match = re.search(r"name is\s+(\w+)\s+(\w+)", t, re.IGNORECASE)
        if match:
            if not fields.first_name:
                fields.first_name = match.group(1)
            if not fields.last_name:
                fields.last_name = match.group(2)

        match = re.search(r"(\d{4}-\d{2}-\d{2})", t)
        if match and not fields.dob:
            fields.dob = match.group(1)

        if state.appointment_context.slot_candidates and not state.appointment_context.selected_slot:
            if re.search(r"morning|10", t, re.IGNORECASE):
                state.appointment_context.selected_slot = state.appointment_context.slot_candidates[0]
            elif re.search(r"afternoon|2", t, re.IGNORECASE) and len(state.appointment_context.slot_candidates) > 1:
                state.appointment_context.selected_slot = state.appointment_context.slot_candidates[1]

    def update_field(self, state: SessionState, field: str, value: str) -> Optional[str]:
        if hasattr(state.collected_fields, field):
            setattr(state.collected_fields, field, value)
            return None
        return "unknown_field"
