from __future__ import annotations

# [Task]: T014 [From]: specs/014-agent-behavior-validation/spec.md User Story 3

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
    stub_agent_responses,
)


def test_behavior_task_not_found_response(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "complete_task", '{"task_id":9999}')],
            )
        ),
        build_response(build_message(content="I could not complete that request.")),
    ]

    stub_agent_responses(monkeypatch, responses)

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
        assert "could not" in payload["response"].lower()
