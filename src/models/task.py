from __future__ import annotations

from datetime import datetime, timezone

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class Task(SQLModel, table=True):
    """Task table persisted in the database."""

    id: int | None = Field(default=None, primary_key=True)
    owner_id: str = Field(index=True, nullable=False)
    title: str = Field(index=True)
    description: str | None = None
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def __init__(self, **data: object) -> None:
        title = data.get("title")
        if isinstance(title, str):
            trimmed = title.strip()
            if not trimmed:
                raise ValueError("title cannot be empty")
            data["title"] = trimmed
        super().__init__(**data)
