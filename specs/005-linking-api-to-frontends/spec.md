# Feature Specification: Frontend tasks UI (unauthenticated, DB-backed)

**Feature Branch**: `005-linking-api-to-frontends`  
**Created**: 2025-10-07  
**Status**: Draft  
**Input**: User description: "Feature: Frontend tasks UI (unauthenticated, DB-backed) User journeys 1.1 Open the web app and view all tasks 1.2 Add a new task from the UI 1.3 See the list update after adding Acceptance criteria 2.1 The homepage (or /tasks) fetches tasks from the backend 2.2 Backend integration uses your existing API: 2.2.1 GET /api/tasks to list tasks 2.2.2 POST /api/tasks to create a task 2.3 UI shows tasks clearly: 2.3.1 title 2.3.2 completion status 2.3.3 optional description (if present) 2.4 UI provides a simple “Add Task” form (title required) 2.5 Validation: empty title shows a user-friendly error and does not submit 2.6 After creating a task, the list refreshes (optimistic update or refetch) 2.7 No authentication is required 2.8 Responsive layout works on mobile and desktop Success metrics 3.1 Manual test: create a task in UI → it appears immediately and persists on refresh 3.2 No console errors during fetch/create 3.3 Backend tests remain green (no regressions)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View existing tasks (Priority: P1)

Users open the homepage (or `/tasks`) and immediately see the list of tasks returned from the backend so they can verify the current backlog.

**Why this priority**: Showing the data is the core value driver; without it the UI is just a form.

**Independent Test**: Verify GET `/api/tasks` is called during page render in a failing Vitest or integration test and the UI renders titles + status pairs.

**Acceptance Scenarios**:

1. **Given** the backend has stored tasks, **When** the frontend loads, **Then** the task list shows each title, completion status badge, and (if available) description.
2. **Given** the backend returns nothing, **When** the frontend loads, **Then** a friendly empty state appears so users know there are no tasks yet.

---

### User Story 2 - Add tasks through UI (Priority: P2)

Users type a title into the “Add Task” form, optionally add a description, submit, and instantly see the new task appear without a full page reload.

**Why this priority**: Creation flow unlocks the interactive experience promised in the spec; it relies on the list view but focuses on mutation.

**Independent Test**: Start with a red test that posts to `/api/tasks` via mocked fetch and asserts the list refreshes; then implement the form.

**Acceptance Scenarios**:

1. **Given** a valid title (and optional description), **When** the user saves, **Then** POST `/api/tasks` runs, the new task appears, and the input resets.
2. **Given** the title is blank, **When** the form submits, **Then** show a validation message, do not call POST, and keep the modal/form open.

---

### User Story 3 - Responsive and resilient layout (Priority: P3)

Users on desktop or mobile see a layout that stacks gracefully, and the page surfaces errors when the backend is unreachable.

**Why this priority**: Responsiveness ensures the feature looks production-ready; error handling protects the UI from network failures.

**Independent Test**: Mock failure on GET `/api/tasks` and assert the fallback message renders while preserving layout structure.

**Acceptance Scenarios**:

1. **Given** the API request fails, **When** the page loads, **Then** show “Backend unavailable” plus error details while keeping the layout intact.
2. **Given** the viewport is narrow, **When** the page renders, **Then** the cards/ form stack vertically without overflow.

---

### Edge Cases

- What happens when the backend returns malformed data (missing title)? Validate and skip rendering that entry with a warning.
- How does the UI behave if POST `/api/tasks` rejects or times out? Show the user-friendly error plus keep form inputs so they can retry.
- Does the layout degrade if the task list is very long? Ensure the container scrolls rather than forcing horizontal overflow.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST call GET `/api/tasks` via the existing backend API when the homepage renders and present each task with title, completion status, and optional description.
- **FR-002**: System MUST offer an “Add Task” form with a required title field and optional description, preventing submissions without a title.
- **FR-003**: System MUST POST new tasks to `/api/tasks`, refresh the list (optimistically or via refetch), and preserve user input when backend errors occur.
- **FR-004**: System MUST display clear validation cues and error summaries when fetch/create operations fail, keeping the rest of the layout interactive.
- **FR-005**: System MUST behave responsively on desktop and mobile (e.g., stacked cards, mobile-friendly typography) while keeping the frontend in sync with backend tests.

### Key Entities *(include if feature involves data)*

- **Task**: Represents a to-do item with attributes `id`, `title`, `description?`, `completed`, `created_at`; interacts with backend GET/POST endpoints.
- **TaskListState**: Client-side representation of the fetched tasks, plus `loading`, `error`, and `validation` flags used for UI feedback.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Manual test (browser) demonstrates creating a task via the UI results in the new row appearing immediately and surviving a page refresh.
- **SC-002**: Vitest/Testing Library suite covers happy/sad flows for GET and POST requests; lint/test script pair run without console errors.
- **SC-003**: Backend API tests (`pytest`) remain successful after frontend integration (no regressions triggered by new fetch clients).
- **SC-004**: Layout renders without horizontal overflow on a 320px viewport and gracefully stacks inputs/cards.
