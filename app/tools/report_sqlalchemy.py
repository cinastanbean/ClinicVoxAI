from __future__ import annotations

import os

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class Report(Base):
    __tablename__ = "report"
    report_id = Column(String, primary_key=True)
    patient_id = Column(String)
    text = Column(String)


class SQLAlchemyReportStore:
    def __init__(self) -> None:
        url = os.getenv("REPORT_DB_URL", "sqlite:///outputs/report_sa.db")
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def seed_report(self, patient_id: str, text: str) -> None:
        report_id = f"R{abs(hash(patient_id + text)) % 100000:05d}"
        with self.Session() as session:
            session.merge(Report(report_id=report_id, patient_id=patient_id, text=text))
            session.commit()

    def get_latest(self, patient_id: str) -> str | None:
        with self.Session() as session:
            row = session.query(Report).filter_by(patient_id=patient_id).first()
            return row.text if row else None
