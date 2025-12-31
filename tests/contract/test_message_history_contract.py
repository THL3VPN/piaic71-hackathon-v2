from __future__ import annotations

# [Task]: T005 [From]: specs/009-message-history-read/spec.md User Story 1

from fastapi.testclient import TestClient

from src.main import app


def test_message_history_contract(auth_headers_factory) -> None:
    headers = auth_headers_factory("history-contract-user")
    with TestClient(app) as client:
        conv_resp = client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == 201
        conversation_id = conv_resp.json()["id"]

        first = client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "user", "content": "first"},
        )
        assert first.status_code == 201

        second = client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "assistant", "content": "second"},
        )
        assert second.status_code == 201

        history = client.get(f"/api/conversations/{conversation_id}/messages", headers=headers)
        assert history.status_code == 200
        payload = history.json()
        assert isinstance(payload, list)
        assert payload[0]["role"] == "user"
        assert payload[1]["role"] == "assistant"
        assert payload[0]["conversation_id"] == conversation_id
        assert payload[0]["content"] == "first"
        assert payload[1]["content"] == "second"


# [Task]: T011 [From]: specs/009-message-history-read/spec.md User Story 2
def test_message_history_limit_contract(auth_headers_factory) -> None:
    headers = auth_headers_factory("history-limit-user")
    with TestClient(app) as client:
        conv_resp = client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == 201
        conversation_id = conv_resp.json()["id"]

        client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "user", "content": "one"},
        )
        client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "assistant", "content": "two"},
        )

        history = client.get(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            params={"limit": 1},
        )
        assert history.status_code == 200
        payload = history.json()
        assert len(payload) == 1
