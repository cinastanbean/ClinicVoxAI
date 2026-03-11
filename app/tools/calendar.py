from __future__ import annotations

from typing import List


class CalendarTool:
    def __init__(self) -> None:
        self._appointments = {}
        self._next_id = 100

    def get_available_slots(self) -> List[str]:
        return ["2026-03-12T10:00:00-05:00", "2026-03-12T14:00:00-05:00"]

    def book_appointment(self, patient_id: str, slot: str) -> str:
        appt_id = f"A{self._next_id:05d}"
        self._next_id += 1
        self._appointments[appt_id] = {"patient_id": patient_id, "slot": slot, "status": "confirmed"}
        return appt_id

    def reschedule_appointment(self, appointment_id: str, new_slot: str) -> None:
        if appointment_id in self._appointments:
            self._appointments[appointment_id]["slot"] = new_slot
            self._appointments[appointment_id]["status"] = "rescheduled"

    def cancel_appointment(self, appointment_id: str) -> None:
        if appointment_id in self._appointments:
            self._appointments[appointment_id]["status"] = "cancelled"
