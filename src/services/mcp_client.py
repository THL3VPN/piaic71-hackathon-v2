from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from urllib.parse import urlparse, urlunparse

from mcp.client.session import ClientSession
from mcp.client.sse import sse_client
import mcp.types as mcp_types

# [Task]: T011 [From]: specs/015-mcp-server-extraction/tasks.md User Story 2

logger = logging.getLogger(__name__)

MCP_SERVER_URL_ENV = "MCP_SERVER_URL"


@dataclass(frozen=True)
class McpClientSettings:
    server_url: str


class McpConfigError(ValueError):
    """Raised when MCP client configuration is invalid."""


class McpClientError(RuntimeError):
    """Raised when MCP tool calls fail."""


def _normalize_sse_url(server_url: str) -> str:
    trimmed = server_url.strip()
    if not trimmed:
        raise McpConfigError(f"{MCP_SERVER_URL_ENV} is required")

    parsed = urlparse(trimmed)
    path = parsed.path or ""

    if path.endswith("/sse"):
        sse_path = path
    elif path.endswith("/"):
        sse_path = f"{path}sse"
    elif path:
        sse_path = f"{path}/sse"
    else:
        sse_path = "/sse"

    return urlunparse(parsed._replace(path=sse_path))


def load_mcp_settings(env: dict[str, str] | None = None) -> McpClientSettings:
    env = env or os.environ
    server_url = env.get(MCP_SERVER_URL_ENV)
    if not server_url:
        raise McpConfigError(f"{MCP_SERVER_URL_ENV} is required")
    return McpClientSettings(server_url=server_url)


@asynccontextmanager
async def _open_session(server_url: str) -> AsyncIterator[ClientSession]:
    async with sse_client(_normalize_sse_url(server_url)) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session


def _extract_error_message(result: mcp_types.CallToolResult) -> str:
    if result.structuredContent:
        message = result.structuredContent.get("message")
        if isinstance(message, str) and message.strip():
            return message
    if result.content:
        first = result.content[0]
        text = getattr(first, "text", None)
        if isinstance(text, str) and text.strip():
            return text
    return "MCP tool call failed"


def _extract_tool_result(result: mcp_types.CallToolResult) -> Any:
    if result.structuredContent is not None:
        if isinstance(result.structuredContent, dict):
            if set(result.structuredContent.keys()) == {"result"}:
                return result.structuredContent["result"]
        return result.structuredContent
    if not result.content:
        return {}
    first = result.content[0]
    text = getattr(first, "text", None)
    if isinstance(text, str) and text.strip():
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"message": text}
    return {}


async def _call_tool(name: str, arguments: dict[str, Any]) -> Any:
    settings = load_mcp_settings()
    logger.info("Calling MCP tool %s", name)
    async with _open_session(settings.server_url) as session:
        result = await session.call_tool(name, arguments)
        if result.isError:
            raise McpClientError(_extract_error_message(result))
        return _extract_tool_result(result)


async def call_add_task(*, user_id: str, title: str, description: str | None = None) -> dict[str, Any]:
    return await _call_tool(
        "add_task",
        {"user_id": user_id, "title": title, "description": description},
    )


async def call_list_tasks(*, user_id: str, status: str | None = None) -> Any:
    return await _call_tool(
        "list_tasks",
        {"user_id": user_id, "status": status},
    )


async def call_complete_task(*, user_id: str, task_id: int) -> dict[str, Any]:
    return await _call_tool(
        "complete_task",
        {"user_id": user_id, "task_id": task_id},
    )


async def call_delete_task(*, user_id: str, task_id: int) -> dict[str, Any]:
    return await _call_tool(
        "delete_task",
        {"user_id": user_id, "task_id": task_id},
    )


async def call_update_task(
    *,
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None,
) -> dict[str, Any]:
    return await _call_tool(
        "update_task",
        {"user_id": user_id, "task_id": task_id, "title": title, "description": description},
    )
