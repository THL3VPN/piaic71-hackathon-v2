# Tasks: Persistent Task Storage (SQLModel + Neon Postgres)

**Input**: Design documents from `/specs/003-sqlmodel-neon-tasks/`  
**Prerequisites**: plan.md (required), spec.md (user stories), research.md, data-model.md, contracts/

**Tests**: TDD mandatory (pytest). Write failing tests first, run red → implement → green → refactor. Maintain ≥80% coverage.

**Organization**: Tasks grouped by user story to enable independent delivery.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure dependencies and env config ready for DB work.

- [X] T001 Add SQLModel + psycopg dependencies via UV (pyproject/uv.lock) (depends on none; deliverable: updated deps)
- [X] T002 Create sample env file documenting `DATABASE_URL` (repository root `.env.example`) (depends on T001; deliverable: .env.example)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core DB wiring required before stories.

- [ ] T003 Write failing unit test for engine/session factory creation using test DATABASE_URL in tests/unit/test_db_engine.py (depends on T001; deliverable: red test)
- [X] T003 Write failing unit test for engine/session factory creation using test DATABASE_URL in tests/unit/test_db_engine.py (depends on T001; deliverable: red test)
- [X] T004 Implement engine/session factory module (e.g., src/services/db.py) to satisfy T003 (depends on T003; deliverable: db module)
- [X] T005 Write failing integration test to ensure `SQLModel.metadata.create_all` executes on startup path (tests/integration/test_startup_db.py) (depends on T004; deliverable: red test)
- [X] T006 Implement startup hook/create_all wiring (e.g., src/main.py or startup module) to satisfy T005 (depends on T005; deliverable: startup wiring)
- [X] T007 Refactor DB wiring for clarity (dedupe session/engine creation; ensure type hints) (depends on T006; deliverable: cleaned db module)

**Checkpoint**: Foundation ready—DB engine/session + create_all verified.

---

## Phase 3: User Story 1 - Start backend with live Neon DB (Priority: P1) 🎯 MVP

**Goal**: App starts with Neon `DATABASE_URL`, applies metadata, and fails fast on invalid URLs.
**Independent Test**: Run with valid `DATABASE_URL`; startup succeeds and tables exist. Invalid URL yields clear failure.

### Tests (write first)
- [X] T008 [US1] Add failing integration test asserting startup success with valid `DATABASE_URL` and table existence (tests/integration/test_startup_db.py) (depends on T006; deliverable: red test)
- [X] T009 [US1] Add failing integration test for invalid/missing `DATABASE_URL` returning clear error (tests/integration/test_startup_db.py) (depends on T008; deliverable: red test)

### Implementation
- [X] T010 [US1] Implement startup validation/error handling for missing/invalid `DATABASE_URL` (src/services/db.py) (depends on T009; deliverable: validated startup)
- [X] T011 [US1] Ensure startup path logs sanitized errors and halts when connection fails (src/main.py startup) (depends on T010; deliverable: logged failure path)

**Checkpoint**: US1 independently testable (startup success/failure cases).

---

## Phase 4: User Story 2 - Create and fetch a task (Priority: P2)

**Goal**: Create task with validation; fetch by ID via service layer.
**Independent Test**: Service-only create→fetch round-trip works; not-found handled cleanly.

### Tests (write first)
- [X] T012 [US2] Add failing unit tests for Task model defaults/validation (title trim, completed default false, created_at set) in tests/unit/test_task_model.py (depends on T007; deliverable: red test)
- [X] T013 [US2] Add failing unit tests for service create_task/get_task behavior with session fixture (tests/unit/test_task_service.py) (depends on T012; deliverable: red test)
- [X] T014 [US2] Add failing integration test for create→get round-trip against test DB (tests/integration/test_task_crud.py) (depends on T013; deliverable: red test)

### Implementation
- [X] T015 [US2] Implement Task SQLModel table with validation/defaults (src/models/task.py) (depends on T013; deliverable: model)
- [X] T016 [US2] Implement create_task/get_task in service/repository (src/services/task_repo.py) with not-found handling (depends on T015; deliverable: service functions)
- [X] T017 [US2] Refactor service to ensure type hints, small functions, and reuse session helpers (depends on T016; deliverable: cleaned service)

**Checkpoint**: US2 independently testable via service tests and integration round-trip.

---

## Phase 5: User Story 3 - List tasks (Priority: P3)

**Goal**: List tasks deterministically (created_at asc) and handle empty set.
**Independent Test**: Service returns ordered list; empty DB returns empty list.

### Tests (write first)
- [X] T018 [US3] Add failing unit tests for list_tasks ordering and empty result in tests/unit/test_task_service.py (depends on T017; deliverable: red test)
- [X] T019 [US3] Add failing integration test seeding multiple tasks and asserting order in tests/integration/test_task_list.py (depends on T018; deliverable: red test)

### Implementation
- [X] T020 [US3] Implement list_tasks in service/repository with deterministic ordering (src/services/task_repo.py) (depends on T019; deliverable: list logic)
- [X] T021 [US3] Refactor common query utilities/shared fixtures if duplication observed (depends on T020; deliverable: refactored helpers)

**Checkpoint**: US3 independently testable; list behaviors validated.

---

## Phase 6: Polish & Cross-Cutting

- [ ] T022 Update quickstart.md with final run/test commands if changed (specs/003-sqlmodel-neon-tasks/quickstart.md) (depends on completion of user stories; deliverable: updated doc)
- [ ] T023 Run full test suite and summarize coverage (root command: `UV_PYTHON=python3.13 UV_CACHE_DIR=.uv-cache uv run pytest --cov=src --cov-report=term-missing`) (depends on all tasks; deliverable: test report)
- [ ] T024 Final refactor for clarity (comments/typing) in db/service modules (depends on T023; deliverable: cleaned code)
- [ ] T025 Prepare changes for review: ensure tasks checked, git status clean (depends on T024; deliverable: ready state)

---

## Dependencies & Execution Order

- Phase 1 → Phase 2 → User Stories (US1 P1, US2 P2, US3 P3) → Polish.
- Tests precede implementation within each story (red → green → refactor).
- T001 before any DB wiring; T003 before T004; T005 before T006; US1 depends on foundational; US2 depends on US1 completion of DB readiness; US3 depends on US2 service availability.

## Parallel Opportunities

- Setup tasks T001–T002 can run sequentially quickly; no parallel need.
- Within stories, test tasks marked sequential due to shared fixtures; implementations follow tests.
- Different stories could be parallel after foundational, but recommended order P1 → P2 → P3 for simplicity.

## MVP Scope

- MVP is US1: startup with Neon DB and create_all verified. US2/US3 extend functionality.
