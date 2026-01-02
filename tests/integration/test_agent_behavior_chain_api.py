from __future__ import annotations

# [Task]: T010 [From]: specs/014-agent-behavior-validation/spec.md User Story 2

from fastapi.testclient import TestClient

from src.main import app
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
    stub_agent_responses,
)


def test_behavior_chain_for_ambiguous_delete_and_complete(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "list_tasks", '{"status":"all"}')],
            )
        ),
        build_response(build_message(content="Which task should I delete?")),
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-2", "list_tasks", '{"status":"all"}')],
            )
        ),
        build_response(build_message(content="Which task did you finish?")),
    ]

    stub_agent_responses(monkeypatch, responses)

    headers = auth_headers_factory("behavior-chain-user")
    with TestClient(app) as client:
        delete_resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Delete the meeting task"},
        )
        assert delete_resp.status_code == 200
        delete_calls = delete_resp.json().get("tool_calls")
        assert delete_calls
        assert delete_calls[0]["name"] == "list_tasks"

        complete_resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "I finished the groceries task"},
        )
        assert complete_resp.status_code == 200
        complete_calls = complete_resp.json().get("tool_calls")
        assert complete_calls
        assert complete_calls[0]["name"] == "list_tasks"
