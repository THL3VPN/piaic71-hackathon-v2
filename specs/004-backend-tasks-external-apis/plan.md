# Implementation Plan: Task REST API (unauthenticated, DB-backed)

**Branch**: `004-backend-tasks-external-apis` | **Date**: 2025-12-14 | **Spec**: specs/004-backend-tasks-external-apis/spec.md  
**Input**: Feature specification from `/specs/004-backend-tasks-external-apis/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Design a RESTful `/api/tasks` surface that delegates to the existing SQLModel/Neon task service, delivering create/list/get/update/delete/toggle workflows with TDD-first tests, validation, and consistent error handling so the backend can manage tasks without authentication.

## Technical Context

**Language/Version**: Python 3.13 (UV-managed interpreter) with strict type hints.  
**Primary Dependencies**: `fastapi`, `uvicorn`, `sqlmodel`, `psycopg`, `questionary`/`rich` remain in place per constitution; new routes will rely on existing service modules.  
**Storage**: Neon Serverless PostgreSQL (configured via `DATABASE_URL` and shared engine/session helpers).  
**Testing**: `pytest` with `RUN_DB_TESTS=1` to surface Neon-backed coverage; unit tests target services/models while integration tests exercise HTTP routes.  
**Target Platform**: Linux-compatible Python service (currently run via UV).  
**Project Type**: Single backend service (existing `src/` and `tests/` layout).  
**Performance Goals**: Manage typical CRUD load; no high-concurrency targets beyond existing acceptance criteria.  
**Constraints**: Coverage ≥80%; TDD flow enforced (tests red→green→refactor); dataclasses/SQLModel for data structures; maintain layered separation (routes → services).  
**Scale/Scope**: API needs to support a few hundred concurrent users initially, but the central concern is testable correctness over throughput.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (fastapi route tests and service tests), executed to red with Neon toggles as needed, then implemented to green while preserving the 80% coverage rule.  
- Python 3.12+ (using 3.13) with type hints on all new routes/services; `Task` dataclass continues to capture state.  
- UV coordinates environment/virtual env; note `UV_CACHE_DIR` usage and set `UV_PYTHON` in docs.  
- Quality bars: maintain ≥80% coverage and log any major design choices (e.g., consistent error handling) in ADR or research notes.

## Project Structure

### Documentation (this feature)

```text
specs/004-backend-tasks-external-apis/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
src/
├── api/
│   └── tasks.py         # new FastAPI routers for /api/tasks
├── models/
│   └── task.py          # existing Task SQLModel
├── services/
│   └── task_repo.py     # existing service helpers
├── cli/                 # existing CLI (unchanged)
└── main.py              # FastAPI app; new router attachment

tests/
├── integration/
│   └── test_task_api.py  # new HTTP-level tests
├── unit/
│   ├── test_task_service.py
│   └── test_task_model.py
└── ...
```

**Structure Decision**: Keep the single-project layout under `src/`; add a dedicated `src/api/tasks.py` router that wires to `src/services/task_repo.py` for clean separation and testability.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|----------------------------------------|
| None | N/A | N/A |
