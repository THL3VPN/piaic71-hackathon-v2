from __future__ import annotations

from datetime import datetime

from sqlmodel import Column, DateTime, Field, SQLModel, UniqueConstraint


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("username", name="uq_users_username"),)

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password_hash: str
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), default=datetime.utcnow)
    )
