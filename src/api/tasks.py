from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services import auth as auth_services

from src.api import schemas
from src.services import db, task_repo

router = APIRouter(dependencies=[Depends(auth_services.require_authorization)])

@router.post(
    "/tasks",
    response_model=schemas.TaskRead,
    status_code=201,
)
async def create_task(
    payload: schemas.TaskCreate,
    session: AsyncSession = Depends(db.get_session),
    _: auth_services.AuthenticatedContext = Depends(auth_services.get_authenticated_context),
) -> schemas.TaskRead:
    task = await task_repo.create_task(session, payload.title, payload.description)
    return task

@router.get(
    "/tasks",
    response_model=list[schemas.TaskRead],
)
async def list_tasks(
    session: AsyncSession = Depends(db.get_session),
    _: auth_services.AuthenticatedContext = Depends(auth_services.get_authenticated_context),
) -> list[schemas.TaskRead]:
    tasks = await task_repo.list_tasks(session)
    return tasks


@router.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskRead,
)
async def get_task(
    task_id: int,
    session: AsyncSession = Depends(db.get_session),
    _: auth_services.AuthenticatedContext = Depends(auth_services.get_authenticated_context),
) -> schemas.TaskRead:
    task = await task_repo.get_task_or_404(session, task_id)
    return task


@router.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskRead,
)
async def update_task(
    task_id: int,
    payload: schemas.TaskUpdate,
    session: AsyncSession = Depends(db.get_session),
    _: auth_services.AuthenticatedContext = Depends(auth_services.get_authenticated_context),
) -> schemas.TaskRead:
    task = await task_repo.update_task(session, task_id, payload.title, payload.description)
    return task


@router.delete(
    "/tasks/{task_id}",
    status_code=204,
)
async def delete_task(
    task_id: int,
    session: AsyncSession = Depends(db.get_session),
    _: auth_services.AuthenticatedContext = Depends(auth_services.get_authenticated_context),
) -> None:
    await task_repo.delete_task(session, task_id)


@router.patch(
    "/tasks/{task_id}/complete",
    response_model=schemas.TaskRead,
)
async def toggle_task_completion(
    task_id: int,
    session: AsyncSession = Depends(db.get_session),
    _: auth_services.AuthenticatedContext = Depends(auth_services.get_authenticated_context),
) -> schemas.TaskRead:
    task = await task_repo.toggle_task_completion(session, task_id)
    return task
