from __future__ import annotations

from dataclasses import asdict
from typing import Dict

from app.graph.state import CollectedFields


class PatientDBTool:
    def __init__(self) -> None:
        self._patients: Dict[str, Dict] = {}
        self._next_id = 1

    def create_patient(self, fields: CollectedFields) -> str:
        if not fields.first_name or not fields.last_name or not fields.dob:
            raise ValueError("Missing required patient fields")
        patient_id = f"P{self._next_id:05d}"
        self._next_id += 1
        self._patients[patient_id] = asdict(fields)
        return patient_id

    def find_patient(self, phone: str, dob: str) -> str | None:
        for pid, data in self._patients.items():
            if data.get("dob") == dob:
                return pid
        return None
