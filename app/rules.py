from __future__ import annotations

INTENT_KEYWORDS = {
    "cancel": ["cancel", "call off"],
    "reschedule": ["reschedule", "move", "change"],
    "schedule": ["schedule", "appointment", "book"],
    "report": ["report", "results", "lab"],
    "insurance": ["insurance"],
    "medication": ["medication", "meds"],
    "registration": ["register", "sign up"],
}

PATIENT_TYPE_KEYWORDS = {
    "new": ["new", "first", "register"],
    "existing": ["last", "again", "existing"],
}
