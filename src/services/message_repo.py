from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.conversation import Conversation
from src.models.message import Message
from src.services import conversation_repo

# [Task]: T018 [From]: specs/008-chat-storage/spec.md User Story 2
# [Task]: T022 [From]: specs/008-chat-storage/spec.md User Story 2


class ConversationAccessError(Exception):
    """Raised when a conversation is missing or not owned by the user."""


def _get_owned_conversation(conversation: Conversation | None, owner_id: str) -> Conversation:
    if conversation is None or conversation.user_id != owner_id:
        raise ConversationAccessError("Conversation not found or not owned by user")
    return conversation


async def create_message(
    session: AsyncSession,
    *,
    owner_id: str,
    conversation_id: int,
    role: str,
    content: str,
) -> Message:
    """Create and persist a message after verifying conversation ownership."""
    conversation = _get_owned_conversation(
        await session.get(Conversation, conversation_id),
        owner_id,
    )

    message = Message(
        user_id=owner_id,
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    conversation_repo.update_activity(conversation)
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


# [Task]: T008 [From]: specs/009-message-history-read/spec.md User Story 1
async def list_messages(
    session: AsyncSession,
    *,
    owner_id: str,
    conversation_id: int,
    limit: int,
) -> list[Message]:
    """Return ordered messages for a conversation after ownership verification."""
    # [Task]: T014 [From]: specs/009-message-history-read/spec.md User Story 2
    if limit > 200:
        limit = 200
    _get_owned_conversation(await session.get(Conversation, conversation_id), owner_id)
    stmt = (
        select(Message)
        .where(
            Message.conversation_id == conversation_id,
            Message.user_id == owner_id,
        )
        .order_by(Message.created_at, Message.id)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())
