from __future__ import annotations

import time
from copy import deepcopy
from dataclasses import asdict
from typing import Dict, List

from app.graph.agent_registry import build_agents
from app.graph.recorder import EventRecorder
from app.graph.state import SessionState, CollectedFields, AppointmentContext, ReportContext
from app.graph.utils import apply_state, state_diff
from app.graph.langgraph_flow import LangGraphOrchestrator


class LangGraphRuntime:
    def __init__(self) -> None:
        self.agents = build_agents()
        self.recorder = EventRecorder()
        self.graph = LangGraphOrchestrator(
            self.agents["router"], self.agents["supervisor"], self.agents["task"]
        ).build()

    def _record_diff(self, agent: str, before: SessionState, after: SessionState) -> None:
        diff = state_diff(before, after)
        if diff:
            self.recorder.record_event("state_diff", {"agent": agent, "diff": diff})

    def _coerce_state(self, state: SessionState | dict) -> SessionState:
        if isinstance(state, SessionState):
            return state
        # Convert nested dicts back to dataclasses
        if isinstance(state.get("collected_fields"), dict):
            state["collected_fields"] = CollectedFields(**state["collected_fields"])
        if isinstance(state.get("appointment_context"), dict):
            state["appointment_context"] = AppointmentContext(**state["appointment_context"])
        if isinstance(state.get("report_context"), dict):
            state["report_context"] = ReportContext(**state["report_context"])
        return SessionState(**state)

    def handle_turn(self, state: SessionState, text: str) -> Dict:
        state.turn_id += 1
        self.recorder.record_event("turn_start", {"turn_id": state.turn_id, "text": text})
        state.meta["text"] = text

        before = deepcopy(state)
        t0 = time.perf_counter()
        new_state = self._coerce_state(self.graph.invoke(state))
        dur = (time.perf_counter() - t0) * 1000
        self.recorder.record_event("node_duration", {"agent": "langgraph", "ms": round(dur, 3)})

        # Mutate original state so callers see updates
        apply_state(state, new_state)

        self._record_diff("langgraph", before, state)
        response = state.meta.get("last_response")
        if response:
            self.recorder.record_event("task_response", {"response": response})
        self.recorder.record_state(state)
        return {"state": state, "response": response}

    def new_state(self, session_id: str, caller_phone: str | None = None) -> SessionState:
        return SessionState(session_id=session_id, caller_phone=caller_phone)

    def simulate_call(self, transcript: List[str], session_id: str, caller_phone: str | None = None) -> Dict:
        state = SessionState(session_id=session_id, caller_phone=caller_phone)
        responses = []
        for text in transcript:
            result = self.handle_turn(state, text)
            responses.append(result["response"])
        return {"state": asdict(state), "responses": responses, "trace": self.recorder.export()}
