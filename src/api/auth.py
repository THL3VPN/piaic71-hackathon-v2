from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import schemas
from src.services import auth, db
from src.models.user import User


router = APIRouter()


async def _get_user_by_username(session: AsyncSession, username: str) -> User | None:
    result = await session.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


def _build_token(user: User, expires_minutes: int | None = None) -> schemas.LoginResponse:
    settings = auth.get_auth_settings()
    ttl_minutes = expires_minutes if expires_minutes and expires_minutes > 0 else settings.ttl_seconds // 60
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=ttl_minutes)).timestamp()),
    }
    token = auth.encode_token(payload)
    return schemas.LoginResponse(token=token, expires_in=ttl_minutes * 60)


@router.post("/register", response_model=schemas.RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: schemas.RegisterRequest, session: AsyncSession = Depends(db.get_session)
) -> schemas.RegisterResponse:
    existing = await _get_user_by_username(session, payload.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username already exists",
        )
    user = User(username=payload.username, password_hash=auth.hash_password(payload.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return schemas.RegisterResponse(id=user.id, username=user.username)


@router.post("/login", response_model=schemas.LoginResponse)
async def login(
    payload: schemas.LoginRequest, session: AsyncSession = Depends(db.get_session)
) -> schemas.LoginResponse:
    user = await _get_user_by_username(session, payload.username)
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials",
        )
    return _build_token(user)
