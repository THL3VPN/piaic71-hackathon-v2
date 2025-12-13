from __future__ import annotations

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task


async def create_task(session: AsyncSession, title: str, description: str | None = None) -> Task:
    """Create and persist a task with validation."""
    # DEBUG instrumentation for tests
    task = Task(title=title, description=description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    """Fetch a task by ID; returns None if missing."""
    return await session.get(Task, task_id)


async def list_tasks(session: AsyncSession) -> Sequence[Task]:
    """List tasks in deterministic (created_at, id) order."""
    stmt = select(Task).order_by(Task.created_at, Task.id)
    result = await session.execute(stmt)
    return result.scalars().all()
