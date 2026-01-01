from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

# [Task]: T007 [From]: specs/008-chat-storage/spec.md User Story 1
# [Task]: T017 [From]: specs/008-chat-storage/spec.md User Story 2


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


class ConversationCreateResponse(SQLModel):
    id: int
    created_at: datetime
    updated_at: datetime


class MessageCreate(SQLModel):
    role: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)


class MessageRead(SQLModel):
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime


# [Task]: T004 [From]: specs/010-stateless-chat/spec.md User Story 1
class ChatRequest(SQLModel):
    conversation_id: int | None = None
    message: str = Field(..., min_length=1)


# [Task]: T004 [From]: specs/010-stateless-chat/spec.md User Story 1
class ChatResponse(SQLModel):
    conversation_id: int
    response: str
    tool_calls: list[dict[str, object]]
class RegisterRequest(SQLModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)


class RegisterResponse(SQLModel):
    id: int
    username: str


class LoginRequest(SQLModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)


class LoginResponse(SQLModel):
    token: str
    token_type: str = "bearer"
    expires_in: int | None = None
