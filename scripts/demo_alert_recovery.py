from __future__ import annotations

from app.resilience import CircuitBreaker, RetryPolicy, call_with_retry
from app.monitoring.alerts import send_alert


def run() -> None:
    breaker = CircuitBreaker(failure_threshold=2, reset_after=1.0)
    policy = RetryPolicy(attempts=2, delay_seconds=0.01)

    def failing_call():
        raise RuntimeError("simulated failure")

    for _ in range(3):
        try:
            call_with_retry(failing_call, policy, breaker)
        except Exception:
            send_alert("tool_failed_after_retries")


if __name__ == "__main__":
    run()
