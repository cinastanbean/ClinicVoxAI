from __future__ import annotations

from dataclasses import asdict, fields
from copy import deepcopy
from typing import Dict

from app.graph.state import SessionState


def state_diff(before: SessionState, after: SessionState) -> Dict[str, object]:
    b = asdict(before)
    a = asdict(after)
    return {k: a[k] for k in a.keys() if a[k] != b.get(k)}


def apply_state(target: SessionState, source: SessionState) -> None:
    for field in fields(SessionState):
        value = getattr(source, field.name)
        setattr(target, field.name, deepcopy(value))
