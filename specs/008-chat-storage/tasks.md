---

description: "Task list for chat storage persistence"
---

# Tasks: Chat Storage Persistence

**Input**: Design documents from `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/chat-storage.openapi.yaml, research.md

**Tests**: TDD required. Each operation starts with RED tests, then GREEN implementation, then REFACTOR.

**Organization**: Tasks grouped by user story to keep each story independently testable.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Minimal scaffolding to support TDD flow

- [x] T001 Create empty chat storage test files in `/home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_chat_storage_contract.py`, `/home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_storage_api.py`, `/home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_conversation_repo.py`, `/home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_message_repo.py` (deliverable: empty test modules)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared helpers required by all stories

- [x] T002 Add chat auth header helper in `/home/aie/all_data/piaic71-hackathon-v2/tests/conftest.py` (deliverable: reusable auth header factory)

**Checkpoint**: Foundation ready. Pause for human review; commit after approval.

---

## Phase 3: User Story 1 - Create a conversation (Priority: P1) 🎯 MVP

**Goal**: Authenticated user can create a conversation and receive its identifier.

**Independent Test**: POST `/api/conversations` returns a new conversation id tied to the authenticated user.

### Operation: Create Conversation — RED Tests

- [x] T003 [P] [US1] Write failing contract test for POST `/api/conversations` in `/home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_chat_storage_contract.py` (deliverable: contract assertions) depends on T001
- [x] T004 [P] [US1] Write failing integration test for create conversation in `/home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_storage_api.py` (deliverable: integration scenario) depends on T001,T002
- [x] T005 [P] [US1] Write failing unit test for conversation create repo in `/home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_conversation_repo.py` (deliverable: repo test) depends on T001

### Operation: Create Conversation — GREEN Implementation

- [x] T006 [P] [US1] Add Conversation model in `/home/aie/all_data/piaic71-hackathon-v2/src/models/conversation.py` (deliverable: SQLModel for conversations) depends on T005
- [x] T007 [P] [US1] Add conversation response schema in `/home/aie/all_data/piaic71-hackathon-v2/src/api/schemas.py` (deliverable: ConversationCreateResponse) depends on T003
- [x] T008 [US1] Implement conversation repository create in `/home/aie/all_data/piaic71-hackathon-v2/src/services/conversation_repo.py` (deliverable: create function) depends on T006
- [x] T009 [US1] Implement POST `/api/conversations` endpoint in `/home/aie/all_data/piaic71-hackathon-v2/src/api/conversations.py` (deliverable: create endpoint) depends on T007,T008
- [x] T010 [US1] Register conversations router in `/home/aie/all_data/piaic71-hackathon-v2/src/main.py` (deliverable: router mount) depends on T009

### Operation: Create Conversation — REFACTOR

- [ ] T011 [US1] Refactor conversation endpoint for clarity in `/home/aie/all_data/piaic71-hackathon-v2/src/api/conversations.py` (deliverable: cleaned endpoint) depends on T009
- [ ] T012 [US1] Refactor conversation repo for clarity in `/home/aie/all_data/piaic71-hackathon-v2/src/services/conversation_repo.py` (deliverable: cleaned repository) depends on T008

**Checkpoint**: Pause for human review; commit after approval.

---

## Phase 4: User Story 2 - Append a message (Priority: P2)

**Goal**: Authenticated user can append a message to their conversation.

**Independent Test**: POST `/api/conversations/{conversation_id}/messages` stores a message when the conversation is owned by the user.

### Operation: Append Message — RED Tests

- [ ] T013 [P] [US2] Write failing contract test for POST `/api/conversations/{conversation_id}/messages` in `/home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_chat_storage_contract.py` (deliverable: contract assertions) depends on T003
- [ ] T014 [P] [US2] Write failing integration test for append message in `/home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_storage_api.py` (deliverable: integration scenario) depends on T004
- [ ] T015 [P] [US2] Write failing unit tests for message repo create + ownership in `/home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_message_repo.py` (deliverable: repo tests) depends on T001

### Operation: Append Message — GREEN Implementation

- [ ] T016 [P] [US2] Add Message model in `/home/aie/all_data/piaic71-hackathon-v2/src/models/message.py` (deliverable: SQLModel for messages) depends on T015
- [ ] T017 [P] [US2] Add message schemas in `/home/aie/all_data/piaic71-hackathon-v2/src/api/schemas.py` (deliverable: MessageCreate/MessageRead) depends on T013
- [ ] T018 [US2] Implement message repository create in `/home/aie/all_data/piaic71-hackathon-v2/src/services/message_repo.py` (deliverable: create function with ownership check) depends on T016,T008
- [ ] T019 [US2] Update conversation updated_at on message append in `/home/aie/all_data/piaic71-hackathon-v2/src/services/conversation_repo.py` (deliverable: updated_at update) depends on T018
- [ ] T020 [US2] Implement POST message endpoint in `/home/aie/all_data/piaic71-hackathon-v2/src/api/conversations.py` (deliverable: append endpoint) depends on T017,T018,T019

### Operation: Append Message — REFACTOR

- [ ] T021 [US2] Refactor message endpoint for clarity in `/home/aie/all_data/piaic71-hackathon-v2/src/api/conversations.py` (deliverable: cleaned endpoint) depends on T020
- [ ] T022 [US2] Refactor message repo for clarity in `/home/aie/all_data/piaic71-hackathon-v2/src/services/message_repo.py` (deliverable: cleaned repository) depends on T018

**Checkpoint**: Pause for human review; commit after approval.

---

## Phase 5: User Story 3 - Retrieve message history (Priority: P3)

**Goal**: Authenticated user can retrieve message history in chronological order with limits.

**Independent Test**: GET `/api/conversations/{conversation_id}/messages` returns ordered history with default limit 50.

### Operation: Retrieve History — RED Tests

- [ ] T023 [P] [US3] Write failing contract test for GET `/api/conversations/{conversation_id}/messages` in `/home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_chat_storage_contract.py` (deliverable: contract assertions) depends on T013
- [ ] T024 [P] [US3] Write failing integration test for history retrieval ordering/limit in `/home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_storage_api.py` (deliverable: integration scenario) depends on T014
- [ ] T025 [P] [US3] Write failing unit tests for history query ordering/limit in `/home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_message_repo.py` (deliverable: repo tests) depends on T015

### Operation: Retrieve History — GREEN Implementation

- [ ] T026 [US3] Implement history query ordering/limit in `/home/aie/all_data/piaic71-hackathon-v2/src/services/message_repo.py` (deliverable: list function) depends on T025
- [ ] T027 [US3] Add limit validation in `/home/aie/all_data/piaic71-hackathon-v2/src/api/conversations.py` (deliverable: limit validation) depends on T026
- [ ] T028 [US3] Implement GET history endpoint in `/home/aie/all_data/piaic71-hackathon-v2/src/api/conversations.py` (deliverable: history endpoint) depends on T023,T027

### Operation: Retrieve History — REFACTOR

- [ ] T029 [US3] Refactor history endpoint for clarity in `/home/aie/all_data/piaic71-hackathon-v2/src/api/conversations.py` (deliverable: cleaned endpoint) depends on T028
- [ ] T030 [US3] Refactor message history repo for clarity in `/home/aie/all_data/piaic71-hackathon-v2/src/services/message_repo.py` (deliverable: cleaned repository) depends on T026

**Checkpoint**: Pause for human review; commit after approval.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation and cleanup affecting multiple stories

- [ ] T031 [P] Update quickstart endpoints and examples in `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/quickstart.md` (deliverable: updated usage notes)
- [ ] T032 [P] Update contracts if needed based on implementation in `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/contracts/chat-storage.openapi.yaml` (deliverable: aligned contract doc)

**Checkpoint**: Pause for human review; commit after approval.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1
- **User Story 1 (Phase 3)**: Depends on Phase 2
- **User Story 2 (Phase 4)**: Depends on Phase 3 (needs conversation ownership)
- **User Story 3 (Phase 5)**: Depends on Phase 4 (needs message persistence)
- **Polish (Phase 6)**: Depends on desired user stories complete

### User Story Dependencies

- **US1 (P1)**: Base conversation creation
- **US2 (P2)**: Requires US1 conversation persistence
- **US3 (P3)**: Requires US2 message persistence

### Parallel Opportunities

- Tests within a story marked [P] can run in parallel
- Model/schema tasks within a story marked [P] can run in parallel
- Documentation tasks in Phase 6 marked [P] can run in parallel

---

## Parallel Example: User Story 1

```text
T003 [P] [US1] Contract test for POST /api/conversations in /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_chat_storage_contract.py
T004 [P] [US1] Integration test for create conversation in /home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_storage_api.py
T005 [P] [US1] Unit test for conversation repo in /home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_conversation_repo.py
```

## Parallel Example: User Story 2

```text
T013 [P] [US2] Contract test for POST /api/conversations/{conversation_id}/messages in /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_chat_storage_contract.py
T014 [P] [US2] Integration test for append message in /home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_storage_api.py
T015 [P] [US2] Unit tests for message repo create in /home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_message_repo.py
```

## Parallel Example: User Story 3

```text
T023 [P] [US3] Contract test for GET /api/conversations/{conversation_id}/messages in /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_chat_storage_contract.py
T024 [P] [US3] Integration test for history retrieval in /home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_storage_api.py
T025 [P] [US3] Unit tests for message history query in /home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_message_repo.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 and Phase 2
2. Complete Phase 3 (US1) with RED → GREEN → REFACTOR
3. Pause for human review and commit on approval

### Incremental Delivery

1. US1: Create conversation (MVP)
2. US2: Append message
3. US3: Retrieve history
4. Polish and documentation

### Reversibility

- Each task touches a single file where possible.
- Each phase can be rolled back independently without affecting later phases.
- Review checkpoints provide safe commit boundaries.
