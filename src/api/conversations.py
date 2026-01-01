from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import schemas
from src.models.conversation import Conversation
from src.services import auth as auth_services
from src.models.message import Message
from src.services import db, conversation_repo, message_repo

# [Task]: T009 [From]: specs/008-chat-storage/spec.md User Story 1
# [Task]: T011 [From]: specs/008-chat-storage/spec.md User Story 1
# [Task]: T020 [From]: specs/008-chat-storage/spec.md User Story 2
# [Task]: T021 [From]: specs/008-chat-storage/spec.md User Story 2

router = APIRouter()


def _to_response(conversation: Conversation) -> schemas.ConversationCreateResponse:
    return schemas.ConversationCreateResponse(
        id=conversation.id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )


def _message_to_response(message: Message) -> schemas.MessageRead:
    return schemas.MessageRead(
        id=message.id,
        conversation_id=message.conversation_id,
        role=message.role,
        content=message.content,
        created_at=message.created_at,
    )


@router.post("/conversations", response_model=schemas.ConversationCreateResponse, status_code=201)
async def create_conversation(
    session: AsyncSession = Depends(db.get_session),
    auth_ctx: auth_services.AuthenticatedContext = Depends(auth_services.require_authorization),
) -> schemas.ConversationCreateResponse:
    conversation = await conversation_repo.create_conversation(session, owner_id=auth_ctx.user_id)
    return _to_response(conversation)


@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=schemas.MessageRead,
    status_code=status.HTTP_201_CREATED,
)
async def append_message(
    conversation_id: int,
    payload: schemas.MessageCreate,
    session: AsyncSession = Depends(db.get_session),
    auth_ctx: auth_services.AuthenticatedContext = Depends(auth_services.require_authorization),
) -> schemas.MessageRead:
    try:
        message = await message_repo.create_message(
            session,
            owner_id=auth_ctx.user_id,
            conversation_id=conversation_id,
            role=payload.role,
            content=payload.content,
        )
    except message_repo.ConversationAccessError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return _message_to_response(message)


# [Task]: T009 [From]: specs/009-message-history-read/spec.md User Story 1
@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[schemas.MessageRead],
)
async def list_messages(
    conversation_id: int,
    limit: int = 50,
    session: AsyncSession = Depends(db.get_session),
    auth_ctx: auth_services.AuthenticatedContext = Depends(auth_services.require_authorization),
) -> list[schemas.MessageRead]:
    # [Task]: T010 [From]: specs/009-message-history-read/spec.md User Story 1
    if limit <= 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="limit must be positive")
    if limit > 200:
        limit = 200
    try:
        messages = await message_repo.list_messages(
            session,
            owner_id=auth_ctx.user_id,
            conversation_id=conversation_id,
            limit=limit,
        )
    except message_repo.ConversationAccessError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    return [_message_to_response(message) for message in messages]
