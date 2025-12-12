---

description: "Task list for FastAPI health service"
---

# Tasks: FastAPI Health Service

**Input**: Design documents from `/specs/002-fastapi-health/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are mandatory and written first (pytest). Each story begins with failing tests; maintain ≥80% project coverage (target 100% for minimal scope).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- Source: `src/`
- Tests: `tests/` at repository root
- Tooling: UV for dependency/env management; pytest/pytest-cov for tests; FastAPI/uvicorn for service

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project directories (`src/api`, `tests/unit`, `tests/integration`) via CLI (depends on none)
- [X] T002 Add dependencies with UV (`fastapi`, `uvicorn`, `pytest`, `pytest-cov`) (depends on T001; deliverable: pyproject/uv.lock)
- [X] T003 Add/update pytest config for coverage gates (`pytest.ini`) targeting `src` (depends on T002; deliverable: pytest.ini)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core scaffolding before user stories

- [X] T004 Stub FastAPI app factory and uvicorn entry in `src/main.py` (no logic) (depends on T003)
- [X] T005 Stub health router module `src/api/health.py` with placeholder handler (depends on T004)
- [X] T006 Human review checkpoint; prep commit if approved (depends on T005)

---

## Phase 3: User Story 1 - Start backend service (Priority: P1) 🎯 MVP

**Goal**: Service starts via uvicorn without errors.

**Independent Test**: Run uvicorn entry; process starts and stays healthy.

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [X] T007 [US1] Write failing unit test for app creation (FastAPI app exists) in `tests/unit/test_health.py` (depends on T005)
- [X] T008 [P] [US1] Write failing integration test stub to invoke app via TestClient (startup path) in `tests/integration/test_health_live.py` (depends on T005)

### Implementation for User Story 1

- [X] T009 [US1] Implement FastAPI app factory and uvicorn entry in `src/main.py` (depends on T007)
- [X] T010 [US1] Refactor/cleanup with docstrings/type hints for app entry in `src/main.py` (depends on T009)
- [X] T011 Human review checkpoint; commit if approved (depends on T010)

---

## Phase 4: User Story 2 - Check health endpoint (Priority: P1)

**Goal**: `/health` returns 200 JSON `{"status": "ok"}` with no auth/DB.

**Independent Test**: `curl http://localhost:<port>/health` returns 200 and JSON status.

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [X] T012 [US2] Write failing unit test for `/health` handler using FastAPI TestClient in `tests/unit/test_health.py` (depends on T009)
- [X] T013 [P] [US2] Write failing integration test for `/health` in `tests/integration/test_health_live.py` (depends on T009)

### Implementation for User Story 2

- [X] T014 [US2] Implement health router/endpoint in `src/api/health.py` returning JSON status (depends on T012)
- [X] T015 [US2] Wire router into app in `src/main.py` (depends on T014)
- [X] T016 [US2] Refactor/cleanup, ensure type hints/docstrings and contract alignment in `src/api/health.py` and `src/main.py` (depends on T015)
- [X] T017 Human review checkpoint; commit if approved (depends on T016)

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final checks, docs, and coverage

- [X] T018 Run full test suite with coverage report (`uv run pytest --cov=src --cov-report=term-missing`) (depends on T017)
- [X] T019 Update quickstart/docs if commands changed in `specs/002-fastapi-health/quickstart.md` (depends on T018)
- [X] T020 Final human review and readiness to open PR/commit (depends on T019)

---

## Dependencies & Execution Order

- Setup (Phase 1) → Foundational (Phase 2) → US1 (Phase 3) → US2 (Phase 4) → Polish (Phase 5)
- Within each story: tests (red) → implementations (green) → refactor → human review/commit.

## Parallel Opportunities

- Marked [P] tasks (integration test authoring) can run alongside unit test authoring within the same story once prerequisites are met.

## Implementation Strategy

- MVP first: get app starting (US1) to enable endpoint tests.
- Then add `/health` (US2) with TDD.
- Validate at each human review checkpoint and commit before proceeding.
