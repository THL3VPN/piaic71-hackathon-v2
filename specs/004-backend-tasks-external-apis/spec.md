# Feature Specification: Task REST API (unauthenticated, DB-backed)

**Feature Branch**: `004-backend-tasks-external-apis`  
**Created**: 2025-12-14  
**Status**: Draft  
**Input**: User description: "Feature: Task REST API (unauthenticated, DB-backed) User journeys 1.1 Create a task via API 1.2 View all tasks via API 1.3 Update a task via API 1.4 Delete a task via API 1.5 Toggle a task complete/incomplete via API Acceptance criteria 2.1 Backend exposes REST endpoints under /api/tasks 2.2 Endpoints implemented: 2.2.1 GET /api/tasks returns list of tasks 2.2.2 POST /api/tasks creates a task and returns it (201 or 200) 2.2.3 GET /api/tasks/{id} returns task details or 404 2.2.4 PUT /api/tasks/{id} updates title/description and returns updated task or 404 2.2.5 DELETE /api/tasks/{id} deletes task and returns success or 404 2.2.6 PATCH /api/tasks/{id}/complete toggles completion and returns updated task or 404 2.3 Validation rules: 2.3.1 Title is required and non-empty on create/update 2.3.2 Invalid payload returns 422 2.4 Errors are consistent: missing task returns 404 with a clear message 2.5 Uses SQLModel session dependency injection (clean separation: routes call service layer) Success metrics 3.1 All pytest API tests pass (create/list/get/update/delete/toggle) 3.2 Coverage ≥80% for backend code touched in this step 3.3 Manual verification works via curl for at least: 3.3.1 POST /api/tasks then GET /api/tasks shows the created task"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create & discover tasks (Priority: P1)

Clients create a task through `POST /api/tasks` and immediately list it via `GET /api/tasks` so the REST surface proves write/read parity.

**Why this priority**: Without the ability to create and list tasks, the API cannot demonstrate value—this slice delivers the baseline REST contract.

**Independent Test**: Send a POST with a valid title/description, then `GET /api/tasks` to assert the created task appears in the list with defaults (completed=false, trimmed title).

**Acceptance Scenarios**:

1. **Given** the store is empty, **When** the client posts `{ "title": "foo", "description": "bar" }`, **Then** the API replies 201 with the task and `GET /api/tasks` contains that record.
2. **Given** multiple tasks exist, **When** the client calls `GET /api/tasks`, **Then** the API returns them sorted by `created_at` plus `id` for deterministic ordering.

---

### User Story 2 - Inspect and update a task (Priority: P2)

Consumers fetch a specific task via `GET /api/tasks/{id}` and update the `title`/`description` via `PUT`, relying on SQLModel sessions injected into routes so logic stays in the task service.

**Why this priority**: Viewing and editing a single task keeps the interface useful for clients that need to correct or re-read task details.

**Independent Test**: Create a task, retrieve it by ID, then submit a valid PUT that changes the title and description; assert both API responses are 200 and subsequent GET returns the updated values.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the client requests `GET /api/tasks/{id}`, **Then** the API returns 200 with the stored record.
2. **Given** a task exists, **When** the client submits `PUT /api/tasks/{id}` with a new title, **Then** the response shows the updated fields and the stored task reflects the change.

---

### User Story 3 - Delete and toggle completion (Priority: P3)

The API supports `DELETE /api/tasks/{id}` and `PATCH /api/tasks/{id}/complete` so clients can retire tasks or flip completion status without authentication.

**Why this priority**: Full lifecycle management (remove/toggle) makes the task collection manageable; these flows rely on the foundational CRUD support.

**Independent Test**: Create a task, call the delete endpoint and ensure fetching it yields 404, then create another task and toggle completion twice verifying the updated `completed` flag.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the client issues `DELETE /api/tasks/{id}`, **Then** the API responds with 204 (or 200) and the record can no longer be fetched.
2. **Given** a task exists, **When** the client sends `PATCH /api/tasks/{id}/complete`, **Then** the API returns 200 with the toggled `completed` boolean and the persisted record reflects the change.

---

### Edge Cases

- What happens when the client omits `title` or submits whitespace? The request should return 422 with a validation payload describing the missing field.
- How does the API respond when the target ID does not exist? Every route that accepts `{id}` must return 404 with `{ "detail": "Task not found" }` so clients can reliably handle missing resources.
- How are invalid JSON payloads handled? The framework returns 422 before hitting business logic, keeping the service layer focused on valid data.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The service MUST expose REST endpoints under `/api/tasks` for GET (list), POST (create), GET/{id}, PUT/{id}, DELETE/{id}, and PATCH/{id}/complete.
- **FR-002**: POST and PUT payloads MUST include a non-empty `title`; descriptions remain optional and `title` MUST be trimmed before persisting.
- **FR-003**: All ID-bound endpoints (GET/PUT/DELETE/PATCH) MUST return 404 with `{ "detail": "Task not found" }` when the record is absent.
- **FR-004**: Routes MUST rely on the shared SQLModel session dependency so service-layer helpers own validation and persistence rather than putting SQL logic in handlers.
- **FR-005**: Each exposed route MUST be accompanied by TDD-style pytest coverage before implementation, and backend modules touched in this feature MUST stay ≥80% covered.

### Key Entities *(include if feature involves data)*

- **Task**: Represents a DB record with `id`, `title`, `description`, `completed`, and `created_at`. Title is required and trimmed, `description` optional, `completed` defaults to false, and `created_at` captures UTC creation time.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: API tests for create/list/get/update/delete/toggle pass consistently when `RUN_DB_TESTS=1` and `DATABASE_URL` point to Neon.
- **SC-002**: Coverage for the routes, services, and models touched in this feature stays at or above 80% after the new tests run.
- **SC-003**: Manual curl verification (`POST /api/tasks` followed by `GET /api/tasks`) surfaces the newly created record in the list response.
- **SC-004**: Successful requests respond with 200/201/204 and client errors respond with 404/422 while returning JSON bodies that allow downstream clients to handle errors uniformly.
