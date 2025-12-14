from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: str = Field(..., min_length=1)


class TaskRead(TaskBase):
    id: int
    completed: bool
    created_at: datetime

