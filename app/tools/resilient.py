from __future__ import annotations

from typing import Callable, Dict, TypeVar

from app.resilience import CircuitBreaker, RetryPolicy, call_with_retry


T = TypeVar("T")


class ResilientCall:
    def __init__(self) -> None:
        self.breakers: Dict[str, CircuitBreaker] = {}
        self.policy = RetryPolicy()

    def _breaker(self, name: str) -> CircuitBreaker:
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker()
        return self.breakers[name]

    def call(self, name: str, fn: Callable[[], T]) -> T:
        return call_with_retry(fn, self.policy, self._breaker(name))
