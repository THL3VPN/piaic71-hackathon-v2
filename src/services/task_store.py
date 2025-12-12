from __future__ import annotations

from typing import Iterable, Optional

from src.models.task import Task


def list_tasks(tasks: list[Task]) -> list[Task]:
    """Return all tasks (shallow copy)."""
    return list(tasks)


def add_task(tasks: list[Task], title: str) -> Task:
    """Create a task with validation, assign a unique id, append to list."""
    if not title or title.strip() == "":
        raise ValueError("Title cannot be empty")
    next_id = (max((t.id for t in tasks), default=0) + 1) if tasks else 1
    task = Task(id=next_id, title=title.strip(), completed=False)
    tasks.append(task)
    return task


def update_task(tasks: list[Task], task_id: int, new_title: str) -> Optional[Task]:
    """Update a task title if found; returns updated task or None."""
    if not new_title or new_title.strip() == "":
        raise ValueError("Title cannot be empty")
    for task in tasks:
        if task.id == task_id:
            task.title = new_title.strip()
            return task
    return None


def delete_task(tasks: list[Task], task_id: int) -> bool:
    """Delete a task by id; returns True if removed."""
    for idx, task in enumerate(tasks):
        if task.id == task_id:
            del tasks[idx]
            return True
    return False


def toggle_task(tasks: list[Task], task_id: int) -> Optional[Task]:
    """Toggle completion status for a task; returns updated task or None."""
    for task in tasks:
        if task.id == task_id:
            task.completed = not task.completed
            return task
    return None
