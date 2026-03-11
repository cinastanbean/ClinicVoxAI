from __future__ import annotations

import os
from dataclasses import asdict

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.graph.state import CollectedFields


Base = declarative_base()


class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    dob = Column(String)
    phone = Column(String)
    email = Column(String)


class SQLAlchemyPatientDB:
    def __init__(self) -> None:
        url = os.getenv("DATABASE_URL", "sqlite:///outputs/patient_sa.db")
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_patient(self, fields: CollectedFields, phone: str | None) -> str:
        if not fields.first_name or not fields.last_name or not fields.dob:
            raise ValueError("Missing required patient fields")
        patient_id = f"P{abs(hash(fields.first_name + fields.last_name + fields.dob)) % 100000:05d}"
        with self.Session() as session:
            session.merge(
                Patient(
                    patient_id=patient_id,
                    first_name=fields.first_name,
                    last_name=fields.last_name,
                    dob=fields.dob,
                    phone=phone,
                    email=fields.email,
                )
            )
            session.commit()
        return patient_id

    def find_patient(self, phone: str | None, dob: str | None) -> str | None:
        if not phone or not dob:
            return None
        with self.Session() as session:
            row = session.query(Patient).filter_by(phone=phone, dob=dob).first()
            return row.patient_id if row else None
