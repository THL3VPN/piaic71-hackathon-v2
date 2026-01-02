# Tasks: Chat Widget Polish

**Input**: Design documents from `/specs/018-chat-widget-polish/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Frontend tests are required; add/update Vitest + Testing Library tests first where UI behavior changes.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and base UI styling tooling

- [x] T001 Validate Tailwind CSS adoption decision and record ADR in specs/018-chat-widget-polish/contracts/adr-tailwind.md
- [x] T002 Add Tailwind CSS to frontend build tooling (config + globals) in frontend/ and frontend/app/globals.css
- [x] T003 [P] Add baseline Tailwind utility classes for chat widget container in frontend/app/components/chat-widget.tsx

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core UI scaffolding that must be stable before story work

- [x] T004 Update chat widget layout wrappers for overflow control in frontend/app/components/chat-panel.tsx
- [x] T005 [P] Add shared typography scale utilities for widget header and bubbles in frontend/app/components/chat-panel.tsx

---

## Phase 3: User Story 1 - Clean Chat Widget Experience (Priority: P1) 🎯 MVP

**Goal**: Clean, ChatGPT-style layout with no horizontal scroll and clear message alignment.

**Independent Test**: Open widget, send message, verify layout fits viewport with no horizontal scroll and wrapped messages.

### Tests for User Story 1 (write first)

- [x] T006 [P] [US1] Add UI layout tests for no horizontal scroll and bubble alignment in frontend/tests/chat-widget.test.tsx

### Implementation for User Story 1

- [x] T007 [US1] Refine widget container sizing, padding, and scroll behavior in frontend/app/components/chat-widget.tsx
- [x] T008 [US1] Style message bubbles (alignment, spacing, wrap) in frontend/app/components/chat-panel.tsx
- [x] T009 [US1] Ensure tool call details wrap and do not overflow in frontend/app/components/chat-panel.tsx

---

## Phase 4: User Story 2 - Always-Visible Composer (Priority: P2)

**Goal**: Composer stays fixed, send button is circular, Enter submits message.

**Independent Test**: Scroll messages and verify input row stays visible; Enter and click send work.

### Tests for User Story 2 (write first)

- [x] T010 [P] [US2] Add composer visibility and send button tests in frontend/tests/chat-widget.test.tsx

### Implementation for User Story 2

- [x] T011 [US2] Make composer sticky/fixed within panel and keep input visible in frontend/app/components/chat-panel.tsx
- [x] T012 [US2] Replace send button styling with circular icon button in frontend/app/components/chat-panel.tsx
- [x] T013 [US2] Ensure Enter submits and does not break input layout in frontend/app/components/chat-panel.tsx

---

## Phase 5: User Story 3 - Concise Assistant Replies (Priority: P3)

**Goal**: UI reflects concise responses without altering content or backend logic.

**Independent Test**: Send simple prompts and confirm responses render compactly without extra UI verbosity.

### Tests for User Story 3 (write first)

- [x] T014 [P] [US3] Add UI test to verify concise rendering (no extra UI verbosity) in frontend/tests/chat-widget.test.tsx

### Implementation for User Story 3

- [x] T015 [US3] Reduce UI chrome around responses (spacing and labels) in frontend/app/components/chat-panel.tsx
- [x] T016 [US3] Ensure header/title hierarchy remains consistent and minimal in frontend/app/components/chat-widget.tsx

---

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T017 [P] Accessibility pass: focus states and button contrast in frontend/app/components/chat-panel.tsx
- [x] T018 Update quickstart validation steps if needed in specs/018-chat-widget-polish/quickstart.md
- [x] T019 Run frontend test suite and ensure no regressions: frontend (npm test)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on user stories complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts after Foundational (Phase 2)
- **User Story 2 (P2)**: Starts after Foundational (Phase 2)
- **User Story 3 (P3)**: Starts after Foundational (Phase 2)

### Parallel Opportunities

- T002 and T003 can run in parallel after T001.
- Test tasks (T006, T010, T014) can run in parallel within their story.

---

## Parallel Example: User Story 1

```bash
Task: "Add UI layout tests for no horizontal scroll and bubble alignment in frontend/tests/chat-widget.test.tsx"
Task: "Refine widget container sizing, padding, and scroll behavior in frontend/app/components/chat-widget.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate layout and scrolling behavior

### Incremental Delivery

1. Add User Story 2 (composer UX) and validate
2. Add User Story 3 (concise rendering) and validate
3. Run full frontend test suite
