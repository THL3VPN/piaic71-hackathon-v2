from __future__ import annotations

# [Task]: T010 [From]: specs/015-mcp-server-extraction/tasks.md User Story 2

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime
from tests.helpers.agent_behavior_fakes import (
    build_message,
    build_response,
    build_tool_call,
    stub_agent_responses,
)


def test_chat_behavior_uses_mcp_tools(auth_headers_factory, monkeypatch) -> None:
    responses = [
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-1", "add_task", '{"title":"buy groceries"}')],
            )
        ),
        build_response(build_message(content="Added.")),
        build_response(
            build_message(
                content="",
                tool_calls=[build_tool_call("call-2", "list_tasks", '{"status":"all"}')],
            )
        ),
        build_response(build_message(content="Here are your tasks.")),
    ]

    stub_agent_responses(monkeypatch, responses)

    async def _fake_add_task(*, user_id: str, title: str, description: str | None = None):
        return {"task_id": 1, "status": "created", "title": title}

    async def _fake_list_tasks(*, user_id: str, status: str | None = None):
        return [{"id": 1, "title": "buy groceries", "completed": False}]

    async def _fake_dispatch(name: str, args: dict[str, object], user_id: str):
        handlers = {
            "add_task": _fake_add_task,
            "list_tasks": _fake_list_tasks,
        }
        return await handlers[name](user_id=user_id, **args)

    monkeypatch.setattr(agent_runtime, "_dispatch_mcp_tool", _fake_dispatch)

    headers = auth_headers_factory("mcp-behavior-user")
    with TestClient(app) as client:
        add_resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Add a task to buy groceries"},
        )
        assert add_resp.status_code == 200
        assert add_resp.json().get("tool_calls")

        list_resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Show me all my tasks"},
        )
        assert list_resp.status_code == 200
        tool_calls = list_resp.json().get("tool_calls")
        assert tool_calls
        assert tool_calls[0]["name"] == "list_tasks"
