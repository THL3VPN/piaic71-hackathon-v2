from __future__ import annotations

# [Task]: T015 [From]: specs/015-mcp-server-extraction/tasks.md User Story 3

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime, mcp_client
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
    stub_agent_responses,
)


def test_chat_mcp_ownership_returns_not_found(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "complete_task", '{"task_id":123}')],
            )
        ),
        build_response(build_message(content="Done")),
    ]

    stub_agent_responses(monkeypatch, responses)

    async def _fake_dispatch(name: str, args: dict[str, object], user_id: str):
        raise mcp_client.McpClientError("Task not found")

    monkeypatch.setattr(agent_runtime, "_dispatch_mcp_tool", _fake_dispatch)

    headers = auth_headers_factory("intruder-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Complete task 123"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        tool_calls = payload.get("tool_calls")
        assert tool_calls
        assert "error" in tool_calls[0].get("result", {})
        assert "not found" in str(tool_calls[0]["result"]["error"]).lower()
