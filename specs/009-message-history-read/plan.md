# Implementation Plan: Message History Read

**Branch**: `009-message-history-read` | **Date**: 2025-12-30 | **Spec**: specs/009-message-history-read/spec.md
**Input**: Feature specification from `/specs/009-message-history-read/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add an authenticated GET endpoint that returns a conversation's message history from the database with ownership enforcement, default/maximum limits, and chronological ordering. Tests will be written first to validate ownership checks, ordering, and limit behavior, then implementation will follow to maintain stateless chat readiness.

## Technical Context

**Language/Version**: Python 3.12+ (repo uses 3.13)  
**Primary Dependencies**: fastapi, sqlmodel, psycopg, uvicorn, pytest, pytest-cov, httpx  
**Storage**: Neon Serverless PostgreSQL (via `DATABASE_URL`)  
**Testing**: pytest (required; TDD)  
**Target Platform**: Linux server (ASGI)  
**Project Type**: Single backend web API (FastAPI)  
**Performance Goals**: Return history responses in under 500ms for typical conversation sizes (<= 200 messages)  
**Constraints**: Coverage ≥80%, type hints everywhere, ADR required for material decisions, stateless backend, ownership enforcement, limit clamp to 200, default limit 50  
**Scale/Scope**: Single endpoint addition with DB query and auth enforcement; no new tables

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan documents how TDD will be performed.
- Python 3.12+ with type hints everywhere; dataclasses are the default for structured data.
- UV is the package/environment manager; note any required system dependencies.
- Quality bars: all planned changes must maintain ≥80% coverage; add ADR references for any significant design choices.

## Project Structure

### Documentation (this feature)

```text
specs/009-message-history-read/
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

No open technical unknowns. Proceed with standard FastAPI + SQLModel patterns used in this repository.

### Research Output

- Decision: Reject non-positive limit values with validation errors (422).
  Rationale: Consistent with FastAPI/Pydantic validation expectations and explicit requirement.
  Alternatives considered: Treat non-positive limit as default; rejected to avoid silent behavior changes.
- Decision: Clamp limit to a maximum of 200.
  Rationale: Requirement specifies max 200; prevents oversized responses.
  Alternatives considered: Return 422 if above max; rejected to keep behavior user-friendly.
- Decision: Order messages by created_at ascending, then id for deterministic ordering.
  Rationale: Ensures stable chronological ordering when timestamps tie.
  Alternatives considered: Only created_at ordering; rejected due to potential nondeterminism.

## Phase 1: Design & Contracts

### Data Model

See `specs/009-message-history-read/data-model.md` for entity details and validation rules.

### API Contracts

See `specs/009-message-history-read/contracts/` for the GET history endpoint contract.

### Quickstart

See `specs/009-message-history-read/quickstart.md` for test scenarios and example calls.

## Phase 2: Planning Gate

All Phase 0/1 artifacts completed; proceed to task breakdown via `/sp.tasks`.
