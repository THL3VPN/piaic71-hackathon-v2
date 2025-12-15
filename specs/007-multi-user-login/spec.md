# Feature Specification: Username/Password Auth with User-Scoped Tasks

**Feature Branch**: `007-multi-user-login`  
**Created**: 2025-12-15  
**Status**: Draft  
**Input**: User description: "Feature: Username/password authentication with user-scoped tasks (multi-user) User journeys 1.1 User opens the application and sees a combined Login/Register landing page 1.2 New user registers with a username and password 1.3 Existing user logs in with username and password 1.4 Logged-in user can add and view only their own tasks 1.5 Logged-in user logs out and returns to the landing page Acceptance criteria 2.1 The application landing page (/) is a Login/Register page 2.2 Registration flow 2.2.1 User can register with username and password 2.2.2 Username is unique; duplicates return a clear error 2.2.3 Passwords are never stored in plaintext (secure hash) 2.3 Login flow 2.3.1 User can log in with username and password 2.3.2 Invalid credentials return a clear error 2.3.3 Successful login returns an authentication token (JWT) to the frontend 2.4 Auth enforcement 2.4.1 All task endpoints require a valid JWT (Authorization: Bearer <token>) 2.4.2 Missing/invalid token returns 401 Unauthorized 2.5 User-scoped task isolation 2.5.1 Each task is owned by exactly one user (user_id stored on the task) 2.5.2 Backend derives the user identity from the JWT (not from client input) 2.5.3 GET returns only tasks owned by the authenticated user 2.5.4 Create automatically assigns ownership to the authenticated user 2.5.5 Update/Delete/Toggle only work for tasks owned by the authenticated user 2.5.6 Cross-user access attempts return 403 Forbidden (or 404 within scope, but consistent) 2.6 Frontend behavior after login 2.6.1 User is redirected to tasks page (e.g., /tasks) 2.6.2 UI shows task list and add task form 2.6.3 All API requests attach the JWT token 2.6.4 Logout clears token/session and returns to / 2.7 Persistence 2.7.1 Users and tasks are stored in Neon PostgreSQL (SQLModel) 2.8 Testing 2.8.1 pytest covers registration, login, invalid login, and protected endpoints 2.8.2 pytest covers task isolation (User A cannot access User B’s tasks) 2.9 Code quality 2.9.1 Python 3.12+ type hints and docstrings are used 2.9.2 Core auth + task logic is separated from UI for testability Success metrics 3.1 New user can register, then immediately log in and receive a valid JWT 3.2 Logged-in user can create tasks and see them persist on refresh 3.3 Two different users see isolated task lists (no leakage) 3.4 Requests without JWT return 401; cross-user attempts are blocked (403/404) 3.5 All tests pass and backend coverage remains ≥80%"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Register and log in (Priority: P1)

New or existing users must be able to register and log in with username/password, receiving a JWT for subsequent requests.

**Why this priority**: No auth → no multi-user isolation. This is the gate for every other flow.

**Independent Test**: pytest covers register → login → receive JWT; duplicate username rejected; invalid credentials return clear error.

**Acceptance Scenarios**:

1. **Given** no account for `alice`, **When** she registers with username/password, **Then** the API returns 201 with a success body (no plaintext password stored).
2. **Given** `alice` exists, **When** she logs in with correct password, **Then** the API returns 200 with a JWT token.
3. **Given** wrong password, **When** login is attempted, **Then** the API returns 401 with an error message and no token issued.
4. **Given** duplicate username on registration, **When** submit same username, **Then** the API returns a conflict/clear error.

---

### User Story 2 - User-scoped task CRUD (Priority: P1)

Authenticated users create, list, update, toggle, and delete only their own tasks.

**Why this priority**: Core product value—tasks must be isolated per user to prevent data leakage.

**Independent Test**: pytest creates tasks with user A token and verifies user B cannot read/update/delete them (403/404). Missing/invalid token returns 401.

**Acceptance Scenarios**:

1. **Given** a valid JWT for user A, **When** POST `/api/tasks` with a title, **Then** 201 and task is owned by user A.
2. **Given** tasks for user A and user B, **When** user A GETs `/api/tasks`, **Then** only user A’s tasks are returned.
3. **Given** user A task id, **When** user B tries to update/delete/toggle it, **Then** 403 (or consistent 404) is returned.
4. **Given** no Authorization header, **When** any `/api/tasks` endpoint is called, **Then** 401 Unauthorized is returned.

---

### User Story 3 - Frontend login + redirect + logout (Priority: P2)

Landing page combines Login/Register. After login, the UI routes to `/tasks`, attaches JWT on API calls, and supports logout back to `/`.

**Why this priority**: Provides the user-facing flow to exercise the backend auth and isolation.

**Independent Test**: Frontend test (or manual) registers/logs in, sees tasks page with user’s tasks, can add a task, then logs out and token is cleared.

**Acceptance Scenarios**:

1. **Given** the app at `/`, **When** a user registers or logs in successfully, **Then** they are redirected to `/tasks` and the token is stored for API calls.
2. **Given** a stored token, **When** fetching tasks from the UI, **Then** the JWT is attached and only that user’s tasks render.
3. **Given** a logged-in user, **When** they click logout, **Then** the token clears and they return to the landing page.

---

### Edge Cases

- Duplicate username registration returns clear error without revealing which field failed.
- Invalid or expired JWT returns 401 with consistent JSON error; no partial responses.
- Cross-user task access returns 403 (or consistent 404) without leaking existence of other users’ tasks.
- Missing/blank title on task create/update returns 422 without altering data.
- Logout must clear token even if backend is unreachable (client-side state cleared).
- Passwords are stored only as secure hashes; no plaintext logging or echo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Provide registration endpoint that creates a user with unique username and securely hashed password.
- **FR-002**: Provide login endpoint that validates credentials and returns a signed JWT containing user identity (subject id/username).
- **FR-003**: Enforce `Authorization: Bearer <token>` on all `/api/tasks/*` endpoints; missing/invalid tokens return 401.
- **FR-004**: Persist tasks with an owning `user_id`; listing returns only the authenticated user’s tasks.
- **FR-005**: Task create automatically assigns ownership to the authenticated user; update/delete/toggle reject access to tasks not owned by the caller (403 or consistent 404).
- **FR-006**: Logout flow clears client-side token and returns user to the landing page.
- **FR-007**: Frontend landing page combines Login/Register and redirects authenticated users to `/tasks`.
- **FR-008**: Error responses for auth and authorization are consistent JSON with clear messages (no stack traces).
- **FR-009**: Passwords are never stored or logged in plaintext; only secure hashes are persisted.
- **FR-010**: Database uses Neon PostgreSQL (via `DATABASE_URL`); all code uses Python 3.12+ type hints and docstrings; pytest-driven tests maintain ≥80% coverage.

### Key Entities *(include if feature involves data)*

- **User**: id (PK), username (unique), password_hash, created_at; used to issue JWT subject.
- **Task**: id (PK), title, description, completed, created_at, owner user_id (FK to User); ownership enforces isolation.
- **JWT Claims**: subject (user id), username, issued/expiry; signed with shared secret; used by backend to derive auth context.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Register → login → receive JWT succeeds end-to-end within one manual flow and via pytest for valid credentials.
- **SC-002**: All `/api/tasks` calls without or with bad tokens return 401; cross-user access attempts return 403/consistent 404.
- **SC-003**: User-specific task lists show only the owner’s tasks; two different users see isolated lists in manual and automated tests.
- **SC-004**: Test suite passes with backend coverage ≥80% and includes registration, login, invalid login, and task isolation cases.
- **SC-005**: Frontend login/register landing page redirects to `/tasks` after success; logout returns to `/` and clears token; API calls include JWT.
