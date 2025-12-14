from __future__ import annotations

import io

from rich.console import Console

from src.cli import render
from src.models.task import Task


def _console() -> Console:
    return Console(file=io.StringIO(), force_terminal=False, color_system=None)


def test_render_tasks_empty_shows_message() -> None:
    console = _console()
    render.render_tasks([], console=console)
    output = console.file.getvalue()
    assert "No tasks yet" in output


def test_render_tasks_populated_renders_rows() -> None:
    console = _console()
    tasks = [Task(id=1, title="Do thing"), Task(id=2, title="Done", completed=True)]
    render.render_tasks(tasks, console=console)
    text = console.file.getvalue()
    assert "Do thing" in text
    assert "Done" in text
    assert "✅ Complete" in text
    assert "⏳ Incomplete" in text


def test_render_add_confirmation_includes_status() -> None:
    console = _console()
    task = Task(id=3, title="Write tests", completed=False)
    render.render_add_confirmation(task, console=console)
    out = console.file.getvalue()
    assert "Added task" in out
    assert "Write tests" in out
    assert "⏳ Incomplete" in out
