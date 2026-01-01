from __future__ import annotations

# [Task]: T006 [From]: specs/014-agent-behavior-validation/spec.md User Story 1

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
    stub_agent_responses,
)


def test_behavior_add_and_list(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "add_task", '{"title":"buy groceries"}')],
            )
        ),
        build_response(build_message(content="Added.")),
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-2", "list_tasks", '{"status":"all"}')],
            )
        ),
        build_response(build_message(content="Here are your tasks.")),
    ]

    stub_agent_responses(monkeypatch, responses)

    headers = auth_headers_factory("behavior-add-list-user")
    with TestClient(app) as client:
        add_resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Add a task to buy groceries"},
        )
        assert add_resp.status_code == 200
        assert add_resp.json().get("tool_calls")

        list_resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Show me all my tasks"},
        )
        assert list_resp.status_code == 200
        tool_calls = list_resp.json().get("tool_calls")
        assert tool_calls
        assert tool_calls[0]["name"] == "list_tasks"
