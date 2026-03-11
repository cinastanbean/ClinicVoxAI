from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from app.graph.state import SessionState


class EventRecorder:
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []
        self.snapshots: List[Dict[str, Any]] = []

    def record_event(self, event: str, payload: Dict[str, Any]) -> None:
        self.events.append({"event": event, **payload})

    def record_state(self, state: SessionState) -> None:
        self.snapshots.append(asdict(state))

    def export(self) -> Dict[str, Any]:
        return {"events": self.events, "snapshots": self.snapshots}
