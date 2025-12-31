from fastapi.testclient import TestClient

from src.main import app

# [Task]: T003 [From]: specs/008-chat-storage/spec.md User Story 1


def test_create_conversation_contract(auth_headers_factory) -> None:
    with TestClient(app) as client:
        resp = client.post("/api/conversations", headers=auth_headers_factory("contract-user"))
    assert resp.status_code == 201
    body = resp.json()
    assert {"id", "created_at", "updated_at"}.issubset(body.keys())
    assert isinstance(body["id"], int)


def test_append_message_contract(auth_headers_factory) -> None:
    headers = auth_headers_factory("contract-user")
    with TestClient(app) as client:
        conv_resp = client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == 201
        conversation_id = conv_resp.json()["id"]

        resp = client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "user", "content": "hello"},
        )
    assert resp.status_code == 201
    body = resp.json()
    assert {"id", "conversation_id", "role", "content", "created_at"}.issubset(body.keys())
    assert body["conversation_id"] == conversation_id
    assert body["role"] == "user"
    assert body["content"] == "hello"


def test_list_messages_contract(auth_headers_factory) -> None:
    headers = auth_headers_factory("contract-user")
    with TestClient(app) as client:
        conv_resp = client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == 201
        conversation_id = conv_resp.json()["id"]

        post_resp = client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "assistant", "content": "hi"},
        )
        assert post_resp.status_code == 201

        resp = client.get(f"/api/conversations/{conversation_id}/messages", headers=headers)
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) >= 1
    first = body[0]
    assert {"id", "conversation_id", "role", "content", "created_at"}.issubset(first.keys())
