from __future__ import annotations

from typing import Dict

from app.agents.audit import AuditAgent
from app.agents.context import ContextAgent
from app.agents.router import RouterAgent
from app.agents.supervisor import SupervisorAgent
from app.agents.task import TaskAgent
from app.config import CONFIG
from app.tools.calendar import CalendarTool
from app.tools.calendar_sqlalchemy import SQLAlchemyCalendar
from app.tools.calendar_sqlite import SQLiteCalendar
from app.tools.db import PatientDBTool
from app.tools.db_sqlalchemy import SQLAlchemyPatientDB
from app.tools.db_sqlite import SQLitePatientDB
from app.tools.notifications import NotificationTool
from app.tools.report_sqlalchemy import SQLAlchemyReportStore
from app.tools.report_store import SQLiteReportStore
from app.tools.reports import ReportTool
from app.tools.verification import VerificationTool


def build_agents() -> Dict[str, object]:
    if CONFIG.storage_backend == "sqlalchemy":
        db = SQLAlchemyPatientDB()
        calendar = SQLAlchemyCalendar()
        reports = SQLAlchemyReportStore()
        reports.seed_report("P00001", "Impression: Mild degenerative changes in L4-L5. No acute findings.")
    elif CONFIG.storage_backend == "sqlite":
        db = SQLitePatientDB()
        calendar = SQLiteCalendar()
        reports = SQLiteReportStore()
        reports.seed_report("P00001", "Impression: Mild degenerative changes in L4-L5. No acute findings.")
    else:
        db = PatientDBTool()
        calendar = CalendarTool()
        reports = ReportTool()

    return {
        "router": RouterAgent(),
        "supervisor": SupervisorAgent(),
        "task": TaskAgent(
            db=db,
            calendar=calendar,
            reports=reports,
            notify=NotificationTool(),
            verifier=VerificationTool(db),
        ),
        "context": ContextAgent(),
        "audit": AuditAgent(),
    }
