---

description: "Task list template for feature implementation"
---

# Tasks: MCP Server Extraction

**Input**: Design documents from `/specs/015-mcp-server-extraction/`
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

**Purpose**: Prepare MCP server scaffolding and dependency setup

- [x] T001 Ensure Official MCP SDK dependency is added in `pyproject.toml` and `uv.lock`
- [x] T002 Create MCP server package structure in `mcp_server/` with `app.py` and `tools.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Implement MCP tool wrappers and DB access

- [x] T003 Define MCP tool schemas and registration in `mcp_server/tools.py`
- [x] T004 Implement MCP DB session helpers in `mcp_server/app.py`

**Checkpoint**: MCP server can register tools and connect to DB

---

## Phase 3: User Story 1 - Task tools available via MCP (Priority: P1) 🎯 MVP

**Goal**: MCP server exposes all task tools with correct behavior

**Independent Test**: Call MCP tools and verify task operations in DB

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T005 [P] [US1] Contract test for MCP tool payloads in `tests/contract/test_mcp_tools_contract.py`
- [x] T006 [P] [US1] Integration test for MCP add/list/complete/delete/update in `tests/integration/test_mcp_tools_api.py`

### Implementation for User Story 1

- [x] T007 [US1] Implement MCP tool handlers using existing task repo logic in `mcp_server/tools.py`
- [x] T008 [US1] Wire MCP server entrypoint in `mcp_server/app.py`

**Checkpoint**: MCP tools operate against Neon DB with ownership enforcement

---

## Phase 4: User Story 2 - Chat uses MCP tools without behavior change (Priority: P2)

**Goal**: Backend agent uses MCP tools and preserves Step 5 behavior

**Independent Test**: Run Step 5 chat scenarios and confirm MCP-backed tool calls

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T009 [P] [US2] Contract test for MCP-backed tool_calls in chat in `tests/contract/test_chat_mcp_tool_calls_contract.py`
- [x] T010 [P] [US2] Integration test for Step 5 commands via MCP in `tests/integration/test_chat_mcp_behavior_api.py`

### Implementation for User Story 2

- [x] T011 [US2] Add MCP client wrapper in `src/services/mcp_client.py`
- [x] T012 [US2] Update agent tool execution to call MCP client in `src/services/agent_runtime.py`
- [x] T013 [US2] Ensure tool_calls capture MCP results in `src/services/agent_runtime.py`

**Checkpoint**: Chat behavior matches Step 5 with MCP-backed tools

---

## Phase 5: User Story 3 - Ownership and statelessness preserved (Priority: P3)

**Goal**: MCP tools enforce ownership and backend remains stateless

**Independent Test**: Attempt cross-user task operations via MCP and chat

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T014 [P] [US3] Contract test for ownership errors in `tests/contract/test_mcp_ownership_contract.py`
- [x] T015 [P] [US3] Integration test for ownership via chat in `tests/integration/test_chat_mcp_ownership_api.py`

### Implementation for User Story 3

- [x] T016 [US3] Enforce not-found style errors in MCP tool handlers in `mcp_server/tools.py`

**Checkpoint**: Ownership violations do not leak task existence

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validation and documentation touch-ups

- [x] T017 Run quickstart validation in `specs/015-mcp-server-extraction/quickstart.md`
- [x] T018 Update implementation notes if needed in `specs/015-mcp-server-extraction/plan.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational
- **User Story 2 (P2)**: Starts after User Story 1 MCP tool availability
- **User Story 3 (P3)**: Starts after User Story 1 MCP tool availability

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- MCP tool handlers before backend integration
- Story complete before moving to next priority

### Parallel Opportunities

- T005–T006 can run in parallel (different files)
- T009–T010 can run in parallel (different files)
- T014–T015 can run in parallel (different files)

---

## Parallel Example: User Story 1

```bash
Task: "Contract test for MCP tool payloads in tests/contract/test_mcp_tools_contract.py"
Task: "Integration test for MCP add/list/complete/delete/update in tests/integration/test_mcp_tools_api.py"
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
