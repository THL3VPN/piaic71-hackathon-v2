from __future__ import annotations

import pytest

import src.services.conversation_repo as conversation_repo

# [Task]: T005 [From]: specs/008-chat-storage/spec.md User Story 1


@pytest.mark.anyio
async def test_create_conversation_persists_user_and_timestamps(session) -> None:
    convo = await conversation_repo.create_conversation(session, owner_id="unit-user")
    assert convo.id is not None
    assert convo.user_id == "unit-user"
    assert convo.created_at is not None
    assert convo.updated_at is not None
