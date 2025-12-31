from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import schemas
from src.services import auth as auth_services
from src.services import chat_service, db, message_repo

# [Task]: T009 [From]: specs/010-stateless-chat/spec.md User Story 1

router = APIRouter()


@router.post("/chat", response_model=schemas.ChatResponse)
async def chat(
    payload: schemas.ChatRequest,
    session: AsyncSession = Depends(db.get_session),
    auth_ctx: auth_services.AuthenticatedContext = Depends(auth_services.require_authorization),
) -> schemas.ChatResponse:
    try:
        result = await chat_service.handle_chat(
            session,
            owner_id=auth_ctx.user_id,
            conversation_id=payload.conversation_id,
            message=payload.message,
        )
    except message_repo.ConversationAccessError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return schemas.ChatResponse(
        conversation_id=result.conversation_id,
        response=result.response,
        tool_calls=result.tool_calls,
    )
