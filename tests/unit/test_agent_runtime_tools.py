from __future__ import annotations

# [Task]: T007 [From]: specs/013-agent-tool-calls/spec.md User Story 1
# [Task]: T001 [From]: specs/019-agent-tool-chaining/spec.md User Story 1

import pytest

from src.services import agent_runtime, agent_tools


class _FakeFunction:
    def __init__(self, name: str, arguments: str):
        self.name = name
        self.arguments = arguments


class _FakeToolCall:
    def __init__(self, call_id: str, name: str, arguments: str):
        self.id = call_id
        self.function = _FakeFunction(name=name, arguments=arguments)


class _FakeMessage:
    def __init__(self, content: str, tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []


class _FakeChoice:
    def __init__(self, message):
        self.message = message


class _FakeResponse:
    def __init__(self, message):
        self.choices = [_FakeChoice(message)]


@pytest.mark.anyio
async def test_agent_runtime_returns_tool_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _handler(session, user_id, args):
        return {"status": "created", "task_id": 1, "title": args.get("title")}

    monkeypatch.setattr(agent_runtime, "build_chat_model", lambda settings: type("M", (), {"client": object(), "model_name": "gpt-test"})())
    monkeypatch.setattr(
        agent_tools,
        "build_task_tools",
        lambda session, user_id: [
            agent_tools.AgentTool(
                name="add_task",
                description="Create task",
                input_schema={"type": "object"},
                handler=_handler,
            )
        ],
    )

    responses = [
        _FakeResponse(
            _FakeMessage(
                content="",
                tool_calls=[_FakeToolCall("call-1", "add_task", '{"title":"file receipts"}')],
            )
        ),
        _FakeResponse(_FakeMessage(content="Done")),
    ]

    async def _fake_request_completion(*, client, model_name, messages, tool_specs):
        return responses.pop(0)

    monkeypatch.setattr(agent_runtime, "_request_completion", _fake_request_completion)

    result = await agent_runtime.run_agent(
        user_message="Create a task called file receipts",
        history=[],
        user_id="user-1",
        session=object(),
    )

    assert result.tool_calls, "Expected tool calls to be returned"


@pytest.mark.anyio
async def test_agent_runtime_handles_two_step_tool_chain(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(agent_runtime, "build_chat_model", lambda settings: type("M", (), {"client": object(), "model_name": "gpt-test"})())
    monkeypatch.setattr(
        agent_tools,
        "build_task_tools",
        lambda session, user_id: [
            agent_tools.AgentTool(
                name="list_tasks",
                description="List tasks",
                input_schema={"type": "object"},
                handler=lambda *_: None,
            ),
            agent_tools.AgentTool(
                name="complete_task",
                description="Complete task",
                input_schema={"type": "object"},
                handler=lambda *_: None,
            ),
        ],
    )

    responses = [
        _FakeResponse(
            _FakeMessage(
                content="",
                tool_calls=[_FakeToolCall("call-1", "list_tasks", '{"status":"all"}')],
            )
        ),
        _FakeResponse(
            _FakeMessage(
                content="",
                tool_calls=[_FakeToolCall("call-2", "complete_task", '{"task_id":3}')],
            )
        ),
        _FakeResponse(_FakeMessage(content="Done")),
    ]

    async def _fake_request_completion(*, client, model_name, messages, tool_specs):
        return responses.pop(0)

    async def _fake_dispatch(name, args, user_id):
        if name == "list_tasks":
            return [{"id": 3, "title": "hello world", "completed": False}]
        if name == "complete_task":
            return {"task_id": args.get("task_id"), "status": "completed", "title": "hello world"}
        raise AssertionError(f"Unexpected tool {name}")

    monkeypatch.setattr(agent_runtime, "_request_completion", _fake_request_completion)
    monkeypatch.setattr(agent_runtime, "_dispatch_mcp_tool", _fake_dispatch)

    result = await agent_runtime.run_agent(
        user_message="Mark hello world as completed",
        history=[],
        user_id="user-1",
        session=object(),
    )

    assert result.response == "Done"
    assert [call["name"] for call in result.tool_calls] == ["list_tasks", "complete_task"]
