# Tasks: Stateless Chat Endpoint

**Input**: Design documents from `/specs/010-stateless-chat/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are mandatory and written first (pytest). Each story begins with failing tests; maintain ≥80% project coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm repository readiness for the chat endpoint

- [x] T001 Verify conversation/message repos are available in src/services/
- [x] T002 Verify auth context dependency wiring in src/services/auth.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared schema and routing dependencies

- [x] T003 Verify message history retrieval helper exists in src/services/message_repo.py
- [x] T004 Add request/response schemas for chat in src/api/schemas.py

---

## Phase 3: User Story 1 - Send a chat message (Priority: P1) 🎯 MVP

**Goal**: Accept a message, store it, generate a dummy response, store it, and return conversation_id with tool_calls empty.

**Independent Test**: POST /api/chat without conversation_id returns a response and stores two messages.

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T005 [P] [US1] Contract test for POST /api/chat in tests/contract/test_stateless_chat_contract.py
- [x] T006 [P] [US1] Integration test for new conversation flow in tests/integration/test_stateless_chat_api.py
- [x] T007 [P] [US1] Unit test for chat service flow in tests/unit/test_stateless_chat_service.py

### Implementation for User Story 1

- [x] T008 [US1] Add chat service helper in src/services/chat_service.py (history fetch, message persistence, dummy response)
- [x] T009 [US1] Add POST /api/chat endpoint in src/api/chat.py
- [x] T010 [US1] Wire chat router in src/main.py

**Checkpoint**: User Story 1 is fully functional and testable independently.

---

## Phase 4: User Story 2 - Enforce ownership and input validity (Priority: P2)

**Goal**: Enforce ownership checks and validation errors for invalid inputs.

**Independent Test**: Invalid conversation_id returns 404; missing/invalid message returns 422.

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T011 [P] [US2] Contract test for ownership and validation errors in tests/contract/test_stateless_chat_contract.py
- [x] T012 [P] [US2] Integration test for ownership and validation errors in tests/integration/test_stateless_chat_api.py
- [x] T013 [P] [US2] Unit test for ownership enforcement in tests/unit/test_stateless_chat_service.py

### Implementation for User Story 2

- [x] T014 [US2] Enforce ownership check in src/services/chat_service.py
- [x] T015 [US2] Add request validation in src/api/chat.py

**Checkpoint**: User Story 2 validation and ownership checks are enforced.

---

## Phase 5: User Story 3 - Retrieve history per request (Priority: P3)

**Goal**: Ensure history retrieval occurs on each request to prove statelessness.

**Independent Test**: Consecutive requests use stored history without in-memory state.

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T016 [P] [US3] Contract test for stateless history usage in tests/contract/test_stateless_chat_contract.py
- [x] T017 [P] [US3] Integration test for history retrieval in tests/integration/test_stateless_chat_api.py
- [x] T018 [P] [US3] Unit test for history retrieval in tests/unit/test_stateless_chat_service.py

### Implementation for User Story 3

- [x] T019 [US3] Ensure history retrieval is part of chat flow in src/services/chat_service.py
- [ ] T020 [US3] Add history fetch limit handling in src/services/chat_service.py

**Checkpoint**: User Story 3 confirms stateless behavior.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation updates

- [ ] T021 [P] Run quickstart validation steps in specs/010-stateless-chat/quickstart.md
- [ ] T022 Update documentation references in specs/010-stateless-chat/plan.md if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2; no dependency on other stories
- **User Story 2 (P2)**: Starts after Phase 2; builds on US1 flow
- **User Story 3 (P3)**: Starts after Phase 2; extends US1 flow

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Service changes before endpoint wiring
- Endpoint wiring before integration validation

### Parallel Opportunities

- T005/T006/T007 can run in parallel (tests in different files)
- T011/T012/T013 can run in parallel (tests in different files)
- T016/T017/T018 can run in parallel (tests in different files)

---

## Parallel Example: User Story 1

```bash
Task: "Contract test for POST /api/chat in tests/contract/test_stateless_chat_contract.py"
Task: "Integration test for new conversation flow in tests/integration/test_stateless_chat_api.py"
Task: "Unit test for chat service flow in tests/unit/test_stateless_chat_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Stop and validate User Story 1 independently

### Incremental Delivery

1. Complete Setup + Foundational
2. Add User Story 1 → Test independently → Deploy
3. Add User Story 2 → Test independently → Deploy
4. Add User Story 3 → Test independently → Deploy
5. Finish Polish phase
