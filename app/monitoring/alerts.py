from __future__ import annotations

from app.compliance.audit import AuditLogger


def send_alert(message: str) -> None:
    audit = AuditLogger()
    audit.write("alert", {"message": message})
    print(f"[ALERT] {message}")
