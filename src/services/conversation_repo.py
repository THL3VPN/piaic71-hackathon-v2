from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.conversation import Conversation

# [Task]: T008 [From]: specs/008-chat-storage/spec.md FR-001, FR-003, FR-010


async def create_conversation(session: AsyncSession, *, owner_id: str) -> Conversation:
    """Create and persist a conversation owned by a user."""
    conversation = Conversation(user_id=owner_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation
