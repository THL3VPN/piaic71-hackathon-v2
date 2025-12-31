from __future__ import annotations

# [Task]: T006 [From]: specs/010-stateless-chat/spec.md User Story 1

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.services import db


@pytest.mark.anyio
async def test_chat_creates_conversation_and_messages(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "chat_flow.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    headers = auth_headers_factory("chat-user")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/chat", headers=headers, json={"message": "Hello"})
        assert resp.status_code == status.HTTP_200_OK
        payload = resp.json()
        conversation_id = payload["conversation_id"]
        history = await client.get(f"/api/conversations/{conversation_id}/messages", headers=headers)
        assert history.status_code == status.HTTP_200_OK
        messages = history.json()
        assert len(messages) == 2
    await db.dispose_engine()


# [Task]: T012 [From]: specs/010-stateless-chat/spec.md User Story 2
@pytest.mark.anyio
async def test_chat_validation_and_ownership(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "chat_validation.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    owner_headers = auth_headers_factory("owner-user")
    other_headers = auth_headers_factory("other-user")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        conv_resp = await client.post("/api/conversations", headers=owner_headers)
        assert conv_resp.status_code == status.HTTP_201_CREATED
        conversation_id = conv_resp.json()["id"]

        resp = await client.post(
            "/api/chat",
            headers=other_headers,
            json={"conversation_id": conversation_id, "message": "Hello"},
        )
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        invalid = await client.post("/api/chat", headers=owner_headers, json={})
        assert invalid.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    await db.dispose_engine()


# [Task]: T017 [From]: specs/010-stateless-chat/spec.md User Story 3
@pytest.mark.anyio
async def test_chat_history_persists_across_requests(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "chat_history_flow.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    headers = auth_headers_factory("history-user")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.post("/api/chat", headers=headers, json={"message": "First"})
        assert first.status_code == status.HTTP_200_OK
        conversation_id = first.json()["conversation_id"]

        second = await client.post(
            "/api/chat",
            headers=headers,
            json={"conversation_id": conversation_id, "message": "Second"},
        )
        assert second.status_code == status.HTTP_200_OK

        history = await client.get(f"/api/conversations/{conversation_id}/messages", headers=headers)
        assert history.status_code == status.HTTP_200_OK
        assert len(history.json()) == 4
    await db.dispose_engine()
