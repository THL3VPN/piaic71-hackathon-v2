from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel


# [Task]: T016 [From]: specs/008-chat-storage/spec.md User Story 2
class Message(SQLModel, table=True):
    """Message table persisted in the database."""

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(index=True)
    content: str
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    )
