---

description: "Task list template for feature implementation"
---

# Tasks: Agent Behavior Validation

**Input**: Design documents from `/specs/014-agent-behavior-validation/`
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

**Purpose**: Confirm existing agent runtime prompt surface and chat behavior baseline

- [x] T001 Review current agent instructions and behavior surface in `src/services/agent_runtime.py`
- [x] T002 Review task tool behavior expectations in `src/services/task_tools.py` and `specs/014-agent-behavior-validation/spec.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish behavior prompt baseline and validation helpers

- [x] T003 Add test stubs/helpers for agent behavior validation in `tests/helpers/agent_behavior_fakes.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Execute natural language task commands (Priority: P1) 🎯 MVP

**Goal**: Agent maps natural language commands to correct tools with confirmations

**Independent Test**: Send chat commands for add/list and verify correct tool calls + confirmations

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T004 [P] [US1] Contract test for natural language task creation in `tests/contract/test_agent_behavior_create_contract.py`
- [x] T005 [P] [US1] Contract test for task listing intent mapping in `tests/contract/test_agent_behavior_list_contract.py`
- [x] T006 [P] [US1] Integration test for natural language add/list in `tests/integration/test_agent_behavior_add_list_api.py`

### Implementation for User Story 1

- [x] T007 [US1] Refine agent system instructions for add/list intents in `src/services/agent_runtime.py`
- [x] T008 [US1] Ensure confirmations are friendly and concise in `src/services/agent_runtime.py`

**Checkpoint**: User Story 1 is independently functional and testable

---

## Phase 4: User Story 2 - Handle ambiguity and tool chaining (Priority: P2)

**Goal**: Agent asks for clarification or deterministically chains tools

**Independent Test**: Send ambiguous delete/complete requests and verify list→action chain or clarification

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T009 [P] [US2] Contract test for tool chaining rules in `tests/contract/test_agent_behavior_chain_contract.py`
- [x] T010 [P] [US2] Integration test for ambiguous delete/complete requests in `tests/integration/test_agent_behavior_chain_api.py`

### Implementation for User Story 2

- [x] T011 [US2] Update agent instructions for deterministic tool chaining in `src/services/agent_runtime.py`
- [x] T012 [US2] Add clarification prompts for ambiguous task references in `src/services/agent_runtime.py`

**Checkpoint**: User Stories 1 and 2 are independently functional

---

## Phase 5: User Story 3 - Graceful error handling (Priority: P3)

**Goal**: Agent responds politely to missing tasks or unclear requests

**Independent Test**: Trigger task-not-found and verify friendly response without guessing

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T013 [P] [US3] Contract test for task-not-found response in `tests/contract/test_agent_behavior_errors_contract.py`
- [x] T014 [P] [US3] Integration test for error messaging in `tests/integration/test_agent_behavior_errors_api.py`

### Implementation for User Story 3

- [x] T015 [US3] Refine error-response guidance in `src/services/agent_runtime.py`

**Checkpoint**: All user stories are independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation and documentation touch-ups

- [x] T016 Run quickstart validation in `specs/014-agent-behavior-validation/quickstart.md`
- [x] T017 Update implementation notes if needed in `specs/014-agent-behavior-validation/plan.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational
- **User Story 2 (P2)**: Starts after Foundational; builds on US1 prompts
- **User Story 3 (P3)**: Starts after Foundational; builds on US1/US2 prompt behaviors

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Prompt updates after tests
- Story complete before moving to next priority

### Parallel Opportunities

- T004–T006 can run in parallel (different files)
- T009–T010 can run in parallel (different files)
- T013–T014 can run in parallel (different files)

---

## Parallel Example: User Story 1

```bash
Task: "Contract test for natural language task creation in tests/contract/test_agent_behavior_create_contract.py"
Task: "Contract test for task listing intent mapping in tests/contract/test_agent_behavior_list_contract.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run User Story 1 tests

### Incremental Delivery

1. Add User Story 1 -> Validate
2. Add User Story 2 -> Validate
3. Add User Story 3 -> Validate
4. Complete Polish tasks
