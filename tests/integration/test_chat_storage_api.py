from __future__ import annotations

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.services import db

# [Task]: T004 [From]: specs/008-chat-storage/spec.md User Story 1


@pytest.mark.anyio
async def test_create_conversation_integration(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "chat.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.post("/api/conversations", headers=auth_headers_factory("integration-user"))
        assert resp.status_code == status.HTTP_201_CREATED
    await db.dispose_engine()


@pytest.mark.anyio
async def test_append_message_integration(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "chat_messages.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    headers = auth_headers_factory("integration-user")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        conv_resp = await client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == status.HTTP_201_CREATED
        conversation_id = conv_resp.json()["id"]

        resp = await client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "assistant", "content": "hello"},
        )
        assert resp.status_code == status.HTTP_201_CREATED
    await db.dispose_engine()


@pytest.mark.anyio
async def test_history_retrieval_integration(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "chat_history.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    headers = auth_headers_factory("history-user")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        conv_resp = await client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == status.HTTP_201_CREATED
        conversation_id = conv_resp.json()["id"]

        first = await client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "user", "content": "first"},
        )
        assert first.status_code == status.HTTP_201_CREATED

        second = await client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "assistant", "content": "second"},
        )
        assert second.status_code == status.HTTP_201_CREATED

        history = await client.get(f"/api/conversations/{conversation_id}/messages", headers=headers)
        assert history.status_code == status.HTTP_200_OK
    await db.dispose_engine()
