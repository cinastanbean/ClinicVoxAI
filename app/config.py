from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AppConfig:
    router_backend: str = "rules"  # rules | llm | openai
    supervisor_low_confidence_threshold: float = 0.5
    supervisor_max_errors: int = 2
    max_verification_attempts: int = 2
    enable_parallel_demo: bool = False
    enable_parallel_async: bool = False
    use_langgraph: bool = False
    log_events: bool = True
    storage_backend: str = "sqlite"  # sqlite | sqlalchemy | memory
    task_use_llm_draft: bool = True
    use_openai_llm: bool = False


CONFIG = AppConfig()
