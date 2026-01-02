from __future__ import annotations

# [Task]: T013 [From]: specs/014-agent-behavior-validation/spec.md User Story 3

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime, chat_model_factory
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
)


def test_behavior_error_instructions_include_task_not_found(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "complete_task", '{"task_id":9999}')],
            )
        ),
        build_response(build_message(content="I couldn't find that task.")),
    ]

    async def _fake_request_completion(*, client, model_name, messages, tool_specs):
        system_content = messages[0]["content"].lower()
        assert "task not found" in system_content
        assert "suggest" in system_content
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

    headers = auth_headers_factory("behavior-error-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Mark task 9999 as complete"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        assert payload.get("tool_calls")
