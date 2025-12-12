from __future__ import annotations

from typing import Iterable, Optional

from rich.console import Console
from rich.table import Table

from src.models.task import Task


def render_tasks(tasks: Iterable[Task], console: Optional[Console] = None) -> None:
    """Render tasks as a table; show empty state if none."""
    console = console or Console()
    table = Table(title="Tasks", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="bold")
    table.add_column("Title")
    table.add_column("Status")

    tasks_list = list(tasks)
    if not tasks_list:
        console.print("[yellow]No tasks yet. Add your first task![/yellow]")
        return

    for task in tasks_list:
        status = "✅ Complete" if task.completed else "⏳ Incomplete"
        table.add_row(str(task.id), task.title, status)
    console.print(table)


def render_add_confirmation(task: Task, console: Optional[Console] = None) -> None:
    """Render confirmation after adding a task."""
    console = console or Console()
    status = "✅ Complete" if task.completed else "⏳ Incomplete"
    console.print(f"[green]Added task[/green] [bold]{task.id}[/bold]: {task.title} ({status})")
