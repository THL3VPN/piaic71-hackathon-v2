from __future__ import annotations

from typing import Callable, List

import questionary

from src.cli.render import render_tasks, render_add_confirmation
from src.services.task_store import add_task, update_task, delete_task, toggle_task
from src.models.task import Task


def main_menu_loop(
    tasks: List[Task] | None = None,
    interactive: bool = True,
    once: bool = False,
    select_fn: Callable[[list[str]], str | None] | None = None,
    prompt_fn: Callable[[str], str | None] | None = None,
) -> None:
    """Minimal menu loop placeholder; supports view and add stubs.

    interactive=False runs a single view pass (used in tests).
    once=True allows single-iteration loop for tests.
    """
    tasks = tasks if tasks is not None else []

    select_fn = select_fn or (
        lambda choices: questionary.select("Choose an option", choices=choices, qmark="> ").ask()
    )
    prompt_fn = prompt_fn or (lambda message: questionary.text(message).ask())

    if not interactive:
        render_tasks(tasks)
        return

    while True:
        choice = select_fn(
            ["View tasks", "Add task", "Update task", "Delete task", "Mark complete/incomplete", "Exit"]
        )

        if choice == "View tasks":
            render_tasks(tasks)
        elif choice == "Add task":
            title = prompt_fn("Task title")
            _handle_add(tasks, title)
        elif choice == "Update task":
            _handle_update(tasks, prompt_fn)
        elif choice == "Delete task":
            _handle_delete(tasks, prompt_fn)
        elif choice == "Mark complete/incomplete":
            _handle_toggle(tasks, prompt_fn)
        elif choice == "Exit" or choice is None:
            break

        if once:
            break


def _handle_add(tasks: List[Task], title: str) -> None:
    """Handle add flow with validation."""
    if title is None:
        return
    try:
        task = add_task(tasks, title)
    except ValueError:
        # In full UI we would render a validation message; keep silent here for now.
        return
    render_add_confirmation(task)


def _prompt_int(prompt_fn: Callable[[str], str | None], message: str) -> int | None:
    raw = prompt_fn(message)
    if raw is None:
        return None
    raw = raw.strip()
    if not raw.isdigit():
        return None
    return int(raw)


def _handle_update(tasks: List[Task], prompt_fn: Callable[[str], str | None]) -> None:
    task_id = _prompt_int(prompt_fn, "Task ID to update")
    if task_id is None:
        return
    new_title = prompt_fn("New title")
    if new_title is None:
        return
    try:
        updated = update_task(tasks, task_id, new_title)
    except ValueError:
        return
    if updated is None:
        return
    render_add_confirmation(updated)


def _handle_delete(tasks: List[Task], prompt_fn: Callable[[str], str | None]) -> None:
    task_id = _prompt_int(prompt_fn, "Task ID to delete")
    if task_id is None:
        return
    deleted = delete_task(tasks, task_id)
    if not deleted:
        return
    # Could render confirmation; no-op for now


def _handle_toggle(tasks: List[Task], prompt_fn: Callable[[str], str | None]) -> None:
    task_id = _prompt_int(prompt_fn, "Task ID to toggle")
    if task_id is None:
        return
    toggled = toggle_task(tasks, task_id)
    if toggled is None:
        return
    # Could render confirmation; no-op for now
