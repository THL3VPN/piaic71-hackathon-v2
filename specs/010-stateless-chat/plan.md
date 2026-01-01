# Implementation Plan: Stateless Chat Endpoint

**Branch**: `010-stateless-chat` | **Date**: 2025-12-31 | **Spec**: specs/010-stateless-chat/spec.md
**Input**: Feature specification from `/specs/010-stateless-chat/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Introduce a POST /api/chat endpoint that performs a stateless request cycle using database persistence: create or validate conversations, fetch history, store the user message, generate a deterministic dummy assistant response, store it, and return conversation_id with an empty tool_calls array. Tests will be written first to validate ownership, persistence, and response contract.

## Technical Context

**Language/Version**: Python 3.12+ (repo uses 3.13)  
**Primary Dependencies**: fastapi, sqlmodel, psycopg, uvicorn, pytest, pytest-cov, httpx  
**Storage**: Neon Serverless PostgreSQL (via `DATABASE_URL`)  
**Testing**: pytest (required; TDD)  
**Target Platform**: Linux server (ASGI)  
**Project Type**: Single backend web API (FastAPI)  
**Performance Goals**: Respond under 500ms for typical chat requests (<= 50 history messages)  
**Constraints**: Coverage ≥80%, type hints everywhere, ADR required for material decisions, stateless backend, ownership enforcement, tool_calls empty  
**Scale/Scope**: Single new endpoint plus supporting service logic; reuse existing conversation/message models

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan documents how TDD will be performed.
- Python 3.12+ with type hints everywhere; dataclasses are the default for structured data.
- UV is the package/environment manager; note any required system dependencies.
- Quality bars: all planned changes must maintain ≥80% coverage; add ADR references for any significant design choices.

## Project Structure

### Documentation (this feature)

```text
specs/010-stateless-chat/
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

No open technical unknowns. Reuse existing conversation/message repositories and auth context patterns.

### Research Output

- Decision: Use deterministic dummy response format "OK (dummy): <message>".
  Rationale: Provides safe, predictable output without tool usage.
  Alternatives considered: Static string; rejected because echoing the input verifies pipeline behavior.
- Decision: Always fetch history (limit 50) even if unused by dummy response.
  Rationale: Enforces statelessness and validates history retrieval path.
  Alternatives considered: Skip history for dummy responses; rejected because it would not test stateless flow.
- Decision: Return 404 for non-owned conversation_id.
  Rationale: Prevents information leakage and aligns with existing ownership rules.
  Alternatives considered: 403; rejected to avoid confirming resource existence.

## Phase 1: Design & Contracts

### Data Model

See `specs/010-stateless-chat/data-model.md` for entity details and validation rules.

### API Contracts

See `specs/010-stateless-chat/contracts/` for the POST /api/chat contract.

### Quickstart

See `specs/010-stateless-chat/quickstart.md` for test scenarios and example calls.

## Phase 2: Planning Gate

All Phase 0/1 artifacts completed; proceed to task breakdown via `/sp.tasks`.
