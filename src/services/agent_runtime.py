from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.chat_model_factory import ChatModel, ModelFactoryError, build_chat_model
from src.services.chat_provider import load_provider_settings
from src.services import agent_tools, task_tools

# [Task]: T009 [From]: specs/012-ai-agent-integration/spec.md User Story 1
# [Task]: T019 [From]: specs/012-ai-agent-integration/spec.md User Story 3
# [Task]: T009 [From]: specs/013-agent-tool-calls/spec.md User Story 1
# [Task]: T010 [From]: specs/013-agent-tool-calls/spec.md User Story 1


@dataclass(frozen=True)
class AgentResult:
    response: str
    tool_calls: list[dict[str, object]]


def _fallback_response() -> str:
    return "I'm having trouble right now. Please try again shortly."


def _apply_history_limit(history: list[dict[str, object]], limit: int) -> list[dict[str, object]]:
    if limit <= 0:
        return []
    return history[-limit:]


def _build_system_instructions() -> str:
    return (
        "You are a helpful task assistant. Use tools for task changes, ask follow-up questions "
        "when needed, and confirm actions in a friendly tone."
    )


def _tool_error_response() -> str:
    return "I could not complete that request. Please check the task details and try again."


def _normalize_history(history: list[dict[str, object]]) -> list[dict[str, object]]:
    filtered = []
    for item in history:
        content = item.get("content")
        if isinstance(content, str) and content.startswith("[tool_calls]"):
            continue
        filtered.append(item)
    return filtered


def _build_tool_specs(tools: list[agent_tools.AgentTool]) -> list[dict[str, object]]:
    specs: list[dict[str, object]] = []
    for tool in tools:
        specs.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_schema,
                },
            }
        )
    return specs


async def _request_completion(
    *,
    client: Any,
    model_name: str,
    messages: list[dict[str, object]],
    tool_specs: list[dict[str, object]],
) -> Any:
    return await client.chat.completions.create(
        model=model_name,
        messages=messages,
        tools=tool_specs,
        tool_choice="auto",
    )


def _parse_tool_call_arguments(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _build_tool_call_payload(name: str, args: dict[str, Any], result: dict[str, Any]) -> dict[str, object]:
    return {"name": name, "arguments": args, "result": result}


async def _execute_agent(
    *,
    user_message: str,
    history: list[dict[str, object]],
    user_id: str,
    model: ChatModel,
    system_instructions: str,
    session: AsyncSession,
) -> AgentResult:
    tools = agent_tools.build_task_tools(session=session, user_id=user_id)
    tool_specs = _build_tool_specs(tools)
    tool_map = {tool.name: tool for tool in tools}

    messages: list[dict[str, object]] = [
        {"role": "system", "content": system_instructions},
        *history,
        {"role": "user", "content": user_message},
    ]

    first_response = await _request_completion(
        client=model.client,
        model_name=model.model_name,
        messages=messages,
        tool_specs=tool_specs,
    )
    first_message = first_response.choices[0].message
    tool_calls = getattr(first_message, "tool_calls", None) or []
    if not tool_calls:
        response_text = first_message.content or _fallback_response()
        return AgentResult(response=response_text, tool_calls=[])

    assistant_message = {
        "role": "assistant",
        "content": first_message.content or "",
        "tool_calls": [
            {
                "id": call.id,
                "type": "function",
                "function": {
                    "name": call.function.name,
                    "arguments": call.function.arguments,
                },
            }
            for call in tool_calls
        ],
    }
    messages.append(assistant_message)

    tool_call_payloads: list[dict[str, object]] = []
    tool_error = False
    for call in tool_calls:
        tool = tool_map.get(call.function.name)
        args = _parse_tool_call_arguments(call.function.arguments)
        if tool is None:
            continue
        try:
            result = await tool.handler(session, user_id, args)
        except task_tools.TaskToolError as exc:
            result = {"error": str(exc)}
            tool_error = True
        tool_call_payloads.append(_build_tool_call_payload(call.function.name, args, result))
        messages.append(
            {
                "role": "tool",
                "tool_call_id": call.id,
                "content": json.dumps(result, separators=(",", ":")),
            }
        )

    if tool_error:
        return AgentResult(response=_tool_error_response(), tool_calls=tool_call_payloads)

    second_response = await _request_completion(
        client=model.client,
        model_name=model.model_name,
        messages=messages,
        tool_specs=tool_specs,
    )
    second_message = second_response.choices[0].message
    response_text = second_message.content or _fallback_response()
    return AgentResult(response=response_text, tool_calls=tool_call_payloads)


async def run_agent(
    *,
    user_message: str,
    history: list[dict[str, object]],
    user_id: str,
    session: AsyncSession,
) -> AgentResult:
    settings = load_provider_settings()
    try:
        model = build_chat_model(settings)
    except ModelFactoryError:
        return AgentResult(response=_fallback_response(), tool_calls=[])

    trimmed_history = _apply_history_limit(history, settings.history_limit)
    normalized_history = _normalize_history(trimmed_history)
    system_instructions = _build_system_instructions()
    return await _execute_agent(
        user_message=user_message,
        history=normalized_history,
        user_id=user_id,
        model=model,
        system_instructions=system_instructions,
        session=session,
    )
