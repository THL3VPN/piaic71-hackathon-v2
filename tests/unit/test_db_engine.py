from __future__ import annotations

import pytest
from typing import AsyncIterator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.services import db


TEST_DB_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture
async def engine() -> AsyncIterator[AsyncEngine]:
    engine = db.get_engine(TEST_DB_URL)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.mark.anyio
async def test_get_engine_returns_async_engine(engine: AsyncEngine) -> None:
    assert isinstance(engine, AsyncEngine)


@pytest.mark.anyio
async def test_session_executes_simple_query(engine: AsyncEngine) -> None:
    async with db.get_session(engine) as session:
        assert isinstance(session, AsyncSession)
