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
