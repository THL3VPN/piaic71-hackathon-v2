from __future__ import annotations

# [Task]: T009 [From]: specs/015-mcp-server-extraction/spec.md User Story 2

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime, chat_model_factory, mcp_client
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
)


def test_chat_tool_calls_reflect_mcp_results(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "add_task", '{"title":"Buy milk"}')],
            )
        ),
        build_response(build_message(content="Done")),
    ]

    async def _fake_request_completion(*, client, model_name, messages, tool_specs):
        return responses.pop(0)

    async def _fake_add_task(*, user_id: str, title: str, description: str | None = None):
        return {"task_id": 1, "status": "created", "title": title}

    monkeypatch.setattr(agent_runtime, "_request_completion", _fake_request_completion)
    monkeypatch.setattr(
        agent_runtime,
        "build_chat_model",
        lambda settings: chat_model_factory.ChatModel(
            provider="openai",
            model_name="gpt-test",
            client=object(),
        ),
    )
    monkeypatch.setattr(mcp_client, "call_add_task", _fake_add_task)

    headers = auth_headers_factory("mcp-contract-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Add a task to buy milk"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        tool_calls = payload.get("tool_calls")
        assert tool_calls
        assert tool_calls[0]["name"] == "add_task"
        assert tool_calls[0]["result"]["status"] == "created"
