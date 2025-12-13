from __future__ import annotations

import os

import anyio
import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.services.db import create_all, get_database_url, get_engine, init_engine_from_env


RUN_DB_TESTS = os.getenv("RUN_DB_TESTS") == "1"

if not RUN_DB_TESTS:
    pytest.skip("Set RUN_DB_TESTS=1 to exercise startup DB integration tests", allow_module_level=True)


@pytest.mark.anyio
async def test_create_all_creates_metadata_tables(tmp_path) -> None:
    db_file = tmp_path / "test.db"
    url = f"sqlite+aiosqlite:///{db_file}"
    engine = get_engine(url)
    try:
        await create_all(engine)
    finally:
        await engine.dispose()


@pytest.mark.anyio
async def test_init_engine_from_env_valid(monkeypatch, tmp_path) -> None:
    db_file = tmp_path / "env.db"
    url = f"sqlite+aiosqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", url)
    engine = await init_engine_from_env()
    try:
        assert engine is not None
    finally:
        await engine.dispose()


@pytest.mark.anyio
async def test_get_database_url_missing(monkeypatch) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)
    with pytest.raises(ValueError):
        get_database_url()


@pytest.mark.anyio
async def test_invalid_url_surfaces_error(monkeypatch) -> None:
    bad_url = "notadb://"
    monkeypatch.setenv("DATABASE_URL", bad_url)
    with pytest.raises(SQLAlchemyError):
        with anyio.fail_after(5):
            engine = await init_engine_from_env()
            await engine.dispose()
