from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List


class SQLiteCalendar:
    def __init__(self, path: str = "outputs/calendar.db") -> None:
        self.path = path
        Path("outputs").mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS appointment (
                appointment_id TEXT PRIMARY KEY,
                patient_id TEXT,
                slot TEXT,
                status TEXT
            )
            """
        )
        self.conn.commit()

    def get_available_slots(self) -> List[str]:
        return ["2026-03-12T10:00:00-05:00", "2026-03-12T14:00:00-05:00"]

    def book(self, patient_id: str, slot: str) -> str:
        appointment_id = f"A{abs(hash(patient_id + slot)) % 100000:05d}"
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO appointment (appointment_id, patient_id, slot, status) VALUES (?, ?, ?, ?)",
            (appointment_id, patient_id, slot, "confirmed"),
        )
        self.conn.commit()
        return appointment_id
