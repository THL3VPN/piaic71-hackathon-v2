---

description: "Task list template for feature implementation"
---

# Tasks: Floating Chat Widget UX

**Input**: Design documents from `/specs/017-add-chat-widget/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/, quickstart.md

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

**Purpose**: Prepare widget scaffolding and styling hooks

- [x] T001 Create widget shell component in `frontend/app/components/chat-widget.tsx`
- [x] T002 Add widget layout styles in `frontend/app/globals.css`
- [x] T003 [P] Add widget UI helpers in `frontend/lib/chatWidget.ts`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared chat panel rendering for page + widget

- [x] T004 Extract chat panel UI into `frontend/app/components/chat-panel.tsx`
- [x] T005 [P] Render chat panel from `/chat` page in `frontend/app/chat/page.tsx`
- [x] T006 [P] Mount widget container and remove chat link in `frontend/app/tasks/page.tsx`

**Checkpoint**: Chat panel is reusable and widget container is ready

---

## Phase 3: User Story 1 - Open Floating Chat and Send a Message (Priority: P1) 🎯 MVP

**Goal**: Authenticated users can open the widget and send a message

**Independent Test**: Open widget from tasks page, send a message, see reply with loading indicator

### Tests for User Story 1 (MANDATORY, write first) ⚠️

- [x] T007 [P] [US1] RED open/close widget test in `frontend/tests/chat-widget.test.tsx`
- [x] T008 [P] [US1] RED send + loading indicator test in `frontend/tests/chat-widget.test.tsx`

### Implementation for User Story 1

- [x] T009 [US1] Implement launcher + panel toggle in `frontend/app/components/chat-widget.tsx`
- [x] T010 [US1] Wire send flow and loading state in `frontend/app/components/chat-panel.tsx`
- [x] T011 [US1] Integrate widget into tasks page in `frontend/app/tasks/page.tsx`

**Checkpoint**: Widget opens, sends messages, and renders replies

---

## Phase 4: User Story 2 - Resume Conversation After Refresh (Priority: P2)

**Goal**: Conversation continuity across refresh and reopen

**Independent Test**: Refresh the page and verify history loads for stored conversation

### Tests for User Story 2 (MANDATORY, write first) ⚠️

- [x] T012 [P] [US2] RED history load on open test in `frontend/tests/chat-history.test.tsx`
- [x] T013 [P] [US2] RED conversation id persistence test in `frontend/tests/chat-history.test.tsx`

### Implementation for User Story 2

- [x] T014 [US2] Load history on widget open in `frontend/app/components/chat-widget.tsx`
- [x] T015 [US2] Persist conversation id in `frontend/app/components/chat-panel.tsx`
- [x] T016 [US2] Handle missing history gracefully in `frontend/app/components/chat-widget.tsx`

**Checkpoint**: Widget reuses conversation and loads history

---

## Phase 5: User Story 3 - Friendly UX with Errors and Empty State (Priority: P3)

**Goal**: Friendly error, empty, and accessibility behavior

**Independent Test**: Open widget with no messages and trigger a retryable error

### Tests for User Story 3 (MANDATORY, write first) ⚠️

- [x] T017 [P] [US3] RED empty state prompt test in `frontend/tests/chat-widget.test.tsx`
- [x] T018 [P] [US3] RED error + retry test in `frontend/tests/chat-widget.test.tsx`
- [x] T019 [P] [US3] RED focus on open + escape close test in `frontend/tests/chat-widget.test.tsx`
- [x] T020 [P] [US3] RED tool call details toggle test in `frontend/tests/chat-tool-calls.test.tsx`

### Implementation for User Story 3

- [x] T021 [US3] Implement empty/error/retry UI in `frontend/app/components/chat-panel.tsx`
- [x] T022 [US3] Add focus-on-open + escape-to-close in `frontend/app/components/chat-widget.tsx`
- [x] T023 [US3] Add optional tool call details toggle in `frontend/app/components/chat-panel.tsx`

**Checkpoint**: Widget UX meets friendly and accessible requirements

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Auth gating and validation

- [x] T024 [P] Hide/disable widget when unauthenticated in `frontend/app/tasks/page.tsx`
- [ ] T025 [P] Run quickstart validation in `specs/017-add-chat-widget/quickstart.md`

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

- T001, T002, and T003 can run in parallel (different files)
- T007 and T008 can run in parallel (same test file, separate tests)
- T012 and T013 can run in parallel (same test file, separate tests)
- T017–T020 can run in parallel (different tests)

---

## Parallel Example: User Story 1

```bash
Task: "RED open/close widget test in frontend/tests/chat-widget.test.tsx"
Task: "RED send + loading indicator test in frontend/tests/chat-widget.test.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 + Phase 2
2. Complete Phase 3 (US1)
3. Validate widget open + send + reply behavior

### Incremental Delivery

1. US1: Open widget, send message, show reply
2. US2: Persistence + history
3. US3: Friendly UX + accessibility + tool call details
4. Polish: Auth gating + quickstart validation

---

## Notes

- Each test task is RED first, then implementation moves to green.
- Keep UI changes confined to frontend paths.
- Ensure conversation identifier persists using existing storage helpers.
