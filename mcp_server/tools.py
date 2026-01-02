from __future__ import annotations

from collections.abc import AsyncIterator, Callable
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.fastmcp.server import FastMCP

from src.services import task_tools

# [Task]: T002 [From]: specs/015-mcp-server-extraction/tasks.md Phase 1
# [Task]: T003 [From]: specs/015-mcp-server-extraction/tasks.md Phase 2
# [Task]: T007 [From]: specs/015-mcp-server-extraction/tasks.md User Story 1
# [Task]: T016 [From]: specs/015-mcp-server-extraction/tasks.md User Story 3

SessionFactory = Callable[[], AsyncIterator[AsyncSession]]


def _map_tool_error(error: task_tools.TaskToolError) -> ToolError:
    message = str(error)
    if isinstance(error, task_tools.UnauthorizedAccess):
        message = "Task not found"
    return ToolError(message)


def register_tools(mcp: FastMCP, session_factory: SessionFactory) -> None:
    @mcp.tool(name="add_task", description="Create a task for a user.")
    async def add_task(user_id: str, title: str, description: str | None = None) -> dict[str, Any]:
        try:
            async with session_factory() as session:
                return await task_tools.add_task(
                    session,
                    user_id=user_id,
                    title=title,
                    description=description,
                )
        except task_tools.TaskToolError as exc:
            raise _map_tool_error(exc) from exc

    @mcp.tool(name="list_tasks", description="List tasks for a user.")
    async def list_tasks(user_id: str, status: str | None = None) -> list[dict[str, Any]]:
        try:
            async with session_factory() as session:
                return await task_tools.list_tasks(
                    session,
                    user_id=user_id,
                    status=status,
                )
        except task_tools.TaskToolError as exc:
            raise _map_tool_error(exc) from exc

    @mcp.tool(name="complete_task", description="Mark a task as completed.")
    async def complete_task(user_id: str, task_id: int) -> dict[str, Any]:
        try:
            async with session_factory() as session:
                return await task_tools.complete_task(
                    session,
                    user_id=user_id,
                    task_id=task_id,
                )
        except task_tools.TaskToolError as exc:
            raise _map_tool_error(exc) from exc

    @mcp.tool(name="delete_task", description="Delete a task.")
    async def delete_task(user_id: str, task_id: int) -> dict[str, Any]:
        try:
            async with session_factory() as session:
                return await task_tools.delete_task(
                    session,
                    user_id=user_id,
                    task_id=task_id,
                )
        except task_tools.TaskToolError as exc:
            raise _map_tool_error(exc) from exc

    @mcp.tool(name="update_task", description="Update task title/description.")
    async def update_task(
        user_id: str,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> dict[str, Any]:
        try:
            async with session_factory() as session:
                return await task_tools.update_task(
                    session,
                    user_id=user_id,
                    task_id=task_id,
                    title=title,
                    description=description,
                )
        except task_tools.TaskToolError as exc:
            raise _map_tool_error(exc) from exc
