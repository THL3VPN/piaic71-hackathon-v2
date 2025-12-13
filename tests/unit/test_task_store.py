from __future__ import annotations

import pytest

from src.models.task import Task
from src.services import task_store


def test_add_task_generates_incrementing_ids_and_trims() -> None:
    tasks: list[Task] = [Task(id=1, title="first")]
    added = task_store.add_task(tasks, "  second  ")
    assert added.id == 2
    assert added.title == "second"
    assert added.completed is False
    assert tasks[-1] is added


@pytest.mark.parametrize("title", ["", "   ", None])
def test_add_task_rejects_empty_titles(title: str | None) -> None:
    tasks: list[Task] = []
    with pytest.raises(ValueError):
        task_store.add_task(tasks, title)  # type: ignore[arg-type]


def test_list_tasks_returns_copy() -> None:
    tasks = [Task(id=1, title="a")]
    result = task_store.list_tasks(tasks)
    assert result == tasks
    result.append(Task(id=2, title="b"))
    assert len(tasks) == 1  # original list unchanged


def test_update_task_happy_path_and_missing() -> None:
    tasks = [Task(id=1, title="a"), Task(id=2, title="b")]
    updated = task_store.update_task(tasks, 2, "  new  ")
    assert updated is tasks[1]
    assert updated.title == "new"
    assert task_store.update_task(tasks, 99, "other") is None


def test_update_task_rejects_empty_title() -> None:
    tasks = [Task(id=1, title="a")]
    with pytest.raises(ValueError):
        task_store.update_task(tasks, 1, "   ")


def test_delete_and_toggle_behaviors() -> None:
    tasks = [Task(id=1, title="a"), Task(id=2, title="b")]
    assert task_store.delete_task(tasks, 1) is True
    assert len(tasks) == 1 and tasks[0].id == 2
    assert task_store.delete_task(tasks, 99) is False

    toggled = task_store.toggle_task(tasks, 2)
    assert toggled is tasks[0]
    assert toggled.completed is True
    assert task_store.toggle_task(tasks, 99) is None
