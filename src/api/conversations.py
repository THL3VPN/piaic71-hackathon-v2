from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import schemas
from src.services import auth as auth_services
from src.services import db, conversation_repo

# [Task]: T009 [From]: specs/008-chat-storage/spec.md User Story 1

router = APIRouter()


@router.post("/conversations", response_model=schemas.ConversationCreateResponse, status_code=201)
async def create_conversation(
    session: AsyncSession = Depends(db.get_session),
    auth_ctx: auth_services.AuthenticatedContext = Depends(auth_services.require_authorization),
) -> schemas.ConversationCreateResponse:
    conversation = await conversation_repo.create_conversation(session, owner_id=auth_ctx.user_id)
    return schemas.ConversationCreateResponse(
        id=conversation.id,
        created_at=conversation.created_at,
        updated_at=conversation.updated_at,
    )
