# Implementation Plan: Task Tools Layer

**Branch**: `011-task-tools` | **Date**: 2025-12-31 | **Spec**: specs/011-task-tools/spec.md
**Input**: Feature specification from `/specs/011-task-tools/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Introduce a deterministic tool layer for task operations that can be invoked directly without chat or HTTP context. The plan adds user-scoped tool functions wrapping existing task repository logic, enforces domain-level validation and ownership, and returns structured JSON-serializable results. Tests will follow a red-green-refactor cycle for each tool operation to preserve the coverage floor and type-safety expectations.

## Technical Context

**Language/Version**: Python 3.12+ (repo uses 3.13)  
**Primary Dependencies**: fastapi, sqlmodel, psycopg, uvicorn, pytest, pytest-cov, httpx  
**Storage**: Neon Serverless PostgreSQL (via `DATABASE_URL`)  
**Testing**: pytest (required; TDD)  
**Target Platform**: Linux server (ASGI)  
**Project Type**: Single backend web API (FastAPI)  
**Performance Goals**: Tool calls complete within typical request budgets (<500ms) for normal task volumes  
**Constraints**: Coverage ≥80%, type hints everywhere, dataclasses for structured data, domain errors (no HTTP exceptions in tools), user_id explicit in tools, no chat state access  
**Scale/Scope**: Tool layer for task CRUD/complete operations only; no new endpoints

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan documents how TDD will be performed.
- Python 3.12+ with type hints everywhere; dataclasses are the default for structured data.
- UV is the package/environment manager; note any required system dependencies.
- Quality bars: all planned changes must maintain ≥80% coverage; add ADR references for any significant design choices.

## Project Structure

### Documentation (this feature)

```text
specs/011-task-tools/
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

No open technical unknowns. Confirm tool error taxonomy and status-filter behavior using existing task repository patterns.

### Research Output

- Decision: Implement domain errors (TaskNotFound, InvalidInput, UnauthorizedAccess) for tools instead of HTTP exceptions.
  Rationale: Tools must be transport-agnostic and reusable across chat/MCP layers.
  Alternatives considered: Raise HTTPException directly; rejected to keep tool layer independent of API concerns.
- Decision: Map list_tasks status filters to completion state (all/pending/completed) and reject unknown values.
  Rationale: Keeps behavior deterministic and aligned with specification.
  Alternatives considered: Treat unknown values as "all"; rejected to avoid silent errors.
- Decision: Reject update_task calls that include no fields.
  Rationale: Explicit requirement and avoids no-op updates.
  Alternatives considered: Return existing task; rejected to avoid ambiguous outcomes.

## Phase 1: Design & Contracts

### Architecture Sketch

- Tool layer lives in services and calls existing repository functions.
- API/chat layers call tools; tools never reference request/response or chat state.
- Domain errors bubble up to API/chat for translation into HTTP responses later.

### Tool Interfaces

See `specs/011-task-tools/contracts/task-tools.md` for tool signatures, inputs, outputs, and domain errors.

### Data Model

See `specs/011-task-tools/data-model.md` for entity and output shape details.

### Error Handling

Tools raise TaskNotFound, InvalidInput, or UnauthorizedAccess domain errors and return structured outputs on success. API/chat layers are responsible for mapping these errors to HTTP responses when integrated later.

### Quickstart

See `specs/011-task-tools/quickstart.md` for test-focused invocation examples and validation steps.

## Phase 2: Planning Gate

All Phase 0/1 artifacts completed; proceed to task breakdown via `/sp.tasks`.
