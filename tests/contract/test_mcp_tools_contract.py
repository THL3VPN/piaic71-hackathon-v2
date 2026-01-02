from __future__ import annotations

# [Task]: T005 [From]: specs/015-mcp-server-extraction/spec.md User Story 1

from contextlib import asynccontextmanager

import pytest
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
async def test_mcp_tool_payload_shapes(tmp_path) -> None:
    engine = db.get_engine(f"sqlite+aiosqlite:///{tmp_path / 'mcp.db'}")
    await db.create_all(engine)

    mcp = FastMCP(name="Test MCP")
    tools.register_tools(mcp, lambda: _session_factory(engine))

    _, created = await mcp.call_tool(
        "add_task",
        {"user_id": "contract-user", "title": "Buy groceries", "description": "Milk"},
    )
    assert set(created.keys()) == {"task_id", "status", "title"}
    assert created["status"] == "created"

    _, listed_raw = await mcp.call_tool("list_tasks", {"user_id": "contract-user", "status": "all"})
    listed = _unwrap_list(listed_raw)
    assert listed and {"id", "title", "completed"}.issubset(listed[0].keys())

    _, updated = await mcp.call_tool(
        "update_task",
        {"user_id": "contract-user", "task_id": created["task_id"], "title": "Buy food"},
    )
    assert updated["status"] == "updated"

    _, completed = await mcp.call_tool(
        "complete_task",
        {"user_id": "contract-user", "task_id": created["task_id"]},
    )
    assert completed["status"] == "completed"

    _, deleted = await mcp.call_tool(
        "delete_task",
        {"user_id": "contract-user", "task_id": created["task_id"]},
    )
    assert deleted["status"] == "deleted"

    await engine.dispose()
