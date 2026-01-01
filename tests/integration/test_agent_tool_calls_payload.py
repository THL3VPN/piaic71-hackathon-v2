from __future__ import annotations

# [Task]: T013 [From]: specs/013-agent-tool-calls/spec.md User Story 2

from fastapi.testclient import TestClient

from src.main import app
from src.services import agent_runtime, chat_model_factory


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


def test_agent_tool_call_payload_contains_fields(auth_headers_factory, monkeypatch) -> None:
    responses = [
        _FakeResponse(
            _FakeMessage(
                content="",
                tool_calls=[
                    _FakeToolCall("call-1", "add_task", '{"title":"plan budget"}')
                ],
            )
        ),
        _FakeResponse(_FakeMessage(content="Done")),
    ]

    async def _fake_request_completion(*, client, model_name, messages, tool_specs):
        return responses.pop(0)

    monkeypatch.setattr(agent_runtime, "_request_completion", _fake_request_completion)
    monkeypatch.setattr(
        agent_runtime,
        "build_chat_model",
        lambda settings: chat_model_factory.ChatModel(
            provider="openai",
            model_name="gpt-test",
            client=object(),
        ),
    )

    headers = auth_headers_factory("agent-tool-payload-user")
    with TestClient(app) as client:
        resp = client.post(
            "/api/chat",
            headers=headers,
            json={"message": "Create a task called plan budget"},
        )
        assert resp.status_code == 200
        payload = resp.json()
        tool_calls = payload.get("tool_calls")
        assert isinstance(tool_calls, list)
        assert tool_calls
        first_call = tool_calls[0]
        assert "name" in first_call
        assert "arguments" in first_call
        assert "result" in first_call
