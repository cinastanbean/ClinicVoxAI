from __future__ import annotations

import json
from pathlib import Path

from app.compliance.redaction import redact_phi


class AuditLogger:
    def __init__(self, path: str = "outputs/audit.log") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, event: str, payload: dict) -> None:
        redacted = {k: redact_phi(str(v)) for k, v in payload.items()}
        with self.path.open("a") as f:
            f.write(json.dumps({"event": event, "payload": redacted}) + "\n")
