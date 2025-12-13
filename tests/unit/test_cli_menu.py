from __future__ import annotations

from typing import Any

from src.cli import menu
from src.models.task import Task


def test_main_menu_loop_noninteractive_renders(monkeypatch) -> None:
    seen: list[list[Task]] = []

    def fake_render(tasks: list[Task]) -> None:
        seen.append(tasks)

    monkeypatch.setattr(menu, "render_tasks", fake_render)
    tasks = [Task(id=1, title="x")]
    menu.main_menu_loop(tasks=tasks, interactive=False)
    assert seen == [tasks]


def test_prompt_int_parses_digits_and_rejects_other(monkeypatch) -> None:
    assert menu._prompt_int(lambda _: "12", "msg") == 12
    assert menu._prompt_int(lambda _: " 99 ", "msg") == 99
    assert menu._prompt_int(lambda _: "abc", "msg") is None
    assert menu._prompt_int(lambda _: None, "msg") is None


def test_handle_add_valid_and_invalid(monkeypatch) -> None:
    added: list[Task] = []

    def fake_add(tasks: list[Task], title: str) -> Task:
        if not title.strip():
            raise ValueError("empty")
        task = Task(id=1, title=title)
        tasks.append(task)
        return task

    def fake_render(task: Task) -> None:
        added.append(task)

    monkeypatch.setattr(menu, "add_task", fake_add)
    monkeypatch.setattr(menu, "render_add_confirmation", fake_render)

    tasks: list[Task] = []
    menu._handle_add(tasks, " title ")
    assert added and added[0].title == "title"

    menu._handle_add(tasks, None)
    menu._handle_add(tasks, "   ")
    assert len(tasks) == 1  # unchanged after invalid inputs


def test_handle_update_delete_toggle(monkeypatch) -> None:
    tasks = [Task(id=1, title="a")]
    rendered: list[Task] = []
    monkeypatch.setattr(menu, "render_add_confirmation", lambda t: rendered.append(t))
    monkeypatch.setattr(menu, "update_task", lambda ts, task_id, new: ts[0] if task_id == 1 else None)
    monkeypatch.setattr(menu, "delete_task", lambda ts, task_id: task_id == 1)
    monkeypatch.setattr(menu, "toggle_task", lambda ts, task_id: ts[0] if task_id == 1 else None)

    # update happy path
    prompts = iter(["1", "new title"])
    menu._handle_update(tasks, lambda _: next(prompts))
    assert rendered and rendered[-1] is tasks[0]

    # delete happy path
    prompts = iter(["1"])
    menu._handle_delete(tasks, lambda _: next(prompts))

    # toggle happy path
    prompts = iter(["1"])
    menu._handle_toggle(tasks, lambda _: next(prompts))

    # invalid prompt returns early
    prompts = iter(["abc"])
    menu._handle_update(tasks, lambda _: next(prompts))
    prompts = iter([None])
    menu._handle_toggle(tasks, lambda _: next(prompts))

    # missing id for delete -> early return
    prompts = iter([None])
    menu._handle_delete(tasks, lambda _: next(prompts))

    # update with missing title -> early return
    prompts = iter(["1", None])
    menu._handle_update(tasks, lambda _: next(prompts))

    # update with ValueError
    monkeypatch.setattr(menu, "update_task", lambda *_: (_ for _ in ()).throw(ValueError()))
    prompts = iter(["1", "bad"])
    menu._handle_update(tasks, lambda _: next(prompts))

    # update with no matching task
    monkeypatch.setattr(menu, "update_task", lambda ts, task_id, new: None)
    prompts = iter(["1", "missing"])
    menu._handle_update(tasks, lambda _: next(prompts))

    # delete with no match
    monkeypatch.setattr(menu, "delete_task", lambda *_: False)
    prompts = iter(["2"])
    menu._handle_delete(tasks, lambda _: next(prompts))

    # toggle missing task
    monkeypatch.setattr(menu, "toggle_task", lambda *_: None)
    prompts = iter(["2"])
    menu._handle_toggle(tasks, lambda _: next(prompts))


def test_main_menu_loop_once_add_flow(monkeypatch) -> None:
    tasks: list[Task] = []
    choices = iter(["Add task", "Exit"])
    titles = iter(["new title"])
    monkeypatch.setattr(menu, "render_add_confirmation", lambda task: None)

    menu.main_menu_loop(
        tasks=tasks,
        interactive=True,
        once=True,
        select_fn=lambda _: next(choices),
        prompt_fn=lambda _: next(titles, None),
    )
    assert tasks and tasks[0].title == "new title"


def test_main_menu_loop_view_and_exit(monkeypatch) -> None:
    tasks: list[Task] = [Task(id=1, title="x")]
    calls: list[str] = []

    def fake_render(ts: list[Task]) -> None:
        calls.append(f"render:{len(ts)}")

    monkeypatch.setattr(menu, "render_tasks", fake_render)

    choices = iter(["View tasks", "Exit"])
    menu.main_menu_loop(
        tasks=tasks,
        interactive=True,
        once=False,
        select_fn=lambda _: next(choices),
        prompt_fn=lambda _: None,
    )
    assert "render:1" in calls


def test_main_menu_loop_other_actions(monkeypatch) -> None:
    called: list[str] = []
    monkeypatch.setattr(menu, "_handle_update", lambda *_: called.append("update"))
    monkeypatch.setattr(menu, "_handle_delete", lambda *_: called.append("delete"))
    monkeypatch.setattr(menu, "_handle_toggle", lambda *_: called.append("toggle"))

    for choice in ["Update task", "Delete task", "Mark complete/incomplete"]:
        menu.main_menu_loop(
            tasks=[Task(id=1, title="x")],
            interactive=True,
            once=True,
            select_fn=lambda _: choice,
            prompt_fn=lambda _: None,
        )
    assert called == ["update", "delete", "toggle"]
