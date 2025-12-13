from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()

@router.get("/tasks")
async def list_tasks():
    """Stub router for task list endpoint."""
    return []
