from __future__ import annotations

import io

from rich.console import Console

from src.cli import render
from src.models.task import Task


def test_render_tasks_empty_shows_message(capsys):
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=False, force_interactive=False, color_system=None)
    render.render_tasks([], console=console)
    console.file.flush()
    output = buffer.getvalue()
    assert "No tasks yet" in output


def test_render_tasks_shows_rows(capsys):
    tasks = [Task(id=1, title="Alpha"), Task(id=2, title="Beta", completed=True)]
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=False, force_interactive=False, color_system=None)
    render.render_tasks(tasks, console=console)
    console.file.flush()
    output = buffer.getvalue()
    assert "Alpha" in output
    assert "Beta" in output
    assert "Complete" in output




from src.cli import render


def test_render_add_confirmation_outputs_title_and_id(capsys):
    task = Task(id=3, title="New", completed=False)
    buffer = io.StringIO()
    console = Console(file=buffer, force_terminal=False, force_interactive=False, color_system=None)
    render.render_add_confirmation(task, console=console)
    console.file.flush()
    output = buffer.getvalue()
    assert "Added task" in output
    assert "3" in output
    assert "New" in output
