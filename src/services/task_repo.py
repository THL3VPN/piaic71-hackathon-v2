from __future__ import annotations

from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task


async def create_task(
    session: AsyncSession, *, owner_id: str, title: str, description: str | None = None
) -> Task:
    """Create and persist a task owned by a user with validation."""
    task = Task(owner_id=owner_id, title=title, description=description)
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_task(session: AsyncSession, task_id: int) -> Task | None:
    """Fetch a task by ID; returns None if missing."""
    return await session.get(Task, task_id)


async def list_tasks(session: AsyncSession, *, owner_id: str) -> Sequence[Task]:
    """List tasks for an owner in deterministic (created_at, id) order."""
    stmt = select(Task).where(Task.owner_id == owner_id).order_by(Task.created_at, Task.id)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_task_or_404(session: AsyncSession, task_id: int) -> Task:
    task = await get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


async def update_task(
    session: AsyncSession, task_id: int, *, owner_id: str, title: str, description: str | None = None
) -> Task:
    task = await get_owned_task_or_404(session, task_id, owner_id=owner_id)
    trimmed = title.strip()
    if not trimmed:
        raise ValueError("title cannot be empty")
    task.title = trimmed
    task.description = description
    await session.commit()
    await session.refresh(task)
    return task


async def delete_task(session: AsyncSession, task_id: int, *, owner_id: str) -> None:
    task = await get_owned_task_or_404(session, task_id, owner_id=owner_id)
    await session.delete(task)
    await session.commit()


async def toggle_task_completion(session: AsyncSession, task_id: int, *, owner_id: str) -> Task:
    task = await get_owned_task_or_404(session, task_id, owner_id=owner_id)
    task.completed = not task.completed
    await session.commit()
    await session.refresh(task)
    return task


async def get_owned_task_or_404(session: AsyncSession, task_id: int, *, owner_id: str) -> Task:
    """Fetch a task owned by the given user or raise 403/404."""
    task = await get_task(session, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != owner_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    return task
