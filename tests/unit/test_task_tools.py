from __future__ import annotations

import pytest

from src.services import task_repo, task_tools


@pytest.mark.anyio
async def test_add_task_creates_task_and_returns_result(session) -> None:
    result = await task_tools.add_task(
        session,
        user_id="user-1",
        title="  New task  ",
        description="details",
    )

    assert result["status"] == "created"
    assert result["title"] == "New task"
    assert isinstance(result["task_id"], int)

    tasks = await task_repo.list_tasks(session, owner_id="user-1")
    assert len(tasks) == 1
    assert tasks[0].title == "New task"
    assert tasks[0].description == "details"
    assert tasks[0].completed is False


@pytest.mark.anyio
async def test_list_tasks_defaults_to_all_and_filters_owner(session) -> None:
    owned = await task_repo.create_task(session, owner_id="user-1", title="Owned")
    await task_repo.create_task(session, owner_id="user-2", title="Other")

    result = await task_tools.list_tasks(session, user_id="user-1")

    assert result == [
        {"id": owned.id, "title": "Owned", "completed": False},
    ]


@pytest.mark.anyio
async def test_list_tasks_supports_status_filters(session) -> None:
    pending = await task_repo.create_task(session, owner_id="user-1", title="Pending")
    completed = await task_repo.create_task(session, owner_id="user-1", title="Done")
    await task_repo.toggle_task_completion(session, completed.id, owner_id="user-1")

    completed_result = await task_tools.list_tasks(session, user_id="user-1", status="completed")
    pending_result = await task_tools.list_tasks(session, user_id="user-1", status="pending")

    assert completed_result == [
        {"id": completed.id, "title": "Done", "completed": True},
    ]
    assert pending_result == [
        {"id": pending.id, "title": "Pending", "completed": False},
    ]


@pytest.mark.anyio
async def test_complete_task_marks_task_completed(session) -> None:
    task = await task_repo.create_task(session, owner_id="user-1", title="Finish")

    result = await task_tools.complete_task(session, user_id="user-1", task_id=task.id)

    assert result == {"task_id": task.id, "status": "completed", "title": "Finish"}
    refreshed = await task_repo.get_task(session, task.id)
    assert refreshed is not None
    assert refreshed.completed is True


@pytest.mark.anyio
async def test_delete_task_removes_task(session) -> None:
    task = await task_repo.create_task(session, owner_id="user-1", title="Remove")

    result = await task_tools.delete_task(session, user_id="user-1", task_id=task.id)

    assert result == {"task_id": task.id, "status": "deleted", "title": "Remove"}
    assert await task_repo.get_task(session, task.id) is None


@pytest.mark.anyio
async def test_update_task_updates_title_and_description(session) -> None:
    task = await task_repo.create_task(session, owner_id="user-1", title="Old", description="before")

    result = await task_tools.update_task(
        session,
        user_id="user-1",
        task_id=task.id,
        title="New",
        description="after",
    )

    assert result == {"task_id": task.id, "status": "updated", "title": "New"}
    refreshed = await task_repo.get_task(session, task.id)
    assert refreshed is not None
    assert refreshed.title == "New"
    assert refreshed.description == "after"


@pytest.mark.anyio
async def test_add_task_rejects_empty_title(session) -> None:
    with pytest.raises(task_tools.InvalidInput):
        await task_tools.add_task(session, user_id="user-1", title="   ")


@pytest.mark.anyio
async def test_list_tasks_rejects_invalid_status(session) -> None:
    with pytest.raises(task_tools.InvalidInput):
        await task_tools.list_tasks(session, user_id="user-1", status="unknown")


@pytest.mark.anyio
async def test_update_task_rejects_empty_payload(session) -> None:
    task = await task_repo.create_task(session, owner_id="user-1", title="Keep")

    with pytest.raises(task_tools.InvalidInput):
        await task_tools.update_task(session, user_id="user-1", task_id=task.id)


@pytest.mark.anyio
async def test_cross_user_access_raises_unauthorized(session) -> None:
    task = await task_repo.create_task(session, owner_id="user-1", title="Private")

    with pytest.raises(task_tools.UnauthorizedAccess):
        await task_tools.complete_task(session, user_id="user-2", task_id=task.id)

    with pytest.raises(task_tools.UnauthorizedAccess):
        await task_tools.delete_task(session, user_id="user-2", task_id=task.id)

    with pytest.raises(task_tools.UnauthorizedAccess):
        await task_tools.update_task(session, user_id="user-2", task_id=task.id, title="Nope")


def test_task_tools_module_has_no_api_imports() -> None:
    assert "fastapi" not in task_tools.__dict__
    assert "starlette" not in task_tools.__dict__
