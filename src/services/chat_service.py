from __future__ import annotations

import json
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.conversation import Conversation
from src.services import agent_runtime, chat_provider, conversation_repo, message_repo

# [Task]: T008 [From]: specs/010-stateless-chat/spec.md User Story 1
# [Task]: T010 [From]: specs/012-ai-agent-integration/spec.md User Story 1


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


def _format_tool_call_payload(tool_calls: list[dict[str, object]]) -> str:
    return f"[tool_calls]{json.dumps(tool_calls, separators=(',', ':'))}"


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

    settings = chat_provider.load_provider_settings()
    history_messages = await message_repo.list_messages(
        session,
        owner_id=owner_id,
        conversation_id=conversation_id,
        limit=settings.history_limit,
    )

    await message_repo.create_message(
        session,
        owner_id=owner_id,
        conversation_id=conversation_id,
        role="user",
        content=message,
    )

    history = [{"role": item.role, "content": item.content} for item in history_messages]
    agent_result = await agent_runtime.run_agent(
        user_message=message,
        history=history,
        user_id=owner_id,
        session=session,
    )
    response = agent_result.response
    await message_repo.create_message(
        session,
        owner_id=owner_id,
        conversation_id=conversation_id,
        role="assistant",
        content=response,
    )
    if agent_result.tool_calls:
        await message_repo.create_message(
            session,
            owner_id=owner_id,
            conversation_id=conversation_id,
            role="assistant",
            content=_format_tool_call_payload(agent_result.tool_calls),
        )

    return ChatResult(
        conversation_id=conversation_id,
        response=response,
        tool_calls=agent_result.tool_calls,
    )
