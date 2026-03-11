from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Callable, TypeVar

from app.monitoring.alerts import send_alert


T = TypeVar("T")


@dataclass
class RetryPolicy:
    attempts: int = 2
    delay_seconds: float = 0.1


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 2, reset_after: float = 5.0) -> None:
        self.failure_threshold = failure_threshold
        self.reset_after = reset_after
        self.failures = 0
        self.opened_at: float | None = None

    def allow(self) -> bool:
        if self.opened_at is None:
            return True
        if time.time() - self.opened_at >= self.reset_after:
            self.failures = 0
            self.opened_at = None
            return True
        return False

    def record_success(self) -> None:
        self.failures = 0
        self.opened_at = None

    def record_failure(self) -> None:
        self.failures += 1
        if self.failures >= self.failure_threshold:
            self.opened_at = time.time()
            send_alert("Circuit opened due to repeated failures")


def call_with_retry(fn: Callable[[], T], policy: RetryPolicy, breaker: CircuitBreaker) -> T:
    if not breaker.allow():
        raise RuntimeError("circuit_open")
    last_exc: Exception | None = None
    for _ in range(policy.attempts):
        try:
            result = fn()
            breaker.record_success()
            return result
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            breaker.record_failure()
            time.sleep(policy.delay_seconds)
    raise last_exc or RuntimeError("unknown_error")
