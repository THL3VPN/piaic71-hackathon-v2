from __future__ import annotations

# [Task]: T005 [From]: specs/010-stateless-chat/spec.md User Story 1
# [Task]: T021 [From]: specs/013-agent-tool-calls/tasks.md Align agent chat tests

from fastapi.testclient import TestClient

from src.main import app


def test_stateless_chat_contract(auth_headers_factory) -> None:
    headers = auth_headers_factory("chat-contract-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Hello"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        assert "conversation_id" in payload
        response = payload["response"]
        assert isinstance(response, str)
        assert response
        assert payload["tool_calls"] == []

        history = client.get(f"/api/conversations/{payload['conversation_id']}/messages", headers=headers)
        assert history.status_code == 200
        messages = history.json()
        assert len(messages) == 2
        assert messages[0]["role"] == "user"
        assert messages[1]["role"] == "assistant"


# [Task]: T011 [From]: specs/010-stateless-chat/spec.md User Story 2
def test_stateless_chat_validation_and_ownership(auth_headers_factory) -> None:
    owner_headers = auth_headers_factory("owner-user")
    other_headers = auth_headers_factory("other-user")
    with TestClient(app) as client:
        conv_resp = client.post("/api/conversations", headers=owner_headers)
        assert conv_resp.status_code == 201
        conversation_id = conv_resp.json()["id"]

        resp = client.post(
            "/api/chat",
            headers=other_headers,
            json={"conversation_id": conversation_id, "message": "Hi"},
        )
        assert resp.status_code == 404

        invalid_resp = client.post("/api/chat", headers=owner_headers, json={})
        assert invalid_resp.status_code == 422


# [Task]: T016 [From]: specs/010-stateless-chat/spec.md User Story 3
def test_stateless_chat_uses_history(auth_headers_factory) -> None:
    headers = auth_headers_factory("history-user")
    with TestClient(app) as client:
        first = client.post("/api/chat", headers=headers, json={"message": "First"})
        assert first.status_code == 200
        conversation_id = first.json()["conversation_id"]

        second = client.post(
            "/api/chat",
            headers=headers,
            json={"conversation_id": conversation_id, "message": "Second"},
        )
        assert second.status_code == 200

        history = client.get(f"/api/conversations/{conversation_id}/messages", headers=headers)
        assert history.status_code == 200
        messages = history.json()
        assert len(messages) == 4
