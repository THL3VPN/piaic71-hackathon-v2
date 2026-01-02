from __future__ import annotations

# [Task]: T007 [From]: specs/010-stateless-chat/spec.md User Story 1
# [Task]: T021 [From]: specs/013-agent-tool-calls/tasks.md Align agent chat tests

import pytest

from src.services import chat_service, message_repo


@pytest.mark.anyio
async def test_chat_service_creates_conversation_and_messages(session) -> None:
    owner_id = "chat-user"
    result = await chat_service.handle_chat(
        session,
        owner_id=owner_id,
        conversation_id=None,
        message="Hello",
    )
    assert result.conversation_id is not None
    assert isinstance(result.response, str)
    assert result.response
    assert result.tool_calls == []

    messages = await message_repo.list_messages(
        session,
        owner_id=owner_id,
        conversation_id=result.conversation_id,
        limit=50,
    )
    assert len(messages) == 2


# [Task]: T013 [From]: specs/010-stateless-chat/spec.md User Story 2
@pytest.mark.anyio
async def test_chat_service_enforces_ownership(session) -> None:
    owner_id = "owner-user"
    other_id = "other-user"
    conversation = await chat_service.handle_chat(
        session,
        owner_id=owner_id,
        conversation_id=None,
        message="Hello",
    )

    with pytest.raises(message_repo.ConversationAccessError):
        await chat_service.handle_chat(
            session,
            owner_id=other_id,
            conversation_id=conversation.conversation_id,
            message="Oops",
        )


# [Task]: T018 [From]: specs/010-stateless-chat/spec.md User Story 3
@pytest.mark.anyio
async def test_chat_service_reuses_history(session) -> None:
    owner_id = "history-user"
    first = await chat_service.handle_chat(
        session,
        owner_id=owner_id,
        conversation_id=None,
        message="First",
    )
    second = await chat_service.handle_chat(
        session,
        owner_id=owner_id,
        conversation_id=first.conversation_id,
        message="Second",
    )
    assert second.conversation_id == first.conversation_id

    messages = await message_repo.list_messages(
        session,
        owner_id=owner_id,
        conversation_id=first.conversation_id,
        limit=50,
    )
    assert len(messages) == 4
