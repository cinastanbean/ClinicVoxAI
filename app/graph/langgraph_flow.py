from __future__ import annotations

try:
    from langgraph.graph import StateGraph
except Exception as exc:  # noqa: BLE001
    StateGraph = None
    _import_error = exc

from app.graph.state import SessionState, CollectedFields, AppointmentContext, ReportContext


def _coerce(state: SessionState | dict) -> SessionState:
    if isinstance(state, SessionState):
        if isinstance(state.collected_fields, dict):
            state.collected_fields = CollectedFields(**state.collected_fields)
        if isinstance(state.appointment_context, dict):
            state.appointment_context = AppointmentContext(**state.appointment_context)
        if isinstance(state.report_context, dict):
            state.report_context = ReportContext(**state.report_context)
        return state
    if isinstance(state.get("collected_fields"), dict):
        state["collected_fields"] = CollectedFields(**state["collected_fields"])
    if isinstance(state.get("appointment_context"), dict):
        state["appointment_context"] = AppointmentContext(**state["appointment_context"])
    if isinstance(state.get("report_context"), dict):
        state["report_context"] = ReportContext(**state["report_context"])
    return SessionState(**state)


class LangGraphOrchestrator:
    def __init__(self, router, supervisor, task) -> None:
        self.router = router
        self.supervisor = supervisor
        self.task = task

    def build(self):
        if StateGraph is None:
            raise RuntimeError(f"LangGraph not installed: {_import_error}")

        graph = StateGraph(SessionState)

        def router_node(state: SessionState | dict) -> SessionState:
            state = _coerce(state)
            return self.router.handle(state, state.meta.get("text", ""))

        def supervisor_node(state: SessionState | dict) -> SessionState:
            state = _coerce(state)
            state = self.supervisor.handle(state)
            decision = self.supervisor.decide(state)
            state.meta["decision"] = decision
            if decision == "clarify":
                state.meta["last_response"] = (
                    "I want to make sure I understood. Are you calling to schedule, change, or discuss a report?"
                )
            if decision == "handoff":
                state.meta["last_response"] = "Let me connect you to a person."
            return state

        def task_node(state: SessionState | dict) -> SessionState:
            state = _coerce(state)
            response = self.task.handle(state, state.meta.get("text", ""))
            state.meta["last_response"] = response
            return state

        graph.add_node("router", router_node)
        graph.add_node("supervisor", supervisor_node)
        graph.add_node("task", task_node)
        graph.set_entry_point("router")
        graph.add_edge("router", "supervisor")

        def route_decision(state: SessionState | dict) -> str:
            state = _coerce(state)
            decision = state.meta.get("decision") or self.supervisor.decide(state)
            if decision == "handoff":
                return "__end__"
            if decision == "clarify":
                count = state.meta.get("clarify_count", 0) + 1
                state.meta["clarify_count"] = count
                if count >= 2:
                    return "__end__"
                return "router"
            return "task"

        graph.add_conditional_edges("supervisor", route_decision)
        graph.add_edge("task", "__end__")
        return graph.compile()
