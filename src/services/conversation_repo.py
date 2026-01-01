from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.conversation import Conversation

# [Task]: T008 [From]: specs/008-chat-storage/spec.md FR-001, FR-003, FR-010
# [Task]: T012 [From]: specs/008-chat-storage/spec.md User Story 1
# [Task]: T019 [From]: specs/008-chat-storage/spec.md User Story 2


def _new_conversation(owner_id: str) -> Conversation:
    return Conversation(user_id=owner_id)


def update_activity(conversation: Conversation) -> None:
    conversation.updated_at = datetime.now(timezone.utc)


async def create_conversation(session: AsyncSession, *, owner_id: str) -> Conversation:
    """Create and persist a conversation owned by a user."""
    conversation = _new_conversation(owner_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation
