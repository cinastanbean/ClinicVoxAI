from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, Set

from app.graph.state import SessionState


AGENT_OWNERSHIP: Dict[str, Set[str]] = {
    "router": {"patient_type", "intent", "intent_confidence", "last_agent"},
    "supervisor": {"handoff_reason", "last_agent"},
    "task": {
        "patient_id",
        "verification_status",
        "verification_attempts",
        "collected_fields",
        "appointment_context",
        "report_context",
        "last_agent",
    },
    "context": {"meta", "last_agent"},
    "audit": {"meta", "last_agent"},
}


def diff_state(before: SessionState, after: SessionState) -> Set[str]:
    b = asdict(before)
    a = asdict(after)
    changed = set()
    for key in a.keys():
        if a[key] != b.get(key):
            changed.add(key)
    return changed


def validate_ownership(agent: str, changed_fields: Iterable[str]) -> list[str]:
    allowed = AGENT_OWNERSHIP.get(agent, set())
    violations = [f for f in changed_fields if f not in allowed and f not in {"turn_id"}]
    return violations
