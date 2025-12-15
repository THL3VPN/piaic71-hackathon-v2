from __future__ import annotations

import anyio
import asyncio
import os

import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src import main as app_module
from src.models.task import Task
from src.services import db, task_repo


RUN_DB_TESTS = os.getenv("RUN_DB_TESTS") == "1"
TEST_DB_URL = os.getenv("DATABASE_URL")

if not RUN_DB_TESTS or not TEST_DB_URL:
    pytest.skip("Set RUN_DB_TESTS=1 and DATABASE_URL to run task CRUD integration tests", allow_module_level=True)


@pytest.fixture
async def engine(tmp_path) -> AsyncEngine:
    engine = db.get_engine(TEST_DB_URL)
    try:
        await db.create_all(engine)
    except (SQLAlchemyError, asyncio.CancelledError, asyncio.TimeoutError) as exc:
        pytest.skip(f"Skipping DB tests due to connection issue: {exc}")
    async with db.get_session_for_engine(engine) as session:
        await session.execute(delete(Task))
        await session.commit()
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncSession:
    async with db.get_session_for_engine(engine) as session:
        yield session


@pytest.mark.anyio
async def test_create_then_get_round_trip(session: AsyncSession) -> None:
    with anyio.fail_after(5):
        created = await task_repo.create_task(session, "integration title", "desc")
        fetched = await task_repo.get_task(session, created.id)  # type: ignore[arg-type]
        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.title == "integration title"
        assert fetched.description == "desc"
        assert fetched.completed is False
