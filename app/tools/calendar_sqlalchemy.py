from __future__ import annotations

import os

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class Appointment(Base):
    __tablename__ = "appointment"
    appointment_id = Column(String, primary_key=True)
    patient_id = Column(String)
    slot = Column(String)
    status = Column(String)


class SQLAlchemyCalendar:
    def __init__(self) -> None:
        url = os.getenv("CALENDAR_DB_URL", "sqlite:///outputs/calendar_sa.db")
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_available_slots(self):
        return ["2026-03-12T10:00:00-05:00", "2026-03-12T14:00:00-05:00"]

    def book(self, patient_id: str, slot: str) -> str:
        appointment_id = f"A{abs(hash(patient_id + slot)) % 100000:05d}"
        with self.Session() as session:
            session.merge(
                Appointment(
                    appointment_id=appointment_id,
                    patient_id=patient_id,
                    slot=slot,
                    status="confirmed",
                )
            )
            session.commit()
        return appointment_id

    def reschedule_appointment(self, appointment_id: str, new_slot: str) -> None:
        with self.Session() as session:
            row = session.query(Appointment).filter_by(appointment_id=appointment_id).first()
            if row:
                row.slot = new_slot
                row.status = "rescheduled"
                session.commit()

    def cancel_appointment(self, appointment_id: str) -> None:
        with self.Session() as session:
            row = session.query(Appointment).filter_by(appointment_id=appointment_id).first()
            if row:
                row.status = "cancelled"
                session.commit()
