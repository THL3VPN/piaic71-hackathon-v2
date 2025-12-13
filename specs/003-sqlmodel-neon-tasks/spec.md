# Feature Specification: Persistent Task Storage (SQLModel + Neon Postgres)

**Feature Branch**: `003-sqlmodel-neon-tasks`  
**Created**: 2025-12-13  
**Status**: Draft  
**Input**: User description: "Feature: Persistent task storage (SQLModel + Neon Postgres) User journeys 1.1 Start backend with a real database connection 1.2 Create a task in the database 1.3 Fetch a task from the database 1.4 List tasks from the database Acceptance criteria 2.1 Backend uses SQLModel as the ORM 2.2 Database is Neon Serverless PostgreSQL (Postgres connection string via env var, e.g. DATABASE_URL) 2.3 A Task model exists as a SQLModel table with at least: 2.3.1 id (primary key, auto) 2.3.2 title (required, non-empty) 2.3.3 description (optional) 2.3.4 completed (boolean, default false) 2.3.5 created_at (timestamp) 2.4 On app startup, the database connection initializes successfully 2.5 Migrations or table creation approach is defined (simple SQLModel.metadata.create_all is OK for now) 2.6 Core DB operations are implemented in a testable service/repository layer (not inside route handlers) Success metrics 3.1 pytest tests pass for DB operations (create/get/list) 3.2 Coverage ≥80% for backend code touched in this step 3.3 A local run can connect to Neon and perform a real insert + read without errors"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently

  Testing is written first (pytest) to drive implementation; capture expected coverage impact so the 80% project floor is preserved.
-->

### User Story 1 - Start backend with live Neon DB (Priority: P1)

Start the backend while connecting to a Neon Postgres database via `DATABASE_URL`, ensuring tables are created and the app is ready to serve requests.

**Why this priority**: Without a working DB connection and table creation, no other task operations can proceed.

**Independent Test**: Run the service with a valid `DATABASE_URL`; startup succeeds, tables exist, and a simple metadata check confirms connectivity without invoking any CRUD routes.

**Acceptance Scenarios**:

1. **Given** a valid `DATABASE_URL`, **When** the app starts, **Then** the database connection opens and SQLModel metadata is applied without errors.
2. **Given** a missing or invalid `DATABASE_URL`, **When** the app starts, **Then** the failure is surfaced clearly (not silent) and the app does not proceed with an unusable connection.

---

### User Story 2 - Create and fetch a task (Priority: P2)

Create a task with required fields and retrieve it by ID from the database through a service/repository layer.

**Why this priority**: Validates persistence correctness and enables downstream task consumption.

**Independent Test**: Using the service layer only, create a task and fetch it back by ID; verify fields (id auto-generated, title persisted, completed default false, created_at set).

**Acceptance Scenarios**:

1. **Given** a non-empty title, **When** create_task is called, **Then** a new row is persisted with `completed=false` and `created_at` set.
2. **Given** an existing task ID, **When** get_task is called, **Then** the stored task is returned with matching values; **When** a non-existent ID is requested, **Then** a not-found result is returned without raising unhandled errors.

---

### User Story 3 - List tasks (Priority: P3)

List tasks from the database to support client displays and validation of persisted records.

**Why this priority**: Reading multiple tasks is essential for UI/API consumers and verifies query correctness beyond single fetch.

**Independent Test**: Seed multiple tasks via the service layer, call list_tasks, and confirm ordering and field integrity without invoking HTTP routes.

**Acceptance Scenarios**:

1. **Given** several persisted tasks, **When** list_tasks is called, **Then** the returned collection includes all tasks with accurate fields and deterministic ordering (e.g., created_at ascending).
2. **Given** an empty database, **When** list_tasks is called, **Then** an empty list is returned without error.

---

### Edge Cases

- Missing or malformed `DATABASE_URL` should fail fast with a clear error path.
- Network interruption to Neon after startup should surface errors to callers and avoid silent data loss.
- Title that is empty or whitespace-only must be rejected before hitting the database.
- Requesting a task ID that does not exist should return a clean not-found result rather than an exception.
- Concurrent task inserts should still produce unique IDs without collisions.
- Clock skew/timezone: `created_at` stored in UTC to avoid mixed timestamps.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The service MUST read `DATABASE_URL` (Neon Postgres) from environment and open a connection at startup.
- **FR-002**: The Task SQLModel table MUST exist with fields: id (auto PK), title (required, non-empty), description (optional), completed (bool default false), created_at (timestamp).
- **FR-003**: On startup, the service MUST apply metadata/table creation (e.g., `SQLModel.metadata.create_all`) so the schema is available without manual steps.
- **FR-004**: A repository/service layer MUST implement create_task with validation (non-empty title) and return the persisted task.
- **FR-005**: The repository/service MUST implement get_task(id) returning the task or a not-found signal without raising unhandled errors.
- **FR-006**: The repository/service MUST implement list_tasks returning all tasks with deterministic ordering suitable for client display.
- **FR-007**: Database operations MUST be isolated from HTTP route handlers to allow unit/integration testing without HTTP.
- **FR-008**: The system MUST expose clear error messages/logging on connection or operation failures without leaking secrets.

### Key Entities *(include if feature involves data)*

- **Task**: Represents a to-do item persisted in Neon Postgres with fields id, title, description, completed, created_at; supports create, get by id, and list operations via repository/service.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Service startup with a valid `DATABASE_URL` succeeds and creates required tables with no errors.
- **SC-002**: A create-then-fetch round-trip persists and returns a task with correct defaults (completed=false, created_at set).
- **SC-003**: Listing tasks returns all persisted rows in deterministic order and handles empty datasets gracefully.
- **SC-004**: pytest suite for DB operations (create/get/list) passes with ≥80% coverage for backend code touched in this feature.
- **SC-005**: A real Neon connection can perform an insert and subsequent read locally without errors.
