from __future__ import annotations

from dataclasses import asdict, dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task
from src.services import task_repo

# [Task]: T002 [From]: specs/011-task-tools/spec.md User Story 1


class TaskToolError(Exception):
    """Base class for task tool domain errors."""


class TaskNotFound(TaskToolError):
    """Raised when a task cannot be found."""


class UnauthorizedAccess(TaskToolError):
    """Raised when a user attempts to access a task they do not own."""


class InvalidInput(TaskToolError):
    """Raised when tool inputs fail validation."""


@dataclass(frozen=True)
class ToolResult:
    """Structured tool result placeholder."""

    task_id: int
    status: str
    title: str


@dataclass(frozen=True)
class TaskSummary:
    id: int
    title: str
    completed: bool


def _raise_invalid_input_from_value_error(exc: ValueError) -> None:
    raise InvalidInput(str(exc)) from exc


def _validate_title(title: str) -> str:
    trimmed = title.strip()
    if not trimmed:
        raise InvalidInput("title cannot be empty")
    return trimmed


def _coerce_status(status: str | None) -> str:
    value = (status or "all").strip().lower()
    if value not in {"all", "pending", "completed"}:
        raise InvalidInput("status must be one of: all, pending, completed")
    return value


async def _get_owned_task(session: AsyncSession, task_id: int, user_id: str) -> Task:
    task = await task_repo.get_task(session, task_id)
    if task is None:
        raise TaskNotFound("Task not found")
    if task.owner_id != user_id:
        raise UnauthorizedAccess("Task not owned by user")
    return task


def _result(task: Task, status: str) -> dict[str, object]:
    return asdict(ToolResult(task_id=task.id, status=status, title=task.title))


def _summary(task: Task) -> dict[str, object]:
    return asdict(TaskSummary(id=task.id, title=task.title, completed=task.completed))


async def add_task(
    session: AsyncSession,
    *,
    user_id: str,
    title: str,
    description: str | None = None,
) -> dict[str, object]:
    """Create a new task for a user and return a structured result."""
    _validate_title(title)
    try:
        task = await task_repo.create_task(
            session,
            owner_id=user_id,
            title=title,
            description=description,
        )
    except ValueError as exc:
        _raise_invalid_input_from_value_error(exc)
    return _result(task, "created")


async def list_tasks(
    session: AsyncSession,
    *,
    user_id: str,
    status: str | None = None,
) -> list[dict[str, object]]:
    """List tasks for a user with optional status filtering."""
    status_value = _coerce_status(status)
    tasks = await task_repo.list_tasks(session, owner_id=user_id)
    if status_value == "completed":
        tasks = [task for task in tasks if task.completed]
    elif status_value == "pending":
        tasks = [task for task in tasks if not task.completed]
    return [_summary(task) for task in tasks]


async def complete_task(
    session: AsyncSession,
    *,
    user_id: str,
    task_id: int,
) -> dict[str, object]:
    """Mark a task as completed and return a structured result."""
    task = await _get_owned_task(session, task_id, user_id)
    task.completed = True
    await session.commit()
    await session.refresh(task)
    return _result(task, "completed")


async def delete_task(
    session: AsyncSession,
    *,
    user_id: str,
    task_id: int,
) -> dict[str, object]:
    """Delete a task and return a structured result."""
    task = await _get_owned_task(session, task_id, user_id)
    await session.delete(task)
    await session.commit()
    return _result(task, "deleted")


async def update_task(
    session: AsyncSession,
    *,
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> dict[str, object]:
    """Update a task title/description and return a structured result."""
    if title is None and description is None:
        raise InvalidInput("At least one field must be provided")
    task = await _get_owned_task(session, task_id, user_id)
    if title is not None:
        task.title = _validate_title(title)
    if description is not None:
        task.description = description
    await session.commit()
    await session.refresh(task)
    return _result(task, "updated")
