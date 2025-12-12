---

description: "Task list for interactive CLI todo app"
---

# Tasks: Interactive CLI Todo App

**Input**: Design documents from `/specs/001-interactive-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are mandatory and written first (pytest). Each story begins with failing tests; maintain ≥80% project coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Language/Version: Python 3.12+ with type hints everywhere; use dataclasses for data structures
- Tooling: UV for dependency/env management; pytest for tests; git tracks all project files

<!--
  ============================================================================
  IMPORTANT: The tasks below are tailored to the interactive CLI todo app.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize project with UV in repo root (`uv init`) to create baseline structure and config (depends on none; deliverable: pyproject/uv.lock)
- [X] T002 Create project directories per plan (`src/models`, `src/services`, `src/cli`, `tests/unit`, `tests/integration`, `tests/contract`) via CLI (depends on T001)
- [X] T003 Add dependencies with UV (`uv add typer questionary rich`) and ensure pytest available (depends on T002; deliverable: pyproject/uv.lock)
- [X] T004 Add pytest config/coverage defaults if missing (e.g., `pytest.ini`) with 80% gate (depends on T003; deliverable: pytest.ini)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core scaffolding that MUST be complete before any user story

- [X] T005 Stub `Task` dataclass module in `src/models/task.py` (id, title, completed) with type hints (depends on T004)
- [X] T006 Stub in-memory task store API signatures in `src/services/task_store.py` (create/list/update/delete/toggle, no logic) (depends on T005)
- [X] T007 Stub CLI entry and app loop wiring in `src/main.py` and `src/cli/app.py` using Typer to call a placeholder run loop (depends on T006)
- [X] T008 Stub menu/render helpers in `src/cli/menu.py` and `src/cli/render.py` with TODO placeholders (depends on T007)
- [X] T009 Human review checkpoint; prep commit if approved (depends on T008)

---

## Phase 3: User Story 1 - Start and view tasks (Priority: P1) 🎯 MVP

**Goal**: Launch app, see main menu, view tasks/empty state without restart

**Independent Test**: Launch, choose “View tasks,” see table or empty-state, return to menu.

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [X] T010 [US1] Write failing unit tests for listing tasks/empty state in `tests/unit/test_task_store.py` (depends on T006)
- [X] T011 [P] [US1] Write failing integration/menu test for view flow in `tests/integration/test_cli_flow.py` (depends on T007)

### Implementation for User Story 1

- [X] T012 [US1] Implement list/read helpers in `src/services/task_store.py` to return task data for rendering (depends on T010)
- [X] T013 [US1] Implement render for view/empty state with Rich in `src/cli/render.py` (depends on T012)
- [X] T014 [US1] Implement menu option wiring for “View tasks” in `src/cli/menu.py` and loop handling in `src/cli/app.py` (depends on T013 and T011)
- [X] T015 [US1] Refactor/cleanup for view path (types/docstrings) in `src/services/task_store.py` and `src/cli/*` (depends on T014)
- [X] T016 Human review checkpoint; commit if approved (depends on T015)

---

## Phase 4: User Story 2 - Add tasks via menu (Priority: P1)

**Goal**: Add tasks with non-empty titles and see them in the list

**Independent Test**: From menu, add task with title → appears in view; empty title rejected; app stays running.

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [ ] T017 [US2] Write failing unit tests for add + validation (non-empty) in `tests/unit/test_task_store.py` (depends on T012)
- [ ] T018 [P] [US2] Write failing integration test for add flow/menu return in `tests/integration/test_cli_flow.py` (depends on T016)

### Implementation for User Story 2

- [X] T019 [US2] Implement add logic (unique ID/index, default incomplete, validation) in `src/services/task_store.py` (depends on T017)
- [X] T018 [P] [US2] Write failing integration test for add flow/menu return in `tests/integration/test_cli_flow.py` (depends on T016)
- [X] T020 [US2] Implement add prompts and menu action in `src/cli/menu.py` and `src/cli/app.py` using Questionary (depends on T019 and T018)
- [X] T021 [US2] Implement render confirmation/update view for added task in `src/cli/render.py` (depends on T020)
- [X] T022 [US2] Refactor/cleanup add path (types/docstrings) in `src/services/task_store.py` and `src/cli/*` (depends on T021)
- [X] T023 Human review checkpoint; commit if approved (depends on T022)

---

## Phase 5: User Story 3 - Manage existing tasks (Priority: P2)

**Goal**: Update, delete, and toggle completion by ID/index with graceful errors

**Independent Test**: Add a task, then update title, toggle status, delete; invalid IDs show “task not found” and app stays running.

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [X] T024 [US3] Write failing unit tests for update (valid/invalid ID, non-empty title) in `tests/unit/test_task_store.py` (depends on T022)
- [X] T025 [US3] Write failing unit tests for delete (valid/invalid ID) in `tests/unit/test_task_store.py` (depends on T024)
- [X] T026 [US3] Write failing unit tests for toggle (valid/invalid ID) in `tests/unit/test_task_store.py` (depends on T025)
- [X] T027 [P] [US3] Write failing integration test covering update/delete/toggle menu flows in `tests/integration/test_cli_flow.py` (depends on T026)

### Implementation for User Story 3

- [X] T028 [US3] Implement update logic in `src/services/task_store.py` (depends on T024)
- [X] T029 [US3] Implement delete logic in `src/services/task_store.py` (depends on T025)
- [X] T030 [US3] Implement toggle logic in `src/services/task_store.py` (depends on T026)
- [X] T031 [US3] Wire update/delete/toggle menu actions with Questionary prompts and Rich messages in `src/cli/menu.py` and `src/cli/app.py` (depends on T028, T029, T030, and T027)
- [X] T032 [US3] Refactor/cleanup manage paths; ensure consistent error messaging and type hints in `src/services/task_store.py` and `src/cli/*` (depends on T031)
- [X] T033 Human review checkpoint; commit if approved (depends on T032)

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final checks, docs, and coverage

- [X] T034 Run full test suite with coverage report (`uv run pytest --cov=src --cov-report=term-missing`) (depends on T033)
- [X] T035 Update quickstart/docs if commands changed in `specs/001-interactive-todo-cli/quickstart.md` (depends on T034)
- [X] T036 Final human review and readiness to open PR/commit (depends on T035)

---

## Dependencies & Execution Order

- Setup (Phase 1) → Foundational (Phase 2) → US1 (Phase 3) → US2 (Phase 4) → US3 (Phase 5) → Polish (Phase 6)
- Within each story: tests (red) → implementations (green) → refactor → human review/commit.

## Parallel Opportunities

- Marked [P] tasks (integration test writing) can run alongside unit test authoring within the same story once prerequisites are met.
- Tasks in different stories run only after prior stories complete per dependency chain.

## Implementation Strategy

- MVP First: Complete US1 (view/menu) to deliver a usable app shell.
- Incremental Delivery: Add creation (US2), then manage actions (US3).
- Validate after each human review checkpoint and commit before proceeding.
