from __future__ import annotations

import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport

from src.main import app
from src.services import db


@pytest.mark.anyio
async def test_register_and_login_success(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "auth.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        reg = await client.post("/api/register", json={"username": "alice", "password": "pw1234"})
        assert reg.status_code == status.HTTP_201_CREATED

        login = await client.post("/api/login", json={"username": "alice", "password": "pw1234"})
        assert login.status_code == status.HTTP_200_OK
        body = login.json()
        assert "token" in body and body["token"]
    await db.dispose_engine()


@pytest.mark.anyio
async def test_register_duplicate_username(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "auth_dup.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.post("/api/register", json={"username": "bob", "password": "pw1234"})
        assert first.status_code == status.HTTP_201_CREATED
        dup = await client.post("/api/register", json={"username": "bob", "password": "pw5678"})
        assert dup.status_code in (status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT)
    await db.dispose_engine()


@pytest.mark.anyio
async def test_login_invalid_credentials(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    db_file = tmp_path / "auth_invalid.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    await db.init_engine_from_env()
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await client.post("/api/register", json={"username": "carol", "password": "pw1234"})
        bad = await client.post("/api/login", json={"username": "carol", "password": "wrongpass"})
        assert bad.status_code == status.HTTP_401_UNAUTHORIZED
        missing = await client.post("/api/login", json={"username": "nobody", "password": "pw1234"})
        assert missing.status_code == status.HTTP_401_UNAUTHORIZED
    await db.dispose_engine()
