from __future__ import annotations

# [Task]: T007 [From]: specs/009-message-history-read/spec.md User Story 1

from datetime import datetime, timedelta, timezone

import pytest

from src.models.conversation import Conversation
from src.models.message import Message
from src.services import message_repo


@pytest.mark.anyio
async def test_list_messages_orders_and_checks_owner(session) -> None:
    owner_id = "owner-user"
    other_id = "other-user"
    conversation = Conversation(user_id=owner_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)

    first = Message(
        user_id=owner_id,
        conversation_id=conversation.id,
        role="user",
        content="first",
        created_at=datetime(2025, 1, 1, tzinfo=timezone.utc),
    )
    second = Message(
        user_id=owner_id,
        conversation_id=conversation.id,
        role="assistant",
        content="second",
        created_at=datetime(2025, 1, 1, 0, 0, 1, tzinfo=timezone.utc),
    )
    session.add_all([first, second])
    await session.commit()

    messages = await message_repo.list_messages(
        session,
        owner_id=owner_id,
        conversation_id=conversation.id,
        limit=50,
    )
    assert [msg.content for msg in messages] == ["first", "second"]

    with pytest.raises(message_repo.ConversationAccessError):
        await message_repo.list_messages(
            session,
            owner_id=other_id,
            conversation_id=conversation.id,
            limit=50,
        )


# [Task]: T013 [From]: specs/009-message-history-read/spec.md User Story 2
@pytest.mark.anyio
async def test_list_messages_clamps_limit(session) -> None:
    owner_id = "limit-user"
    conversation = Conversation(user_id=owner_id)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)

    base_time = datetime(2025, 1, 1, tzinfo=timezone.utc)
    messages = [
        Message(
            user_id=owner_id,
            conversation_id=conversation.id,
            role="user",
            content=f"msg-{idx}",
            created_at=base_time + timedelta(seconds=idx),
        )
        for idx in range(210)
    ]
    session.add_all(messages)
    await session.commit()

    result = await message_repo.list_messages(
        session,
        owner_id=owner_id,
        conversation_id=conversation.id,
        limit=500,
    )
    assert len(result) == 200
