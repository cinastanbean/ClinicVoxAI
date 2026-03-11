from __future__ import annotations

from typing import Any, Dict

from app.config import CONFIG


def log_event(event: str, payload: Dict[str, Any]) -> None:
    if not CONFIG.log_events:
        return
    print(f"[event={event}] {payload}")
