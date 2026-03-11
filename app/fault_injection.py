from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FaultConfig:
    fail_db: bool = False
    fail_calendar: bool = False
    fail_notify: bool = False


FAULTS = FaultConfig()
