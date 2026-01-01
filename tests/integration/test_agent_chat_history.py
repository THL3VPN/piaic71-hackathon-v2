from __future__ import annotations

# [Task]: T018 [From]: specs/012-ai-agent-integration/spec.md User Story 3
# [Task]: T021 [From]: specs/013-agent-tool-calls/tasks.md Align agent chat tests

import pytest

from src.services import agent_runtime, chat_service, db


@pytest.mark.anyio
async def test_agent_history_limit_applied(tmp_path, monkeypatch: pytest.MonkeyPatch, auth_headers_factory) -> None:
    db_file = tmp_path / "agent_history.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite+aiosqlite:///{db_file}")
    monkeypatch.setenv("BETTER_AUTH_SECRET", "replace-with-shared-secret")
    monkeypatch.setenv("CHAT_HISTORY_LIMIT", "1")

    async def _stub_execute_agent(
        *,
        user_message: str,
        history: list[dict[str, object]],
        user_id: str,
        model: object,
        system_instructions: str,
        session: object,
    ):
        return agent_runtime.AgentResult(response="ok", tool_calls=[])

    monkeypatch.setattr(agent_runtime, "_execute_agent", _stub_execute_agent, raising=False)
    monkeypatch.setattr(agent_runtime, "build_chat_model", lambda settings: object())

    engine = await db.init_engine_from_env()
    captured: dict[str, object] = {"history": None}

    async def _capture_execute_agent(
        *,
        user_message: str,
        history: list[dict[str, object]],
        user_id: str,
        model: object,
        system_instructions: str,
        session: object,
    ):
        captured["history"] = history
        return agent_runtime.AgentResult(response="ok", tool_calls=[])

    monkeypatch.setattr(agent_runtime, "_execute_agent", _capture_execute_agent, raising=False)

    async with db.get_session_for_engine(engine) as session:
        first = await chat_service.handle_chat(
            session,
            owner_id="agent-history-user",
            conversation_id=None,
            message="First",
        )
        await chat_service.handle_chat(
            session,
            owner_id="agent-history-user",
            conversation_id=first.conversation_id,
            message="Second",
        )

    await db.dispose_engine()

    assert captured["history"] is not None
    assert len(captured["history"]) == 1
