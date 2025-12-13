# Implementation Plan: Persistent Task Storage (SQLModel + Neon Postgres)

**Branch**: `003-sqlmodel-neon-tasks` | **Date**: 2025-12-13 | **Spec**: specs/003-sqlmodel-neon-tasks/spec.md
**Input**: Feature specification from `/specs/003-sqlmodel-neon-tasks/spec.md`

## Summary

Persist tasks in Neon Postgres using SQLModel with a service/repository layer that supports create/get/list and initializes the DB on startup. Use TDD with pytest (unit + integration) and keep HTTP handlers thin by delegating to the service. Use `SQLModel.metadata.create_all` at startup for table creation. Tests must reach ≥80% coverage for touched backend code and exercise real DB connections (Neon) as well as local integration via a test database URL.

## Technical Context

**Language/Version**: Python 3.13 (constitution requires 3.12+, using 3.13)  
**Primary Dependencies**: UV-managed: fastapi, sqlmodel, uvicorn, httpx (tests), pytest/pytest-cov; database driver via SQLModel (psycopg recommended)  
**Storage**: Neon Serverless PostgreSQL via `DATABASE_URL` env var  
**Testing**: pytest with unit + integration (service with test DB URL); coverage ≥80%  
**Target Platform**: Linux server (container-friendly), UV-managed env  
**Project Type**: Backend service (FastAPI entry), single repo  
**Performance Goals**: Low throughput acceptable; aim for fast startup and consistent CRUD latency for small datasets (default Neon)  
**Constraints**: Type hints everywhere, TDD red/green, dataclasses where applicable, ADR for material decisions, keep public API stable within phase  
**Scale/Scope**: Single table Task; small user base; focus on correctness and reliability

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests first: write failing unit/integration tests for service create/get/list; run red → implement → green → refactor.
- Python 3.12+ with type hints everywhere; dataclasses for structured data where suitable (SQLModel models also typed).
- UV-managed env and deps; add psycopg driver if not already present.
- Coverage must stay ≥80% for backend code touched; add ADR if we change DB strategy or connection management.

## Project Structure

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

```text
src/
├── models/
├── services/
├── api/
├── cli/
└── lib/

tests/
├── integration/
└── unit/
```

**Structure Decision**: Keep single backend project under `src/` with `models`, `services`, `api`; tests under `tests/unit` and `tests/integration`. No separate frontend. Feature docs under `specs/003-sqlmodel-neon-tasks/`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Architecture Sketch

- Entry: FastAPI app (`src/main.py`) already exists; add task API router (thin) that delegates to service.
- Persistence: Async SQLModel engine built from `DATABASE_URL`; session factory for per-request context; metadata create_all on startup.
- Service/Repository: Module `src/services/task_repo.py` (or similar) exposing `create_task`, `get_task`, `list_tasks`; handles validation and not-found behavior.
- Models: `src/models/task.py` SQLModel table; include validators for title and defaults.
- Error Handling: Validation errors → 400 from API; DB issues → logged, 500 with sanitized message; service returns None/Result for not-found.

## Interfaces

- `get_engine(database_url: str) -> AsyncEngine`
- `get_session(engine: AsyncEngine) -> AsyncSession` (async context manager/dependency)
- `create_task(session, title: str, description: str | None) -> Task`
- `get_task(session, task_id: int) -> Task | None`
- `list_tasks(session) -> list[Task]`
- Optional router handlers map to service calls; handlers remain thin.

## Error Handling

- Empty/whitespace title rejected before DB insert; raise ValueError → mapped to 400.
- Not found returns None; API maps to 404; service callers can branch.
- Connection errors: log with context (no secrets), raise HTTP 500; startup fails fast if engine cannot connect.
- Date handling: use UTC `datetime.utcnow()` via default_factory; serialize ISO 8601.

## Decisions Needing (captured in research)

- ORM/driver: SQLModel + async psycopg (decided).
- Schema management: create_all on startup (decided).
- Session scope: per-request/per-op session (decided).
- Routing: keep API thin and optional; core logic in service (decided).

## Testing Strategy

- Unit: service functions with in-memory or test Postgres URL (e.g., Neon test DB) using transactional rollback fixtures; validate title rules and not-found behavior.
- Integration: with real database URL (Neon) to ensure create_all, insert, fetch, list.
- Coverage: run `UV_PYTHON=python3.13 UV_CACHE_DIR=.uv-cache uv run pytest --cov=src --cov-report=term-missing`; target 80%+ for new backend code.
- TDD: write failing tests for create/get/list before implementing service/engine wiring.

## Phase 0: Research (complete)

- Deliverable: `specs/003-sqlmodel-neon-tasks/research.md`
- Outcomes: chosen SQLModel + async psycopg, create_all on startup, session factory, service layer separation, UTC timestamps.
- Open questions: none.

## Phase 1: Design & Contracts (complete)

- Deliverables:
  - `data-model.md`: Task entity fields/constraints.
  - `contracts/openapi.md`: POST /tasks, GET /tasks/{id}, GET /tasks (thin wrappers over service).
  - `quickstart.md`: env setup, run commands, tests.
  - Agent context updated via `.specify/scripts/bash/update-agent-context.sh codex`.
- Constitution re-check: passes (TDD planned, type hints, coverage target, UV stack).
