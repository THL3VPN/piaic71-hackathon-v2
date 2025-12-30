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
