from __future__ import annotations

import pytest
from sqlalchemy.pool import StaticPool

from src.services import db


@pytest.mark.anyio
async def test_get_engine_handles_postgres_prefix() -> None:
    engine = db.get_engine("postgresql://user:pass@localhost/db")
    try:
        assert engine.url.render_as_string(hide_password=False).startswith("postgresql+psycopg://")
    finally:
        await engine.dispose()


@pytest.mark.anyio
async def test_get_engine_sqlite_uses_static_pool() -> None:
    engine = db.get_engine("sqlite+aiosqlite:///:memory:")
    try:
        assert isinstance(engine.sync_engine.pool, StaticPool)
    finally:
        await engine.dispose()


def test_get_database_url_valid_and_missing() -> None:
    env = {"DATABASE_URL": " sqlite:///:memory: "}
    assert db.get_database_url(env) == "sqlite:///:memory:"
    with pytest.raises(ValueError):
        db.get_database_url({"DATABASE_URL": "   "})


@pytest.mark.anyio
async def test_init_engine_from_env_invokes_create_all(monkeypatch) -> None:
    calls: list[str] = []

    class DummyEngine:
        disposed = False

        async def dispose(self) -> None:
            self.disposed = True

    async def fake_create_all(engine: object) -> None:
        calls.append("create_all")

    def fake_get_engine(url: str) -> DummyEngine:
        calls.append(f"get_engine:{url}")
        return DummyEngine()

    monkeypatch.setattr(db, "create_all", fake_create_all)
    monkeypatch.setattr(db, "get_engine", fake_get_engine)

    engine = await db.init_engine_from_env({"DATABASE_URL": "sqlite+aiosqlite:///:memory:"})
    assert calls == ["get_engine:sqlite+aiosqlite:///:memory:", "create_all"]
    assert isinstance(engine, DummyEngine)
    await engine.dispose()
    assert engine.disposed is True
