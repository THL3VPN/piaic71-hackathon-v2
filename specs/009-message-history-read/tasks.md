# Tasks: Message History Read

**Input**: Design documents from `/specs/009-message-history-read/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are mandatory and written first (pytest). Each story begins with failing tests; maintain ≥80% project coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Confirm project readiness for new endpoint work

- [x] T001 Verify existing FastAPI app wiring for conversations in src/main.py
- [x] T002 Verify existing auth dependency usage for protected endpoints in src/services/auth.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared behaviors required before user stories

- [x] T003 Verify repository layer supports conversation ownership checks in src/services/message_repo.py
- [x] T004 Verify message schema response model exists in src/api/schemas.py

---

## Phase 3: User Story 1 - Read conversation history (Priority: P1) 🎯 MVP

**Goal**: Allow authenticated users to retrieve ordered message history for their own conversation.

**Independent Test**: Request history with a valid token and conversation ID; verify ordered messages and 404 for non-owners.

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T005 [P] [US1] Contract test for GET /api/conversations/{conversation_id}/messages in tests/contract/test_message_history_contract.py
- [x] T006 [P] [US1] Integration test for history retrieval in tests/integration/test_message_history_api.py
- [x] T007 [P] [US1] Unit test for ownership and ordering query in tests/unit/test_message_history_repo.py

### Implementation for User Story 1

- [x] T008 [US1] Add list_messages helper in src/services/message_repo.py (ownership check + ordering)
- [x] T009 [US1] Add GET history endpoint in src/api/conversations.py
- [x] T010 [US1] Add query validation for limit in src/api/conversations.py

**Checkpoint**: User Story 1 history retrieval is functional and tested.

---

## Phase 4: User Story 2 - Control history size (Priority: P2)

**Goal**: Support client-provided limits with default and clamp behavior.

**Independent Test**: Request history with limit values within, above, and below allowed ranges.

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T011 [P] [US2] Contract test for limit behavior in tests/contract/test_message_history_contract.py
- [x] T012 [P] [US2] Integration test for limit behavior in tests/integration/test_message_history_api.py
- [x] T013 [P] [US2] Unit test for limit clamping in tests/unit/test_message_history_repo.py

### Implementation for User Story 2

- [x] T014 [US2] Enforce limit default/clamp in src/services/message_repo.py
- [x] T015 [US2] Wire limit param handling in src/api/conversations.py

**Checkpoint**: User Story 2 limit behavior is functional and tested.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [x] T016 [P] Run quickstart validation steps in specs/009-message-history-read/quickstart.md
- [x] T017 Update documentation references in specs/009-message-history-read/plan.md if needed

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Phase 2; no dependency on US2
- **User Story 2 (P2)**: Starts after Phase 2; depends on US1 implementation for shared endpoint

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Service query changes before endpoint wiring
- Endpoint changes before integration validation

### Parallel Opportunities

- T005/T006/T007 can run in parallel (tests in different files)
- T011/T012/T013 can run in parallel (tests in different files)

---

## Parallel Example: User Story 1

```bash
Task: "Contract test for GET history in tests/contract/test_message_history_contract.py"
Task: "Integration test for history retrieval in tests/integration/test_message_history_api.py"
Task: "Unit test for ownership and ordering query in tests/unit/test_message_history_repo.py"
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
4. Finish Polish phase
