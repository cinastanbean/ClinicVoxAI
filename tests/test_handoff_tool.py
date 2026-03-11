from __future__ import annotations

from app.tools.handoff import HandoffTool


def test_handoff_tool_noop() -> None:
    tool = HandoffTool()
    tool.transfer("verification_failed")
