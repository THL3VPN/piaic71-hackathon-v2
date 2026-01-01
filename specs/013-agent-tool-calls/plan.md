# Implementation Plan: Real-Time Agent Tool Calls

**Branch**: `013-agent-tool-calls` | **Date**: 2026-01-01 | **Spec**: /home/aie/all_data/piaic71-hackathon-v2/specs/013-agent-tool-calls/spec.md
**Input**: Feature specification from `/home/aie/all_data/piaic71-hackathon-v2/specs/013-agent-tool-calls/spec.md`

**Note**: This plan follows Spec-Driven Development and the project constitution.

## Summary

Implement real-time agent replies using the OpenAI Agents SDK with registered task tools, ensuring tool calls are executed via the existing tool layer and returned in the `/api/chat` response while preserving stateless chat behavior.

## Technical Context

**Language/Version**: Python 3.12+ (repo uses 3.13)
**Primary Dependencies**: fastapi, uvicorn, sqlmodel, psycopg, openai (Agents SDK), pytest
**Storage**: PostgreSQL (Neon via `DATABASE_URL`)
**Testing**: pytest with red-green-refactor
**Target Platform**: Linux server
**Project Type**: Single backend service
**Performance Goals**: Typical chat response under a few seconds with tool actions
**Constraints**: Coverage >= 80%, type hints everywhere, no DB model changes, no auth changes, chat remains stateless, provider configurable via env
**Scale/Scope**: Single service, limited tool set, single chat endpoint

## Constitution Check

- Tests are defined first (pytest), executed to red, then implemented to green; plan includes contract/integration tests for tool calls.
- Python 3.12+ with type hints everywhere; dataclasses remain the default for structured data.
- UV is the package/environment manager.
- Quality bars: keep coverage >= 80%; no ADR required for incremental SDK wiring (no architectural change).

## Project Structure

### Documentation (this feature)

```text
/home/aie/all_data/piaic71-hackathon-v2/specs/013-agent-tool-calls/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
/home/aie/all_data/piaic71-hackathon-v2/src/
├── api/
├── models/
├── services/
└── main.py

/home/aie/all_data/piaic71-hackathon-v2/tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single backend service with `src/` and `tests/` at repository root.

## Phase 0: Outline & Research

### Research Tasks

- Research OpenAI Agents SDK integration patterns for tool calling and message history.
- Confirm tool registration strategy that preserves ownership and existing tool behavior.
- Verify response payload expectations for tool call transparency.

### Research Output

See `/home/aie/all_data/piaic71-hackathon-v2/specs/013-agent-tool-calls/research.md`.

## Phase 1: Design & Contracts

### Architecture Sketch

- Agent runtime builds an SDK agent using provider config and model factory.
- Task tools are registered with the agent and invoked by name.
- Tool calls are executed through existing tool layer and captured for response payloads.
- Chat endpoint persists user + assistant messages and returns tool call details.

### Agent Interface

- Stateless per request with DB-backed history.
- Tools registered once per request execution.
- Emits tool call records with name, inputs, and outputs.

### Data Model

See `/home/aie/all_data/piaic71-hackathon-v2/specs/013-agent-tool-calls/data-model.md`.

### API Contracts

See `/home/aie/all_data/piaic71-hackathon-v2/specs/013-agent-tool-calls/contracts/chat-tool-calls.openapi.yaml`.

### Error Handling

- Tool errors are translated into friendly assistant messages.
- Auth and validation errors preserve existing HTTP responses.
- Provider errors return a safe fallback response.

### Quickstart

See `/home/aie/all_data/piaic71-hackathon-v2/specs/013-agent-tool-calls/quickstart.md`.

## Implementation Notes (2026-01-01)

- Agent runtime executes tool calls through `task_tools` and returns structured `tool_calls` in the chat response.
- Tool errors map to a friendly assistant response while preserving tool call payloads.
- Chat runtime remains stateless by using DB-backed history and request-scoped tool wiring.

## Phase 1: Agent Context Update

Run `/home/aie/all_data/piaic71-hackathon-v2/.specify/scripts/bash/update-agent-context.sh codex` after design files are created.

## Phase 1 Constitution Re-check

- TDD flow maintained (tests first).
- Type hints and dataclasses preserved.
- No changes to DB models or auth logic.

## Phase 2: Planning Gate

All Phase 0/1 artifacts completed; proceed to task breakdown via `/sp.tasks`.
