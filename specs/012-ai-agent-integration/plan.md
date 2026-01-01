# Implementation Plan: AI Agent Integration

**Branch**: `012-ai-agent-integration` | **Date**: 2025-12-31 | **Spec**: specs/012-ai-agent-integration/spec.md
**Input**: Feature specification from `/specs/012-ai-agent-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Replace the dummy chat response with a model-agnostic agent that uses the task tool layer. The plan introduces a provider-configured model factory, stateless agent execution that rebuilds history from the database each request, and tool call capture in responses. Tests will be written first to validate tool invocation, ownership enforcement, error translation, and provider configuration handling.

## Technical Context

**Language/Version**: Python 3.12+ (repo uses 3.13)  
**Primary Dependencies**: fastapi, sqlmodel, psycopg, uvicorn, pytest, pytest-cov, httpx  
**Storage**: Neon Serverless PostgreSQL (via `DATABASE_URL`)  
**Testing**: pytest (required; TDD)  
**Target Platform**: Linux server (ASGI)  
**Project Type**: Single backend web API (FastAPI)  
**Performance Goals**: Chat responses return within typical request budgets (<2s) for standard history sizes  
**Constraints**: Coverage ≥80%, type hints everywhere, dataclasses for structured data, stateless chat, tool-only task mutations, provider config via env only  
**Scale/Scope**: Single agent integrated into existing chat endpoint with tool binding and provider switch via config

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan documents how TDD will be performed.
- Python 3.12+ with type hints everywhere; dataclasses are the default for structured data.
- UV is the package/environment manager; note any required system dependencies.
- Quality bars: all planned changes must maintain ≥80% coverage; add ADR references for any significant design choices.

## Project Structure

### Documentation (this feature)

```text
specs/012-ai-agent-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── api/
├── models/
└── services/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single FastAPI backend rooted at `src/` with tests organized by contract/integration/unit under `tests/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| n/a | n/a | n/a |

## Phase 0: Outline & Research

### Research Questions

No open technical unknowns. Confirm provider configuration error handling and tool-call capture approach for the current chat response payload.

### Research Output

- Decision: Fail chat requests with a safe fallback assistant message when model/provider config is invalid.
  Rationale: Avoid leaking config details while keeping a consistent user experience.
  Alternatives considered: Raise 500 with raw error; rejected to avoid leaking config state.
- Decision: Persist tool call summaries alongside assistant responses.
  Rationale: Required response payload includes tool call details; storing them ensures auditability.
  Alternatives considered: Return tool calls without persistence; rejected due to auditing needs.
- Decision: Use existing history retrieval with a configurable limit for agent context.
  Rationale: Maintains statelessness and aligns with configured history cap.
  Alternatives considered: Store in-memory history; rejected due to stateless requirement.

## Phase 1: Design & Contracts

### Architecture Sketch

- Model factory reads provider configuration and returns a model instance.
- Agent runtime uses system instructions plus DB-backed history per request.
- Tool layer is injected into the agent; tool calls are executed and captured.
- Chat endpoint persists user + assistant messages and tool call results.

### Agent Interface

- Stateless per request.
- Uses only tool outputs for task mutations.
- Emits tool call records (name, arguments, result) for response payloads.

### Data Model

See `specs/012-ai-agent-integration/data-model.md` for tool call and message fields.

### API Contracts

See `specs/012-ai-agent-integration/contracts/` for the updated chat response payload.

### Error Handling

Tool errors are translated into friendly assistant messages. Provider errors return a safe fallback response while preserving existing HTTP auth/validation behavior.

### Quickstart

See `specs/012-ai-agent-integration/quickstart.md` for test scenarios and example calls.

## Phase 2: Planning Gate

All Phase 0/1 artifacts completed; proceed to task breakdown via `/sp.tasks`.

## Implementation Notes (2025-12-31)

- Provider configuration is validated in `chat_provider`, with errors surfaced via `ModelFactoryError`.
- Agent runtime trims history using `CHAT_HISTORY_LIMIT` and routes execution through `_execute_agent`.
- Tool call payloads are persisted as assistant messages prefixed with `[tool_calls]`.
