from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from typing import Dict, Iterable, List, Tuple

from app.graph.state import SessionState


def diff_top_level(before: SessionState, after: SessionState) -> Dict[str, object]:
    b = asdict(before)
    a = asdict(after)
    changed: Dict[str, object] = {}
    for key in a.keys():
        if a[key] != b.get(key):
            changed[key] = a[key]
    return changed


def merge_states(
    base: SessionState,
    branches: List[Tuple[str, SessionState]],
    priority: Iterable[str],
) -> Tuple[SessionState, List[Dict[str, object]]]:
    priority_list = list(priority)
    base_copy = deepcopy(base)

    diffs: Dict[str, Dict[str, object]] = {}
    for name, branch_state in branches:
        diffs[name] = diff_top_level(base, branch_state)

    conflicts = []
    applied = set()

    for field in set().union(*[set(d.keys()) for d in diffs.values()]):
        values = {name: diff.get(field) for name, diff in diffs.items() if field in diff}
        if len(values) <= 1:
            for name, value in values.items():
                setattr(base_copy, field, value)
                applied.add(field)
            continue

        unique_vals = {repr(v) for v in values.values()}
        if len(unique_vals) == 1:
            chosen = next(iter(values.values()))
            setattr(base_copy, field, chosen)
            applied.add(field)
        else:
            conflicts.append({"field": field, "values": values})
            for name in priority_list:
                if name in values:
                    setattr(base_copy, field, values[name])
                    applied.add(field)
                    break

    return base_copy, conflicts
