from __future__ import annotations

from datetime import datetime, timezone

import pytest

from src.models.task import Task


def test_task_defaults_and_trimmed_title() -> None:
    task = Task(title="  Test title  ")
    assert task.title == "Test title"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)
    assert task.created_at.tzinfo == timezone.utc


def test_empty_title_rejected() -> None:
    with pytest.raises(ValueError):
        Task(title="   ")

