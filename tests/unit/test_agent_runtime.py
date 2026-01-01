from __future__ import annotations

# [Task]: T007 [From]: specs/012-ai-agent-integration/spec.md User Story 1

import pytest

from src.services import agent_runtime


@pytest.mark.anyio
async def test_agent_runtime_returns_response_and_tool_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _stub_execute_agent(*, user_message, history, user_id, model, system_instructions, session):
        return agent_runtime.AgentResult(response="ok", tool_calls=[])

    monkeypatch.setattr(agent_runtime, "build_chat_model", lambda settings: object())
    monkeypatch.setattr(agent_runtime, "_execute_agent", _stub_execute_agent)

    result = await agent_runtime.run_agent(
        user_message="Add a task",
        history=[],
        user_id="user-1",
        session=object(),
    )

    assert isinstance(result.response, str)
    assert isinstance(result.tool_calls, list)
