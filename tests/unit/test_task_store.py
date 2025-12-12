from __future__ import annotations

import pytest

from src.models.task import Task
from src.services import task_store


def test_list_tasks_empty_returns_empty_list():
    tasks: list[Task] = []
    result = task_store.list_tasks(tasks)
    assert result == []


def test_list_tasks_returns_copy_not_same_object():
    tasks = [Task(id=1, title="a"), Task(id=2, title="b", completed=True)]
    result = task_store.list_tasks(tasks)
    assert result == tasks
    assert result is not tasks


def test_list_tasks_does_not_mutate_original():
    tasks = [Task(id=1, title="a")]
    result = task_store.list_tasks(tasks)
    result.append(Task(id=2, title="b"))
    assert len(tasks) == 1
    assert tasks[0].id == 1


def test_list_tasks_preserves_order_and_fields():
    tasks = [Task(id=1, title="a"), Task(id=2, title="b", completed=True)]
    result = task_store.list_tasks(tasks)
    assert [(t.id, t.title, t.completed) for t in result] == [(1, "a", False), (2, "b", True)]




def test_add_task_assigns_incrementing_id_and_defaults():
    tasks: list[Task] = []
    new = task_store.add_task(tasks, "New Task")
    assert new.id == 1
    assert new.title == "New Task"
    assert new.completed is False
    assert tasks[-1] is new


def test_add_task_rejects_empty_title():
    tasks: list[Task] = []
    with pytest.raises(ValueError):
        task_store.add_task(tasks, "   ")


def test_add_task_increments_from_existing_max():
    tasks = [Task(id=5, title="a"), Task(id=10, title="b")]
    new = task_store.add_task(tasks, "c")
    assert new.id == 11
    assert tasks[-1] is new





def test_update_task_updates_title_when_found():
    tasks = [Task(id=1, title="old")]
    updated = task_store.update_task(tasks, 1, "new")
    assert updated is tasks[0]
    assert updated.title == "new"


def test_update_task_returns_none_when_not_found():
    tasks = [Task(id=1, title="old")]
    updated = task_store.update_task(tasks, 2, "new")
    assert updated is None
    assert tasks[0].title == "old"


def test_update_task_rejects_empty_title():
    tasks = [Task(id=1, title="old")]
    with pytest.raises(ValueError):
        task_store.update_task(tasks, 1, "   ")


def test_delete_task_removes_when_found():
    tasks = [Task(id=1, title="a"), Task(id=2, title="b")]
    assert task_store.delete_task(tasks, 1) is True
    assert [t.id for t in tasks] == [2]


def test_delete_task_returns_false_when_not_found():
    tasks = [Task(id=1, title="a")]
    assert task_store.delete_task(tasks, 2) is False
    assert len(tasks) == 1


def test_toggle_task_flips_status_when_found():
    tasks = [Task(id=1, title="a", completed=False)]
    toggled = task_store.toggle_task(tasks, 1)
    assert toggled.completed is True
    toggled = task_store.toggle_task(tasks, 1)
    assert toggled.completed is False


def test_toggle_task_returns_none_when_not_found():
    tasks = [Task(id=1, title="a", completed=False)]
    assert task_store.toggle_task(tasks, 2) is None
    assert tasks[0].completed is False
