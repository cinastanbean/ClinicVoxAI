from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteReportStore:
    def __init__(self, path: str = "outputs/reports.db") -> None:
        self.path = path
        Path("outputs").mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self._init_schema()

    def _init_schema(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS report (
                report_id TEXT PRIMARY KEY,
                patient_id TEXT,
                text TEXT
            )
            """
        )
        self.conn.commit()

    def seed_report(self, patient_id: str, text: str) -> None:
        report_id = f"R{abs(hash(patient_id + text)) % 100000:05d}"
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO report (report_id, patient_id, text) VALUES (?, ?, ?)",
            (report_id, patient_id, text),
        )
        self.conn.commit()

    def get_latest(self, patient_id: str) -> str | None:
        cur = self.conn.cursor()
        cur.execute("SELECT text FROM report WHERE patient_id = ? LIMIT 1", (patient_id,))
        row = cur.fetchone()
        return row[0] if row else None
