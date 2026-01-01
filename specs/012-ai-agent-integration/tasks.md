---

description: "Task list template for feature implementation"
---

# Tasks: AI Agent Integration

**Input**: Design documents from `/specs/012-ai-agent-integration/`
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

**Purpose**: Confirm existing chat/tool scaffolding and prepare for agent integration

- [x] T001 Review chat endpoint flow in `src/api/chat.py` and `src/services/chat_service.py`
- [x] T002 Review task tool layer in `src/services/task_tools.py` for integration points

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish agent factory and config layer before user story work

- [x] T003 Add provider config module in `src/services/chat_provider.py`
- [x] T004 Add model factory skeleton in `src/services/chat_model_factory.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Task Operations via Chat Agent (Priority: P1) 🎯 MVP

**Goal**: Agent executes tool-driven task operations via chat

**Independent Test**: Send chat requests that invoke tools and verify persisted messages + tool call payloads

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T005 [US1] Add failing contract test for agent chat response in `tests/contract/test_agent_chat_contract.py`
- [x] T006 [US1] Add failing integration test for tool invocation in `tests/integration/test_agent_chat_api.py`
- [x] T007 [US1] Add failing unit test for agent execution in `tests/unit/test_agent_runtime.py`

### Implementation for User Story 1

- [x] T008 [US1] Implement model factory selection in `src/services/chat_model_factory.py`
- [x] T009 [US1] Implement agent runtime using tools in `src/services/agent_runtime.py`
- [x] T010 [US1] Update chat service to call agent runtime in `src/services/chat_service.py`
- [x] T011 [US1] Update chat endpoint response to include tool calls in `src/api/chat.py`
- [x] T012 [US1] Refactor tool call persistence helpers in `src/services/chat_service.py`
- [x] T013 [US1] Record US1 review checkpoint in `specs/012-ai-agent-integration/tasks.md`

**Checkpoint**: User Story 1 is independently functional and testable

---

## Phase 4: User Story 2 - Provider Configuration via Environment (Priority: P2)

**Goal**: Provider and model can be swapped via configuration

**Independent Test**: Change env variables and ensure agent runs without code changes

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T014 [US2] Add failing config validation tests in `tests/unit/test_chat_provider.py`

### Implementation for User Story 2

- [x] T015 [US2] Implement config validation and errors in `src/services/chat_provider.py`
- [x] T016 [US2] Refactor factory wiring for provider config in `src/services/chat_model_factory.py`
- [x] T017 [US2] Record US2 review checkpoint in `specs/012-ai-agent-integration/tasks.md`

**Checkpoint**: User Stories 1 and 2 are independently functional

---

## Phase 5: User Story 3 - Stateless and Auditable Chat (Priority: P3)

**Goal**: Agent uses DB history and remains stateless

**Independent Test**: Ensure history reconstruction and statelessness via persisted messages

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T018 [US3] Add failing history reconstruction tests in `tests/integration/test_agent_chat_history.py`

### Implementation for User Story 3

- [x] T019 [US3] Ensure history limit is applied from config in `src/services/agent_runtime.py`
- [x] T020 [US3] Record US3 review checkpoint in `specs/012-ai-agent-integration/tasks.md`

**Checkpoint**: All user stories are independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation and documentation touch-ups

- [x] T021 Run quickstart validation in `specs/012-ai-agent-integration/quickstart.md`
- [x] T022 Update implementation notes if needed in `specs/012-ai-agent-integration/plan.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational
- **User Story 2 (P2)**: Starts after Foundational; builds on provider config
- **User Story 3 (P3)**: Starts after Foundational; builds on history usage

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Unit helpers before service integration
- Story complete before moving to next priority

### Parallel Opportunities

- T005–T007 can be split among contributors but touch different files
- T008–T011 touch different files and can be parallel if dependencies met

---

## Parallel Example: User Story 1

```bash
Task: "Add failing contract test for agent chat response in tests/contract/test_agent_chat_contract.py"
Task: "Add failing integration test for tool invocation in tests/integration/test_agent_chat_api.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Run agent chat tests

### Incremental Delivery

1. Add User Story 1 → Validate
2. Add User Story 2 → Validate
3. Add User Story 3 → Validate
4. Complete Polish tasks
