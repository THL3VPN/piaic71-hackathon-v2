from __future__ import annotations

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.services import task_repo


class DummySession:
    async def get(self, model, id):
        return None

    async def delete(self, instance):
        pass

    async def commit(self):
        pass

    async def refresh(self, instance):
        pass
    async def delete(self, instance):
        pass

    async def commit(self):  # pragma: no cover
        pass

    async def refresh(self, instance):  # pragma: no cover
        pass


@pytest.mark.anyio
async def test_get_task_or_404_missing(monkeypatch):
    session = DummySession()

    async def fake_get(session_obj: AsyncSession, task_id: int):
        return None

    monkeypatch.setattr(task_repo, "get_task", fake_get)

    with pytest.raises(HTTPException) as exc_info:
        await task_repo.get_task_or_404(session, 42)  # type: ignore[arg-type]
    assert exc_info.value.status_code == 404


@pytest.mark.anyio
async def test_get_task_or_404_success(monkeypatch):
    session = DummySession()
    fake_task = object()

    async def fake_get(session_obj: AsyncSession, task_id: int):
        return fake_task

    monkeypatch.setattr(task_repo, "get_task", fake_get)

    result = await task_repo.get_task_or_404(session, 42)  # type: ignore[arg-type]
    assert result is fake_task


@pytest.mark.anyio
async def test_update_task_requires_title(monkeypatch):
    session = DummySession()

    fake_task = type("T", (), {"id": 1, "title": "OK", "description": None, "completed": False, "owner_id": "user-1"})

    async def fake_get(session_obj: AsyncSession, task_id: int):
        return fake_task

    monkeypatch.setattr(task_repo, "get_task", fake_get)

    with pytest.raises(ValueError):
        await task_repo.update_task(session, fake_task.id, owner_id="user-1", title="   ", description="desc")  # type: ignore[arg-type]


@pytest.mark.anyio
async def test_update_task_returns_trimmed(monkeypatch):
    session = DummySession()
    fake_task = type("T", (), {"id": 1, "title": "OK", "description": None, "completed": False, "owner_id": "user-1"})

    async def fake_get(session_obj: AsyncSession, task_id: int):
        return fake_task

    monkeypatch.setattr(task_repo, "get_task", fake_get)

    updated = await task_repo.update_task(
        session, fake_task.id, owner_id="user-1", title="  trimmed  ", description="desc"
    )
    assert updated.title == "trimmed"
    assert updated.description == "desc"


@pytest.mark.anyio
async def test_delete_task(monkeypatch):
    session = DummySession()
    fake_task = type("T", (), {"id": 1, "owner_id": "user-1"})

    async def fake_owned(session_obj: AsyncSession, task_id: int, *, owner_id: str):
        return fake_task

    called = []

    async def fake_delete(instance):
        called.append(instance)

    monkeypatch.setattr(task_repo, "get_owned_task_or_404", fake_owned)
    session.delete = fake_delete  # type: ignore[attr-defined]

    await task_repo.delete_task(session, fake_task.id, owner_id="user-1")
    assert called == [fake_task]


@pytest.mark.anyio
async def test_toggle_task_completion(monkeypatch):
    session = DummySession()
    fake_task = type("T", (), {"id": 1, "completed": False, "owner_id": "user-1"})

    async def fake_owned(session_obj: AsyncSession, task_id: int, *, owner_id: str):
        return fake_task

    monkeypatch.setattr(task_repo, "get_owned_task_or_404", fake_owned)

    toggled = await task_repo.toggle_task_completion(session, fake_task.id, owner_id="user-1")
    assert toggled.completed is True
