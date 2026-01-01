from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.services.chat_model_factory import ChatModel, ModelFactoryError, build_chat_model
from src.services.chat_provider import load_provider_settings
from src.services import agent_tools, mcp_client, task_tools

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
        "You are a task assistant. Always use tools for task changes.\n"
        "\n"
        "Tool selection:\n"
        "- add/create/remember a task -> add_task (extract a concise title).\n"
        "- list/show tasks -> list_tasks with status mapping:\n"
        "  - all -> status=\"all\"\n"
        "  - pending/open/remaining -> status=\"pending\"\n"
        "  - completed/done -> status=\"completed\"\n"
        "- complete/finish a task -> complete_task (requires task_id; if missing, ask or list_tasks).\n"
        "- delete/remove a task -> delete_task (if ambiguous, list_tasks then ask for confirmation).\n"
        "- update/change/rename a task -> update_task (only update provided fields; if none, ask).\n"
        "\n"
        "Tool chaining (deterministic): list_tasks -> delete_task, list_tasks -> complete_task, "
        "list_tasks -> update_task.\n"
        "\n"
        "Ambiguity: ask a follow-up question; do not guess.\n"
        "Task not found: respond politely and suggest listing tasks.\n"
        "\n"
        "Responses: friendly and concise confirmations; no internal tool or system details; "
        "no hallucinated task state."
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


async def _dispatch_mcp_tool(name: str, args: dict[str, Any], user_id: str) -> Any:
    match name:
        case "add_task":
            return await mcp_client.call_add_task(
                user_id=user_id,
                title=args.get("title"),
                description=args.get("description"),
            )
        case "list_tasks":
            return await mcp_client.call_list_tasks(
                user_id=user_id,
                status=args.get("status"),
            )
        case "complete_task":
            return await mcp_client.call_complete_task(
                user_id=user_id,
                task_id=args.get("task_id"),
            )
        case "delete_task":
            return await mcp_client.call_delete_task(
                user_id=user_id,
                task_id=args.get("task_id"),
            )
        case "update_task":
            return await mcp_client.call_update_task(
                user_id=user_id,
                task_id=args.get("task_id"),
                title=args.get("title"),
                description=args.get("description"),
            )
        case _:
            raise mcp_client.McpClientError(f"Unknown tool: {name}")


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
        args = _parse_tool_call_arguments(call.function.arguments)
        args.pop("user_id", None)
        tool = tool_map.get(call.function.name)
        if tool is None:
            continue
        try:
            result = await _dispatch_mcp_tool(call.function.name, args, user_id)
        except mcp_client.McpConfigError:
            try:
                result = await tool.handler(session, user_id, args)
            except task_tools.TaskToolError as exc:
                result = {"error": str(exc)}
                tool_error = True
        except mcp_client.McpClientError as exc:
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
