from __future__ import annotations

import os
from contextlib import asynccontextmanager
from typing import AsyncIterator, Mapping

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel


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


@asynccontextmanager
async def get_session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """Yield an AsyncSession bound to the provided engine."""
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_maker() as session:
        yield session


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
    return engine
