---

description: "Task list template for feature implementation"
---

# Tasks: Real-Time Agent Tool Calls

**Input**: Design documents from `/specs/013-agent-tool-calls/`
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

- [x] T001 Review current chat + agent runtime flow in `src/services/agent_runtime.py` and `src/services/chat_service.py`
- [x] T002 Review task tool surface for agent registration in `src/services/task_tools.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Prepare SDK wiring and tool adapters before user story work

- [x] T003 Ensure OpenAI Agents SDK dependency is present in `pyproject.toml` and `uv.lock`
- [x] T004 Add agent tool adapter module in `src/services/agent_tools.py`

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Execute task tools via chat (Priority: P1) 🎯 MVP

**Goal**: Agent executes task tools through chat requests

**Independent Test**: Send a chat request that creates a task and verify tool_calls returned and task exists

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T005 [P] [US1] Contract test for chat tool calls in `tests/contract/test_agent_tool_calls_contract.py`
- [x] T006 [P] [US1] Integration test for tool execution in `tests/integration/test_agent_tool_calls_api.py`
- [x] T007 [P] [US1] Unit test for agent runtime tool execution in `tests/unit/test_agent_runtime_tools.py`

### Implementation for User Story 1

- [x] T008 [US1] Wire tool registration helpers in `src/services/agent_tools.py`
- [x] T009 [US1] Implement Agents SDK execution in `src/services/agent_runtime.py`
- [x] T010 [US1] Map tool outputs into agent result in `src/services/agent_runtime.py`
- [x] T011 [US1] Ensure chat service returns tool_calls from agent runtime in `src/services/chat_service.py`

**Checkpoint**: User Story 1 is independently functional and testable

---

## Phase 4: User Story 2 - Tool call transparency (Priority: P2)

**Goal**: Response payload includes tool name, inputs, and outputs

**Independent Test**: Inspect tool_calls payload for name/arguments/result fields

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T012 [P] [US2] Contract test for tool call payload shape in `tests/contract/test_agent_tool_calls_contract.py`
- [x] T013 [P] [US2] Integration test for tool call payload contents in `tests/integration/test_agent_tool_calls_payload.py`

### Implementation for User Story 2

- [x] T014 [US2] Normalize tool call payload structure in `src/services/agent_runtime.py`
- [x] T015 [US2] Align response schema usage in `src/api/chat.py`

**Checkpoint**: User Stories 1 and 2 are independently functional

---

## Phase 5: User Story 3 - Robust tool error handling (Priority: P3)

**Goal**: Tool errors become friendly assistant replies without breaking auth/validation

**Independent Test**: Trigger a tool error and verify friendly response and safe payload

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T016 [P] [US3] Integration test for tool error handling in `tests/integration/test_agent_tool_calls_errors.py`

### Implementation for User Story 3

- [x] T017 [US3] Map tool errors to friendly responses in `src/services/agent_runtime.py`
- [x] T018 [US3] Ensure error tool_calls are captured in `src/services/agent_runtime.py`

**Checkpoint**: All user stories are independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation and documentation touch-ups

- [x] T019 Run quickstart validation in `specs/013-agent-tool-calls/quickstart.md`
- [x] T020 Update implementation notes if needed in `specs/013-agent-tool-calls/plan.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational
- **User Story 2 (P2)**: Starts after Foundational; builds on US1 payloads
- **User Story 3 (P3)**: Starts after Foundational; builds on US1 execution

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Agent tool adapters before runtime integration
- Runtime integration before response wiring
- Story complete before moving to next priority

### Parallel Opportunities

- T005–T007 can run in parallel (different files)
- T012–T013 can run in parallel (different files)

---

## Parallel Example: User Story 1

```bash
Task: "Contract test for chat tool calls in tests/contract/test_agent_tool_calls_contract.py"
Task: "Integration test for tool execution in tests/integration/test_agent_tool_calls_api.py"
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
