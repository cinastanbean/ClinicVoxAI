from __future__ import annotations

from app.tools.db import PatientDBTool


class VerificationTool:
    def __init__(self, db: PatientDBTool) -> None:
        self.db = db

    def verify(self, phone: str | None, dob: str | None) -> str | None:
        if not phone or not dob:
            return None
        return self.db.find_patient(phone, dob)
