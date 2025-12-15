from __future__ import annotations

import os
from typing import AsyncIterator, Mapping, Optional

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel

# Import models to ensure metadata includes all tables
from src import models  # noqa: F401

_engine: Optional[AsyncEngine] = None


def get_engine_instance() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError("Database engine has not been initialized")
    return _engine


def get_engine(database_url: str) -> AsyncEngine:
    """Create an async engine for the given database URL."""
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    is_sqlite = database_url.startswith("sqlite")
    connect_args = {"check_same_thread": False} if is_sqlite else {}
    poolclass = StaticPool if is_sqlite else None
    return create_async_engine(
        database_url,
        echo=False,
        future=True,
        connect_args=connect_args,
        poolclass=poolclass,
    )


class SessionContext:
    def __init__(self, engine: AsyncEngine) -> None:
        self._engine = engine
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> AsyncSession:
        self._session = AsyncSession(self._engine, expire_on_commit=False)
        return self._session

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session is not None:
            await self._session.close()


async def get_session() -> AsyncIterator[AsyncSession]:
    """Yield an AsyncSession bound to the configured engine (FastAPI dependency)."""
    engine = get_engine_instance()
    async with SessionContext(engine) as session:
        yield session


def get_session_for_engine(engine: AsyncEngine) -> SessionContext:
    """Return a session context manager bound to the provided test engine."""
    return SessionContext(engine)


async def create_all(engine: AsyncEngine) -> None:
    """Apply SQLModel metadata to create tables if missing."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def get_database_url(env: Mapping[str, str] | None = None) -> str:
    """Read DATABASE_URL from environment, raising if missing or blank."""
    env = env or os.environ
    value = env.get("DATABASE_URL", "").strip()
    if not value:
        raise ValueError("DATABASE_URL is required")
    return value


async def init_engine_from_env(env: Mapping[str, str] | None = None) -> AsyncEngine:
    """Create engine from env DATABASE_URL and run create_all."""
    url = get_database_url(env)
    engine = get_engine(url)
    await create_all(engine)
    global _engine
    _engine = engine
    return engine


async def dispose_engine() -> None:
    """Dispose the configured engine, if present."""
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None
