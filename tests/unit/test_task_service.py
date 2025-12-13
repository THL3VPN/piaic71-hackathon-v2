from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import anyio
import asyncio
import pytest
from sqlalchemy import delete, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.models.task import Task
from src.services import db, task_repo


RUN_DB_TESTS = os.getenv("RUN_DB_TESTS") == "1"
TEST_DB_URL = os.getenv("DATABASE_URL")

if not RUN_DB_TESTS or not TEST_DB_URL:
    pytest.skip("Set RUN_DB_TESTS=1 and DATABASE_URL to run task service tests", allow_module_level=True)


@pytest.fixture
async def engine(tmp_path) -> AsyncEngine:
    engine = db.get_engine(TEST_DB_URL)
    try:
        await db.create_all(engine)
    except (SQLAlchemyError, asyncio.CancelledError, asyncio.TimeoutError) as exc:
        pytest.skip(f"Skipping DB tests due to connection issue: {exc}")
    async with db.get_session(engine) as session:
        await session.execute(delete(Task))
        await session.commit()
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncSession:
    async with db.get_session(engine) as session:
        yield session


@pytest.mark.anyio
async def test_create_task_trims_and_sets_defaults(session: AsyncSession) -> None:
    task = await task_repo.create_task(session, "  title  ", "desc")
    assert task.id is not None
    assert task.title == "title"
    assert task.description == "desc"
    assert task.completed is False


@pytest.mark.anyio
async def test_create_task_rejects_empty_title(session: AsyncSession) -> None:
    with pytest.raises(ValueError):
        await task_repo.create_task(session, "   ")


@pytest.mark.anyio
async def test_get_task_handles_missing(session: AsyncSession) -> None:
    assert await task_repo.get_task(session, 9999) is None


@pytest.mark.anyio
async def test_list_tasks_orders_by_created_at(session: AsyncSession) -> None:
    first = await task_repo.create_task(session, "first")
    second = await task_repo.create_task(session, "second")
    tasks = await task_repo.list_tasks(session)
    assert [t.id for t in tasks] == [first.id, second.id]


@pytest.mark.anyio
async def test_list_tasks_handles_empty(session: AsyncSession) -> None:
    tasks = await task_repo.list_tasks(session)
    assert tasks == []


@pytest.mark.anyio
async def test_list_tasks_orders_by_created_at_even_with_custom_timestamps(session: AsyncSession) -> None:
    earlier = await task_repo.create_task(session, "earlier")
    later = await task_repo.create_task(session, "later")
    middle = await task_repo.create_task(session, "middle")
    base = datetime.now(timezone.utc)
    await session.execute(
        update(Task).where(Task.id == earlier.id).values(created_at=base + timedelta(seconds=5))
    )
    await session.execute(
        update(Task).where(Task.id == later.id).values(created_at=base - timedelta(seconds=5))
    )
    await session.commit()
    tasks = await task_repo.list_tasks(session)
    assert [t.id for t in tasks] == [later.id, middle.id, earlier.id]
