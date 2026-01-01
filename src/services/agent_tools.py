from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.services import task_tools

# [Task]: T004 [From]: specs/013-agent-tool-calls/spec.md User Story 1
# [Task]: T008 [From]: specs/013-agent-tool-calls/spec.md User Story 1


@dataclass(frozen=True)
class AgentTool:
    name: str
    description: str
    input_schema: dict[str, object]
    handler: Callable[[AsyncSession, str, dict[str, Any]], Awaitable[dict[str, object]]]


async def _add_task(session: AsyncSession, user_id: str, args: dict[str, Any]) -> dict[str, object]:
    return await task_tools.add_task(
        session,
        user_id=user_id,
        title=str(args.get("title", "")),
        description=args.get("description"),
    )


async def _list_tasks(session: AsyncSession, user_id: str, args: dict[str, Any]) -> dict[str, object]:
    status = args.get("status")
    results = await task_tools.list_tasks(session, user_id=user_id, status=status)
    return {"tasks": results}


async def _complete_task(session: AsyncSession, user_id: str, args: dict[str, Any]) -> dict[str, object]:
    task_id = int(args.get("task_id", 0))
    return await task_tools.complete_task(session, user_id=user_id, task_id=task_id)


async def _delete_task(session: AsyncSession, user_id: str, args: dict[str, Any]) -> dict[str, object]:
    task_id = int(args.get("task_id", 0))
    return await task_tools.delete_task(session, user_id=user_id, task_id=task_id)


async def _update_task(session: AsyncSession, user_id: str, args: dict[str, Any]) -> dict[str, object]:
    task_id = int(args.get("task_id", 0))
    title = args.get("title")
    description = args.get("description")
    return await task_tools.update_task(
        session,
        user_id=user_id,
        task_id=task_id,
        title=title,
        description=description,
    )


def build_task_tools(*, session: AsyncSession, user_id: str) -> list[AgentTool]:
    _ = (session, user_id)
    return [
        AgentTool(
            name="add_task",
            description="Create a new task for the user.",
            input_schema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["title"],
            },
            handler=_add_task,
        ),
        AgentTool(
            name="list_tasks",
            description="List tasks for the user with optional status filtering.",
            input_schema={
                "type": "object",
                "properties": {"status": {"type": "string"}},
            },
            handler=_list_tasks,
        ),
        AgentTool(
            name="complete_task",
            description="Mark a task as completed.",
            input_schema={
                "type": "object",
                "properties": {"task_id": {"type": "integer"}},
                "required": ["task_id"],
            },
            handler=_complete_task,
        ),
        AgentTool(
            name="update_task",
            description="Update a task title or description.",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["task_id"],
            },
            handler=_update_task,
        ),
        AgentTool(
            name="delete_task",
            description="Delete a task by id.",
            input_schema={
                "type": "object",
                "properties": {"task_id": {"type": "integer"}},
                "required": ["task_id"],
            },
            handler=_delete_task,
        ),
    ]
