from __future__ import annotations

from app.graph.agent_registry import build_agents
from app.graph.langgraph_flow import LangGraphOrchestrator
from app.graph.state import SessionState


def run() -> None:
    agents = build_agents()
    lg = LangGraphOrchestrator(agents["router"], agents["supervisor"], agents["task"]).build()

    state = SessionState(session_id="LG-1")
    for text in [
        "I want to schedule an appointment",
        "My first name is Jane",
        "My last name is Doe",
        "My date of birth is 1990-01-01",
        "Wednesday morning works",
    ]:
        state.meta["text"] = text
        state = lg.invoke(state)
        print("Turn:", text)
        print("Intent:", state.intent)
        print("Last agent:", state.last_agent)
        print("-")


if __name__ == "__main__":
    run()
