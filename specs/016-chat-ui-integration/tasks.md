---

description: "Task list template for feature implementation"
---

# Tasks: Frontend Chat UI Integration

**Input**: Design documents from `/specs/016-chat-ui-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are mandatory and written first (vitest). Each story begins with failing tests; maintain ≥80% project coverage.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `frontend/app/`, `frontend/lib/`, `frontend/tests/`
- Language/Version: TypeScript 5.3 + React 18.3 (Next.js App Router)
- Tooling: npm for frontend deps, vitest for tests; backend remains unchanged

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare Chat UI scaffolding and dependencies

- [x] T001 Create chat UI route shell in `frontend/app/chat/page.tsx`
- [x] T002 Verify OpenAI ChatKit package name and add dependency in `frontend/package.json`
- [x] T003 [P] Define chat UI types in `frontend/lib/types.ts`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared utilities required by all user stories

- [x] T004 [P] Add chat API client for `/api/chat` and history in `frontend/lib/chat.ts`
- [x] T005 [P] Add conversation storage helpers in `frontend/lib/chatStorage.ts`
- [x] T006 Update logout to clear conversation state in `frontend/lib/auth.ts`

**Checkpoint**: Chat API client and storage helpers are available

---

## Phase 3: User Story 1 - Start a Chat and Get a Reply (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can send a message and see the assistant reply

**Independent Test**: Use Chat UI to send a message and render assistant reply with loading state

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T007 [P] [US1] RED chat send flow test in `frontend/tests/chat-page.test.tsx`
- [x] T008 [P] [US1] RED loading + optimistic message test in `frontend/tests/chat-page.test.tsx`

### Implementation for User Story 1

- [x] T009 [US1] Implement chat composer + message list using ChatKit in `frontend/app/chat/page.tsx`
- [x] T010 [US1] Wire send flow to chat client in `frontend/app/chat/page.tsx`
- [x] T011 [US1] Add chat entry link/button in `frontend/app/tasks/page.tsx`

**Checkpoint**: User can send a message and receive a reply in the chat UI

---

## Phase 4: User Story 2 - Resume Chat After Refresh (Priority: P2)

**Goal**: Conversation continuity across refreshes with message history

**Independent Test**: Reload chat UI and verify history for stored conversation_id

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T012 [P] [US2] RED history load test in `frontend/tests/chat-history.test.tsx`
- [x] T013 [P] [US2] RED conversation_id persistence test in `frontend/tests/chat-history.test.tsx`

### Implementation for User Story 2

- [x] T014 [US2] Persist and reuse conversation_id in `frontend/app/chat/page.tsx`
- [x] T015 [US2] Load message history on mount in `frontend/app/chat/page.tsx`
- [x] T016 [US2] Handle missing/invalid history gracefully in `frontend/app/chat/page.tsx`

**Checkpoint**: Refreshing the page preserves conversation and history

---

## Phase 5: User Story 3 - See Tool Call Details (Priority: P3)

**Goal**: Optional debug view for tool calls

**Independent Test**: Expand details toggle and verify tool call metadata

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T017 [P] [US3] RED tool call details toggle test in `frontend/tests/chat-tool-calls.test.tsx`

### Implementation for User Story 3

- [x] T018 [US3] Render tool call details in `frontend/app/chat/page.tsx`
- [x] T019 [US3] Add collapsible toggle UI in `frontend/app/chat/page.tsx`

**Checkpoint**: Tool calls are visible when toggled

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Error/empty states and validation

- [x] T020 [P] Add empty state + error retry UI in `frontend/app/chat/page.tsx`
- [x] T021 [P] Add error/empty state tests in `frontend/tests/chat-page.test.tsx`
- [x] T022 Run quickstart validation in `specs/016-chat-ui-integration/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: Depend on Foundational completion
- **Polish (Phase 6)**: Depends on user stories completion

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational
- **US2 (P2)**: Starts after US1 foundations are in place
- **US3 (P3)**: Starts after US1 foundations are in place

### Parallel Opportunities

- T004 and T005 can run in parallel (different files)
- T007 and T008 can run in parallel (same file, but separate tests)
- T012 and T013 can run in parallel (same file, but separate tests)
- T017 can run in parallel with other test tasks

---

## Parallel Example: User Story 1

```bash
Task: "RED chat send flow test in frontend/tests/chat-page.test.tsx"
Task: "RED loading + optimistic message test in frontend/tests/chat-page.test.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 + Phase 2
2. Complete Phase 3 (US1)
3. Validate chat send + reply behavior

### Incremental Delivery

1. US1: Send + reply
2. US2: Persistence + history
3. US3: Tool call details
4. Polish: Empty/error states + quickstart validation

---

## Notes

- Each test task is RED first, then implementation moves to green.
- Keep UI changes confined to frontend paths.
- Ensure conversation_id persistence uses local storage per spec.
