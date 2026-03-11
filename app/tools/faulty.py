from __future__ import annotations

from app.fault_injection import FAULTS


def maybe_fail_db() -> None:
    if FAULTS.fail_db:
        raise RuntimeError("fault:db")


def maybe_fail_calendar() -> None:
    if FAULTS.fail_calendar:
        raise RuntimeError("fault:calendar")


def maybe_fail_notify() -> None:
    if FAULTS.fail_notify:
        raise RuntimeError("fault:notify")
