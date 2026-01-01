from __future__ import annotations

# [Task]: T006 [From]: specs/009-message-history-read/spec.md User Story 1

import pytest
from fastapi import status
from httpx import ASGITransport, AsyncClient

from src.main import app
from src.services import db


@pytest.mark.anyio
async def test_message_history_integration(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "message_history.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    headers = auth_headers_factory("history-user")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        conv_resp = await client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == status.HTTP_201_CREATED
        conversation_id = conv_resp.json()["id"]

        await client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "user", "content": "hello"},
        )

        history = await client.get(f"/api/conversations/{conversation_id}/messages", headers=headers)
        assert history.status_code == status.HTTP_200_OK
    await db.dispose_engine()


# [Task]: T012 [From]: specs/009-message-history-read/spec.md User Story 2
@pytest.mark.anyio
async def test_message_history_limit_integration(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "message_history_limit.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    headers = auth_headers_factory("history-user")
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        conv_resp = await client.post("/api/conversations", headers=headers)
        assert conv_resp.status_code == status.HTTP_201_CREATED
        conversation_id = conv_resp.json()["id"]

        await client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "user", "content": "one"},
        )
        await client.post(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            json={"role": "assistant", "content": "two"},
        )

        history = await client.get(
            f"/api/conversations/{conversation_id}/messages",
            headers=headers,
            params={"limit": 1},
        )
        assert history.status_code == status.HTTP_200_OK
        assert len(history.json()) == 1
    await db.dispose_engine()
