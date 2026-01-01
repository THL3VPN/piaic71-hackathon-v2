from __future__ import annotations

# [Task]: T005 [From]: specs/014-agent-behavior-validation/spec.md User Story 1

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime, chat_model_factory
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
)


def test_behavior_list_instructions_include_status_mapping(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "list_tasks", '{"status":"pending"}')],
            )
        ),
        build_response(build_message(content="Here are your tasks")),
    ]

    async def _fake_request_completion(*, client, model_name, messages, tool_specs):
        system_content = messages[0]["content"]
        assert "list_tasks" in system_content
        assert "pending" in system_content
        assert "completed" in system_content
        assert "all" in system_content
        return responses.pop(0)

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

    headers = auth_headers_factory("behavior-list-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "What's pending?"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        assert payload.get("tool_calls")
