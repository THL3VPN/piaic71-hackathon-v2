from __future__ import annotations

from contextlib import asynccontextmanager
import os
from typing import AsyncIterator
from urllib.parse import urlparse

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from mcp.server.fastmcp.server import FastMCP

from src.services import db
from mcp_server import tools

# [Task]: T002 [From]: specs/015-mcp-server-extraction/tasks.md Phase 1
# [Task]: T004 [From]: specs/015-mcp-server-extraction/tasks.md Phase 2

_engine: AsyncEngine | None = None


def _set_engine(engine: AsyncEngine) -> None:
    global _engine
    _engine = engine


def _get_engine() -> AsyncEngine:
    if _engine is None:
        raise RuntimeError("MCP database engine not initialized")
    return _engine


@asynccontextmanager
async def lifespan(_: FastMCP) -> AsyncIterator[None]:
    engine = db.get_engine(db.get_database_url())
    await db.create_all(engine)
    _set_engine(engine)
    try:
        yield
    finally:
        await engine.dispose()
        _set_engine(None)


@asynccontextmanager
async def session_scope() -> AsyncIterator[AsyncSession]:
    async with db.get_session_for_engine(_get_engine()) as session:
        yield session


_DEFAULT_HOST = "127.0.0.1"
_DEFAULT_PORT = 9000


def _read_mcp_server_url() -> tuple[str, int]:
    raw = os.getenv("MCP_SERVER_URL")
    if not raw:
        return _DEFAULT_HOST, _DEFAULT_PORT
    parsed = urlparse(raw)
    host = parsed.hostname or _DEFAULT_HOST
    port = parsed.port or _DEFAULT_PORT
    return host, port


_HOST, _PORT = _read_mcp_server_url()

mcp = FastMCP(
    name="Task MCP",
    instructions="Task tool server for MCP-backed task operations.",
    lifespan=lifespan,
    host=_HOST,
    port=_PORT,
)

tools.register_tools(mcp, session_scope)


if __name__ == "__main__":
    mcp.run(transport="sse")
