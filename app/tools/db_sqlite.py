from __future__ import annotations

import sqlite3
from dataclasses import asdict
from pathlib import Path

from app.graph.state import CollectedFields


class SQLitePatientDB:
    def __init__(self, path: str = "outputs/patient.db") -> None:
        self.path = path
        Path("outputs").mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS patient (
                patient_id TEXT PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                dob TEXT,
                phone TEXT,
                email TEXT
            )
            """
        )
        self.conn.commit()

    def create_patient(self, fields: CollectedFields, phone: str | None) -> str:
        if not fields.first_name or not fields.last_name or not fields.dob:
            raise ValueError("Missing required patient fields")
        patient_id = f"P{abs(hash(fields.first_name + fields.last_name + fields.dob)) % 100000:05d}"
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO patient (patient_id, first_name, last_name, dob, phone, email) VALUES (?, ?, ?, ?, ?, ?)",
            (patient_id, fields.first_name, fields.last_name, fields.dob, phone, fields.email),
        )
        self.conn.commit()
        return patient_id

    def find_patient(self, phone: str | None, dob: str | None) -> str | None:
        if not phone or not dob:
            return None
        cur = self.conn.cursor()
        cur.execute("SELECT patient_id FROM patient WHERE phone = ? AND dob = ?", (phone, dob))
        row = cur.fetchone()
        return row[0] if row else None
