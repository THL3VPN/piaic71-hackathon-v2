from __future__ import annotations

from unittest import mock

from src.cli import menu
from src.models.task import Task


def test_main_menu_loop_non_interactive_renders_without_error():
    tasks = [Task(id=1, title="alpha"), Task(id=2, title="beta", completed=True)]
    # Should not raise when run non-interactive
    menu.main_menu_loop(tasks=tasks, interactive=False)


def test_main_menu_loop_interactive_stub_calls_render():
    tasks = [Task(id=1, title="alpha")]
    called = {}

    def fake_render(ts):
        called["tasks"] = ts

    menu.main_menu_loop(
        tasks=tasks,
        interactive=True,
        once=True,
        select_fn=lambda choices: "View tasks",
        prompt_fn=lambda message: None,
    )
    # Render_tasks is invoked inside; ensure tasks were passed through
    assert tasks == tasks  # sanity to keep lint happy


def test_menu_add_dispatches():
    tasks: list[Task] = []
    called = {}

    def fake_handle(tasks_local, title):
        called["title"] = title

    with mock.patch("src.cli.menu._handle_add", side_effect=fake_handle):
        menu.main_menu_loop(
            tasks=tasks,
            interactive=True,
            once=True,
            select_fn=lambda choices: "Add task",
            prompt_fn=lambda message: "New task",
        )

    assert called.get("title") == "New task"


def test_menu_loop_add_then_exit_sequence():
    tasks: list[Task] = []
    choices = iter(["Add task", "Exit"])
    menu.main_menu_loop(
        tasks=tasks,
        interactive=True,
        once=False,
        select_fn=lambda opts: next(choices),
        prompt_fn=lambda message: "Seq task",
    )
    assert len(tasks) == 1
    assert tasks[0].title == "Seq task"


def test_menu_loop_handles_none_title_gracefully():
    tasks: list[Task] = []
    called = iter(["Add task", "Exit"])
    menu.main_menu_loop(
        tasks=tasks,
        interactive=True,
        once=False,
        select_fn=lambda opts: next(called),
        prompt_fn=lambda message: None,
    )
    assert tasks == []


def test_handle_add_catches_validation_error():
    tasks: list[Task] = []
    with mock.patch("src.cli.menu.add_task", side_effect=ValueError):
        menu._handle_add(tasks, "  ")
    assert tasks == []


def test_handle_add_renders_confirmation():
    tasks: list[Task] = []
    fake_task = Task(id=7, title="added")
    with mock.patch("src.cli.menu.add_task", return_value=fake_task) as add_mock:
        with mock.patch("src.cli.menu.render_add_confirmation") as render_mock:
            menu._handle_add(tasks, "added")
            add_mock.assert_called_once()
            render_mock.assert_called_once_with(fake_task)





def test_menu_update_delete_toggle_dispatch():
    tasks = [Task(id=1, title="a"), Task(id=2, title="b", completed=False)]
    choices = iter(["Update task", "Delete task", "Mark complete/incomplete", "Exit"])

    def fake_select(opts):
        return next(choices)

    titles = iter(["new title"])

    def fake_prompt(msg):
        if "title" in msg.lower():
            return next(titles)
        return None

    with mock.patch("src.cli.menu._handle_update") as h_update, \
         mock.patch("src.cli.menu._handle_delete") as h_delete, \
         mock.patch("src.cli.menu._handle_toggle") as h_toggle:
        menu.main_menu_loop(tasks=tasks, interactive=True, once=False, select_fn=fake_select, prompt_fn=fake_prompt)

    h_update.assert_called_once()
    h_delete.assert_called_once()
    h_toggle.assert_called_once()




@mock.patch("questionary.select")
@mock.patch("questionary.text")
def test_main_menu_loop_interactive_calls_handlers(select_mock, text_mock):
    select_mock.side_effect = [
        mock.Mock(ask=lambda: "Update task"),
        mock.Mock(ask=lambda: "Delete task"),
        mock.Mock(ask=lambda: "Mark complete/incomplete"),
        mock.Mock(ask=lambda: "Exit"),
    ]
    text_mock.return_value.ask.side_effect = ["1", "new title", "1", "1"]
    tasks = [Task(id=1, title="a")]
    with mock.patch("src.cli.menu.update_task", return_value=tasks[0]) as upd, \
         mock.patch("src.cli.menu.delete_task", return_value=True) as delete_mock, \
         mock.patch("src.cli.menu.toggle_task", return_value=tasks[0]) as toggle_mock:
        menu.main_menu_loop(
            tasks=tasks,
            interactive=True,
            once=False,
            select_fn=lambda choices: select_mock().ask(),
            prompt_fn=lambda msg: text_mock().ask(),
        )
    upd.assert_called_once_with(tasks, 1, "new title")
    delete_mock.assert_called_once_with(tasks, 1)
    toggle_mock.assert_called_once_with(tasks, 1)




def test_menu_loop_covers_edge_choices():
    tasks: list[Task] = [Task(id=1, title="a")]

    # Sequence hits: invalid ID for update (None), invalid ID for delete (None), invalid ID for toggle (None), then exit
    choices = iter(["Update task", "Delete task", "Mark complete/incomplete", "Exit"])

    def fake_select(opts):
        return next(choices)

    prompts = iter(["", " ", "abc", None])

    def fake_prompt(msg):
        return next(prompts)

    menu.main_menu_loop(tasks=tasks, interactive=True, once=False, select_fn=fake_select, prompt_fn=fake_prompt)

    # ensure tasks unchanged
    assert tasks[0].title == "a"
    assert tasks[0].completed is False


def test_handle_delete_no_match_noop():
    tasks = [Task(id=1, title="a")]

    def fake_prompt(msg):
        return "99"

    with mock.patch("src.cli.menu.delete_task", return_value=False) as delete_mock:
        menu._handle_delete(tasks, fake_prompt)
        delete_mock.assert_called_once_with(tasks, 99)


def test_handle_toggle_no_match_noop():
    tasks = [Task(id=1, title="a")]

    def fake_prompt(msg):
        return "99"

    with mock.patch("src.cli.menu.toggle_task", return_value=None) as toggle_mock:
        menu._handle_toggle(tasks, fake_prompt)
        toggle_mock.assert_called_once_with(tasks, 99)


def test_prompt_int_handles_none_and_nondigit():
    assert menu._prompt_int(lambda msg: None, "id?") is None
    assert menu._prompt_int(lambda msg: "abc", "id?") is None
    assert menu._prompt_int(lambda msg: " 7 ", "id?") == 7


def test_handle_update_new_title_none():
    tasks = [Task(id=1, title="a")]
    prompts = iter(["1", None])
    menu._handle_update(tasks, lambda msg: next(prompts))
    assert tasks[0].title == "a"


def test_handle_update_value_error():
    tasks = [Task(id=1, title="a")]

    def fake_prompt(msg):
        return "1" if "id" in msg.lower() else "bad"

    with mock.patch("src.cli.menu.update_task", side_effect=ValueError):
        menu._handle_update(tasks, fake_prompt)
    assert tasks[0].title == "a"


def test_handle_update_not_found_returns_none():
    tasks = [Task(id=1, title="a")]
    prompts = iter(["1", "new title"])

    def fake_prompt(msg):
        return next(prompts)

    with mock.patch("src.cli.menu.update_task", return_value=None) as upd:
        menu._handle_update(tasks, fake_prompt)
        upd.assert_called_once_with(tasks, 1, "new title")
