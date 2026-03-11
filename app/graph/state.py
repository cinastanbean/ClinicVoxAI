from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ErrorEntry:
    source: str
    code: str
    message: str


@dataclass
class AppointmentContext:
    provider_id: Optional[str] = None
    department: Optional[str] = None
    slot_candidates: List[str] = field(default_factory=list)
    selected_slot: Optional[str] = None
    appointment_id: Optional[str] = None
    version: int = 0


@dataclass
class ReportContext:
    report_id: Optional[str] = None
    report_type: Optional[str] = None
    report_text: Optional[str] = None
    summary: Optional[str] = None
    version: int = 0


@dataclass
class CollectedFields:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[str] = None
    email: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_member_id: Optional[str] = None
    reason_for_visit: Optional[str] = None


@dataclass
class SessionState:
    session_id: str
    turn_id: int = 0
    caller_phone: Optional[str] = None
    patient_id: Optional[str] = None
    patient_type: str = "unknown"
    intent: str = "unknown"
    intent_confidence: float = 0.0
    verification_status: str = "unverified"
    verification_attempts: int = 0
    collected_fields: CollectedFields = field(default_factory=CollectedFields)
    appointment_context: AppointmentContext = field(default_factory=AppointmentContext)
    report_context: ReportContext = field(default_factory=ReportContext)
    handoff_reason: Optional[str] = None
    last_agent: str = ""
    errors: List[ErrorEntry] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


def reset_context_on_intent_change(state: SessionState, new_intent: str) -> None:
    if new_intent != state.intent:
        state.appointment_context = AppointmentContext(
            version=state.appointment_context.version + 1
        )
        state.report_context = ReportContext(
            version=state.report_context.version + 1
        )


def append_error(state: SessionState, source: str, code: str, message: str) -> None:
    state.errors.append(ErrorEntry(source=source, code=code, message=message))
