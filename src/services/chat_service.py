from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.conversation import Conversation
from src.services import conversation_repo, message_repo

# [Task]: T008 [From]: specs/010-stateless-chat/spec.md User Story 1


@dataclass(frozen=True)
class ChatResult:
    conversation_id: int
    response: str
    tool_calls: list[dict[str, object]]


def _get_owned_conversation_id(
    conversation_id: int | None,
    owner_id: str,
    conversation: Conversation | None,
) -> int:
    if conversation_id is None:
        raise message_repo.ConversationAccessError("Conversation id required")
    if conversation is None or conversation.user_id != owner_id:
        raise message_repo.ConversationAccessError("Conversation not found or not owned by user")
    return conversation_id


def _build_dummy_response(message: str) -> str:
    return f"OK (dummy): {message}"


async def handle_chat(
    session: AsyncSession,
    *,
    owner_id: str,
    conversation_id: int | None,
    message: str,
) -> ChatResult:
    if conversation_id is None:
        conversation = await conversation_repo.create_conversation(session, owner_id=owner_id)
        conversation_id = conversation.id
    else:
        conversation = await session.get(Conversation, conversation_id)
        _get_owned_conversation_id(conversation_id, owner_id, conversation)

    await message_repo.list_messages(
        session,
        owner_id=owner_id,
        conversation_id=conversation_id,
        limit=50,
    )

    await message_repo.create_message(
        session,
        owner_id=owner_id,
        conversation_id=conversation_id,
        role="user",
        content=message,
    )

    response = _build_dummy_response(message)
    await message_repo.create_message(
        session,
        owner_id=owner_id,
        conversation_id=conversation_id,
        role="assistant",
        content=response,
    )

    return ChatResult(conversation_id=conversation_id, response=response, tool_calls=[])
