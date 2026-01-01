from __future__ import annotations

import pytest

import src.services.message_repo as message_repo
from src.services import conversation_repo

# [Task]: T015 [From]: specs/008-chat-storage/spec.md User Story 2


@pytest.mark.anyio
async def test_create_message_persists_owner(session) -> None:
    conversation = await conversation_repo.create_conversation(session, owner_id="unit-user")
    message = await message_repo.create_message(
        session,
        owner_id="unit-user",
        conversation_id=conversation.id or 0,
        role="user",
        content="hello",
    )
    assert message.id is not None
    assert message.user_id == "unit-user"
    assert message.conversation_id == conversation.id
    assert message.role == "user"
    assert message.content == "hello"


@pytest.mark.anyio
async def test_create_message_forbidden_for_other_owner(session) -> None:
    conversation = await conversation_repo.create_conversation(session, owner_id="owner-a")
    with pytest.raises(message_repo.ConversationAccessError):
        await message_repo.create_message(
            session,
            owner_id="owner-b",
            conversation_id=conversation.id or 0,
            role="assistant",
            content="blocked",
        )
