---

description: "Task list template for feature implementation"
---

# Tasks: Task Tools Layer

**Input**: Design documents from `/specs/011-task-tools/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are mandatory and written first (pytest). Each story begins with failing tests; maintain ≥80% project coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project
- Language/Version: Python 3.12+ with type hints everywhere; use dataclasses for data structures
- Tooling: UV for dependency/env management; pytest for tests; git tracks all project files

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm reuse points and prepare for tool layer work

- [x] T001 Review task persistence APIs in `src/services/task_repo.py` and `src/models/task.py` for tool reuse

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish shared tool module surface before user story work

- [x] T002 Create tool module shell with domain error placeholders in `src/services/task_tools.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Deterministic Task Tools (Priority: P1) 🎯 MVP

**Goal**: Deterministic, user-scoped tool functions for core task operations

**Independent Test**: Invoke tools directly via unit tests and verify structured outputs

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T003 [US1] Add failing add_task tests in `tests/unit/test_task_tools.py`
- [x] T004 [US1] Add failing list_tasks tests in `tests/unit/test_task_tools.py`
- [x] T005 [US1] Add failing complete_task and delete_task tests in `tests/unit/test_task_tools.py`
- [x] T006 [US1] Add failing update_task happy-path tests in `tests/unit/test_task_tools.py`

### Implementation for User Story 1

- [x] T007 [US1] Implement add_task tool in `src/services/task_tools.py`
- [x] T008 [US1] Implement list_tasks tool in `src/services/task_tools.py`
- [x] T009 [US1] Implement complete_task and delete_task tools in `src/services/task_tools.py`
- [x] T010 [US1] Implement update_task tool in `src/services/task_tools.py`
- [x] T011 [US1] Refactor tool result dataclasses and shared helpers in `src/services/task_tools.py`
- [x] T012 [US1] Record US1 review checkpoint in `specs/011-task-tools/tasks.md`

**Checkpoint**: User Story 1 is independently functional and testable

---

## Phase 4: User Story 2 - Ownership and Validation Enforcement (Priority: P2)

**Goal**: Enforce ownership and validation with domain errors

**Independent Test**: Attempt cross-user access and invalid inputs in unit tests

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T013 [US2] Add failing ownership and invalid-input tests in `tests/unit/test_task_tools.py`

### Implementation for User Story 2

- [x] T014 [US2] Implement ownership enforcement and InvalidInput handling in `src/services/task_tools.py`
- [x] T015 [US2] Refactor domain error mapping in `src/services/task_tools.py`
- [x] T016 [US2] Record US2 review checkpoint in `specs/011-task-tools/tasks.md`

**Checkpoint**: User Stories 1 and 2 are independently functional

---

## Phase 5: User Story 3 - Tool Isolation from Chat Context (Priority: P3)

**Goal**: Tools remain callable without chat or HTTP objects

**Independent Test**: Call tools directly without request/chat context

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T017 [US3] Add failing isolation tests in `tests/unit/test_task_tools.py`

### Implementation for User Story 3

- [x] T018 [US3] Ensure tool module has no HTTP/chat imports in `src/services/task_tools.py`
- [x] T019 [US3] Record US3 review checkpoint in `specs/011-task-tools/tasks.md`

**Checkpoint**: All user stories are independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation and documentation touch-ups

- [x] T020 Run quickstart validation in `specs/011-task-tools/quickstart.md`
- [x] T021 Update implementation notes if needed in `specs/011-task-tools/plan.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational
- **User Story 2 (P2)**: Starts after Foundational; builds on shared tool surface
- **User Story 3 (P3)**: Starts after Foundational; verifies isolation

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Tool functions before refactors
- Story complete before moving to next priority

### Parallel Opportunities

- T003–T006 can be split among contributors but touch the same file; run sequentially if solo
- Tool implementations in T007–T010 touch the same file; execute sequentially

---

## Parallel Example: User Story 1

```bash
# If multiple contributors are available, split test additions
Task: "Add failing add_task tests in tests/unit/test_task_tools.py"
Task: "Add failing list_tasks tests in tests/unit/test_task_tools.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run unit tests for tool functions

### Incremental Delivery

1. Add User Story 1 → Validate
2. Add User Story 2 → Validate
3. Add User Story 3 → Validate
4. Complete Polish tasks
