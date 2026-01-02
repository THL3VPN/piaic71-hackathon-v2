from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from src.services import agent_runtime, chat_model_factory

# [Task]: T003 [From]: specs/014-agent-behavior-validation/tasks.md Foundation


@dataclass
class FakeFunction:
    name: str
    arguments: str


@dataclass
class FakeToolCall:
    id: str
    function: FakeFunction


@dataclass
class FakeMessage:
    content: str
    tool_calls: list[FakeToolCall]


@dataclass
class FakeChoice:
    message: FakeMessage


@dataclass
class FakeResponse:
    choices: list[FakeChoice]


def build_tool_call(call_id: str, name: str, arguments: str) -> FakeToolCall:
    return FakeToolCall(id=call_id, function=FakeFunction(name=name, arguments=arguments))


def build_message(content: str, tool_calls: list[FakeToolCall] | None = None) -> FakeMessage:
    return FakeMessage(content=content, tool_calls=tool_calls or [])


def build_response(message: FakeMessage) -> FakeResponse:
    return FakeResponse(choices=[FakeChoice(message=message)])


def stub_agent_responses(monkeypatch, responses: Iterable[FakeResponse]) -> None:
    queue = list(responses)

    async def _fake_request_completion(*, client: Any, model_name: str, messages, tool_specs):
        return queue.pop(0)

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
