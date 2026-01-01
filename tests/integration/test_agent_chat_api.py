from __future__ import annotations

# [Task]: T006 [From]: specs/012-ai-agent-integration/spec.md User Story 1

from fastapi.testclient import TestClient

from src.main import app


def test_agent_chat_invokes_tools(auth_headers_factory) -> None:
    headers = auth_headers_factory("agent-integration-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Create a task called write report"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        assert payload.get("tool_calls"), "Expected tool calls to be returned"

        tasks_resp = client.get("/api/tasks", headers=headers)
        assert tasks_resp.status_code == 200
        titles = [task["title"] for task in tasks_resp.json()]
        assert "write report" in [title.lower() for title in titles]
