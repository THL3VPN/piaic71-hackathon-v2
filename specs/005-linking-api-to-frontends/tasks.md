# Tasks: Frontend tasks UI (unauthenticated, DB-backed)

**Input**: spec.md, plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml  
**Prerequisites**: Next.js App Router frontend + existing backend `/api/tasks` endpoints  
**Tests**: TDD enforced – each user story starts with failing Vitest tests (RED) before implementation (GREEN) followed by REFACTOR cleanup; maintain ≥80% overall coverage.

## Phase 1: Setup (project scaffolding)

**Purpose**: Bootstrap the `/tasks` route, shared helpers, and documentation for the new UI.

- [X] T001 Create `frontend/app/tasks/page.tsx` with layout placeholders (deliverable: empty tasks route)  
- [X] T002 Create `frontend/lib/tasks.ts` helper for GET/POST and `frontend/lib/types.ts` with `Task` interface (deliverable: typed fetch helper)  
- [X] T003 Verify quickstart/plan highlight the new route and contracts (deliverable: updated quickstart & spec references)  

## Phase 2: Foundational (contracts + docs)

**Purpose**: Document API expectations and add contract-based tests before story work.

- [X] T004 [P] Add OpenAPI specs for `/api/tasks` (GET/POST) and align front-end expectations (deliverable: `specs/005-linking-api-to-frontends/contracts/openapi.yaml`)  
- [X] T005 [P] Document the new tasks UI workflow in quickstart/plan (deliverable: README/quickstart additions)  

## Phase 3: User Story 1 – View tasks (Priority: P1)

**Goal**: Fetch `/api/tasks` and render the list with title/completion/optional description in a responsive card stack.  
**Independent Test**: Vitest test ensures GET is called and the DOM renders each task entry before implementation.

- [X] T006 [P] [US1] RED: Vitest test `frontend/tests/tasks-page.test.tsx` expects mocking GET `/api/tasks` and verifying titles/status present (deliverable: failing test).  
- [X] T007 [US1] GREEN: Implement `frontend/app/tasks/page.tsx` to fetch tasks via `frontend/lib/tasks.ts`, render cards with title/status/description, handle loading state, and keep layout responsive (deliverable: populated list).
- [X] T008 [US1] REFACTOR: Extract shared UI bits (status badge, grid responsive styles) and ensure fetch helper returns typed `Task` array (deliverable: cleaned helper + components).

## Phase 4: User Story 2 – Add task form (Priority: P2)

**Goal**: Supply a form with required title that posts to `/api/tasks` and refreshes the list immediately.  
**Independent Test**: Vitest test ensures form validation blocks empty titles and POST occurs on valid submit, with list refresh triggered.

- [X] T009 [P] [US2] RED: Vitest test mocks POST `/api/tasks`, submits the form, and expects list refresh/new entry text or validation error when title blank.
- [X] T010 [US2] GREEN: Build the add-task form in `frontend/app/tasks/page.tsx` with required title validation, POST call, error handling, and optimistic/refetch handling (deliverable: active form).
- [X] T011 [US2] REFACTOR: Separate validation logic and fetch submission helpers into `frontend/lib/tasks.ts` (deliverable: DRY helper with retry/refresh flag).

## Phase 5: User Story 3 – Resilience & polish (Priority: P3)

**Goal**: Show friendly errors when the backend is unreachable and ensure layout stays clean on mobile.  
**Independent Test**: Vitest test simulates failing GET/POST and checks error messages/responsive grid for <480px width.

- [X] T012 [P] [US3] RED: Vitest test mocks fetch rejection and asserts UI shows “Backend unavailable” plus responsive class toggled (deliverable: failing resilience test).
- [X] T013 [US3] GREEN: Update the component to catch errors, show inline alerts, and add CSS utilities for mobile stacking (deliverable: graceful error state + responsive behavior).
- [X] T014 [US3] REFACTOR: Ensure error/validation states use shared state hooks and document fallback behavior in quickstart/research (deliverable: cleanup + doc note).

## Phase 6: Polish & cross-cutting

- [X] T015 Add README/quickstart section describing manual test (create task → refresh) and lint/test commands (`npm run lint`, `npm run test`).
- [X] T016 Run `cd frontend && npm run lint` + `npm run test` after each story group and log results in quickstart.
- [X] T017 After human review, mark completed tasks in this file and prepare commit (deliverable: tasks checklist updated).

## Dependencies & Strategy

1. Phase 1 ensures the route and contract scaffolding exist.  
2. Phase 2 documents/validates the API so UI tests rely on stable expectations.  
3. US1 builds the list view; US2 adds the form (depends on US1 list structure).  
4. US3 adds resilience/responsive polish once GET/POST flows are solid.  
5. Phase 6 finalizes docs/tests and verification before commit.  

**Parallel opportunities**: Phase 1 config tasks + Phase 2 docs/contracts run concurrently. Within each user story, RED/GREEN/REFACTOR follow TDD and can be executed in quick succession; US1, US2, US3 tasks can be grouped after foundational work is ready.  

**MVP scope**: Deliver US1 (view tasks) first; once list renders correctly, incrementally add the form (US2) and resilience (US3).  
