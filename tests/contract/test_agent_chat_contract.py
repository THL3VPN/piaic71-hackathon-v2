from __future__ import annotations

# [Task]: T005 [From]: specs/012-ai-agent-integration/spec.md User Story 1

from fastapi.testclient import TestClient

from src.main import app


def test_agent_chat_contract_includes_tool_calls(auth_headers_factory) -> None:
    headers = auth_headers_factory("agent-contract-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Add a task to buy milk"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        assert "conversation_id" in payload
        assert isinstance(payload.get("response"), str)
        tool_calls = payload.get("tool_calls")
        assert isinstance(tool_calls, list)
        assert tool_calls, "Expected at least one tool call"
        first_call = tool_calls[0]
        assert "name" in first_call
        assert "arguments" in first_call
        assert "result" in first_call
