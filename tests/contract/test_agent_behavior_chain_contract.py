from __future__ import annotations

# [Task]: T009 [From]: specs/014-agent-behavior-validation/spec.md User Story 2

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime, chat_model_factory
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
)


def test_behavior_chain_instructions_include_rules(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "list_tasks", '{"status":"all"}')],
            )
        ),
        build_response(build_message(content="Which task should I delete?")),
    ]

    async def _fake_request_completion(*, client, model_name, messages, tool_specs):
        system_content = messages[0]["content"]
        assert "list_tasks -> delete_task" in system_content
        assert "list_tasks -> complete_task" in system_content
        assert "list_tasks -> update_task" in system_content
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

    headers = auth_headers_factory("behavior-chain-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Delete the meeting task"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        assert payload.get("tool_calls")
