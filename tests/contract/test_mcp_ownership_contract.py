from __future__ import annotations

# [Task]: T014 [From]: specs/015-mcp-server-extraction/tasks.md User Story 3

from contextlib import asynccontextmanager

import pytest
from mcp.server.fastmcp.exceptions import ToolError
from mcp.server.fastmcp.server import FastMCP

from mcp_server import tools
from src.services import db


@asynccontextmanager
async def _session_factory(engine):
    async with db.get_session_for_engine(engine) as session:
        yield session


def _unwrap_list(result: object) -> list[dict[str, object]]:
    if isinstance(result, dict) and "result" in result:
        value = result["result"]
        return value if isinstance(value, list) else []
    return result if isinstance(result, list) else []


@pytest.mark.anyio
async def test_mcp_tools_enforce_ownership(tmp_path) -> None:
    engine = db.get_engine(f"sqlite+aiosqlite:///{tmp_path / 'mcp_owner.db'}")
    await db.create_all(engine)

    mcp = FastMCP(name="Ownership MCP")
    tools.register_tools(mcp, lambda: _session_factory(engine))

    _, created = await mcp.call_tool(
        "add_task",
        {"user_id": "owner-user", "title": "Private task"},
    )
    task_id = created["task_id"]

    _, listed = await mcp.call_tool(
        "list_tasks",
        {"user_id": "intruder-user", "status": "all"},
    )
    assert _unwrap_list(listed) == []

    for tool_name, args in [
        ("complete_task", {"task_id": task_id}),
        ("delete_task", {"task_id": task_id}),
        ("update_task", {"task_id": task_id, "title": "Hacked"}),
    ]:
        with pytest.raises(ToolError) as excinfo:
            await mcp.call_tool(tool_name, {"user_id": "intruder-user", **args})
        assert "Task not found" in str(excinfo.value)

    await engine.dispose()
