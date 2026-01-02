# Implementation Plan: MCP Server Extraction

**Branch**: `015-mcp-server-extraction` | **Date**: 2026-01-02 | **Spec**: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
**Input**: Feature specification from `/home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md`

**Note**: This plan follows Spec-Driven Development and the project constitution.

## Summary

Extract task operations into a dedicated MCP server using the Official MCP SDK and update the backend agent path to call MCP tools while preserving Step 5 behavior, statelessness, and ownership enforcement.

## Technical Context

**Language/Version**: Python 3.12+ (repo uses 3.13)
**Primary Dependencies**: fastapi, uvicorn, sqlmodel, psycopg, openai (Agents SDK), pytest, official MCP SDK
**Storage**: PostgreSQL (Neon via `DATABASE_URL`)
**Testing**: pytest with red-green-refactor
**Target Platform**: Linux server
**Project Type**: Single backend service plus a new MCP server service
**Performance Goals**: Typical chat response under a few seconds with MCP tool calls
**Constraints**: Coverage ≥80%, type hints everywhere, no DB model changes, no auth changes, chat remains stateless, no secrets in code, Step 5 behavior parity
**Scale/Scope**: One MCP server exposing five task tools with DB-backed stateless operations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan includes contract/integration tests for MCP tool usage.
- Python 3.12+ with type hints everywhere; dataclasses remain the default for structured data.
- UV is the package/environment manager; add MCP SDK as required dependency.
- Quality bars: maintain ≥80% coverage; ADR required if MCP extraction is considered a material architectural decision.

## Project Structure

### Documentation (this feature)

```text
/home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/
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

/home/aie/all_data/piaic71-hackathon-v2/mcp_server/
├── app.py
└── tools.py
```

**Structure Decision**: Single backend service with a new `mcp_server/` package for the MCP SDK server.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Additional service (MCP server) | Required by Step 6 architecture | In-process tools violate MCP extraction requirement |

## Phase 0: Outline & Research

### Research Tasks

- Confirm Official MCP SDK server setup and tool registration patterns.
- Determine authentication and request flow between backend and MCP server (URL, headers).
- Define error mapping for not-found and validation errors without leaking ownership.

### Research Output

See `/home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/research.md`.

## Phase 1: Design & Contracts

### Architecture Sketch

- MCP server exposes task tools backed by the Neon DB and enforces ownership via user_id.
- Backend agent runtime uses MCP tool invocations instead of local Python tool functions.
- Chat response continues to return tool_calls and friendly confirmations.

### MCP Tool Interface

- Tools: add_task, list_tasks, complete_task, delete_task, update_task.
- Inputs include user_id plus task fields.
- Outputs mirror existing tool result shapes.

### Data Model

No new entities; MCP server uses existing task storage. See `/home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/data-model.md`.

### API Contracts

See `/home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/contracts/mcp-tools.openapi.yaml` for tool payload expectations and `/api/chat` response behavior.

### Error Handling

- MCP tool errors map to not-found style responses for ownership violations.
- Backend handles MCP connectivity errors with friendly fallback responses.
- Auth and validation errors remain unchanged.

### Quickstart

See `/home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/quickstart.md`.

## Phase 1: Agent Context Update

Run `/home/aie/all_data/piaic71-hackathon-v2/.specify/scripts/bash/update-agent-context.sh codex` after design files are created.

## Phase 1 Constitution Re-check

- TDD flow maintained (tests first).
- Type hints preserved; no DB model changes.
- ADR required for the MCP server extraction decision.

## Phase 2: Planning Gate

All Phase 0/1 artifacts completed; proceed to task breakdown via `/sp.tasks`.

## Implementation Notes

- MCP client falls back to local tool handlers when `MCP_SERVER_URL` is not set (test environments).
- Manual quickstart validation requires running the MCP server and backend with real env vars.
