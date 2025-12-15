---
id: 0001
title: username-password-task-auth
stage: spec
date: 2025-12-15
surface: cli
model: gpt-4.1
feature: 007-multi-user-login
branch: 007-multi-user-login
user: user
command: .specify/scripts/bash/create-new-feature.sh ... (spec authoring)
labels: [spec]
links:
  spec: specs/007-multi-user-login/spec.md
  ticket: ""
  adr: ""
  pr: ""
files:
  - specs/007-multi-user-login/spec.md
  - specs/007-multi-user-login/checklists/requirements.md
tests:
  - command: ""
    result: not-run
    coverage: ""
---

## Prompt

Feature: Username/password authentication with user-scoped tasks (multi-user) User journeys 1.1 User opens the application and sees a combined Login/Register landing page 1.2 New user registers with a username and password 1.3 Existing user logs in with username and password 1.4 Logged-in user can add and view only their own tasks 1.5 Logged-in user logs out and returns to the landing page Acceptance criteria 2.1 The application landing page (/) is a Login/Register page 2.2 Registration flow 2.2.1 User can register with username and password 2.2.2 Username is unique; duplicates return a clear error 2.2.3 Passwords are never stored in plaintext (secure hash) 2.3 Login flow 2.3.1 User can log in with username and password 2.3.2 Invalid credentials return a clear error 2.3.3 Successful login returns an authentication token (JWT) to the frontend 2.4 Auth enforcement 2.4.1 All task endpoints require a valid JWT (Authorization: Bearer <token>) 2.4.2 Missing/invalid token returns 401 Unauthorized 2.5 User-scoped task isolation 2.5.1 Each task is owned by exactly one user (user_id stored on the task) 2.5.2 Backend derives the user identity from the JWT (not from client input) 2.5.3 GET returns only tasks owned by the authenticated user 2.5.4 Create automatically assigns ownership to the authenticated user 2.5.5 Update/Delete/Toggle only work for tasks owned by the authenticated user 2.5.6 Cross-user access attempts return 403 Forbidden (or 404 within scope, but consistent) 2.6 Frontend behavior after login 2.6.1 User is redirected to tasks page (e.g., /tasks) 2.6.2 UI shows task list and add task form 2.6.3 All API requests attach the JWT token 2.6.4 Logout clears token/session and returns to / 2.7 Persistence 2.7.1 Users and tasks are stored in Neon PostgreSQL (SQLModel) 2.8 Testing 2.8.1 pytest covers registration, login, invalid login, and protected endpoints 2.8.2 pytest covers task isolation (User A cannot access User B’s tasks) 2.9 Code quality 2.9.1 Python 3.12+ type hints and docstrings are used 2.9.2 Core auth + task logic is separated from UI for testability Success metrics 3.1 New user can register, then immediately log in and receive a valid JWT 3.2 Logged-in user can create tasks and see them persist on refresh 3.3 Two different users see isolated task lists (no leakage) 3.4 Requests without JWT return 401; cross-user attempts are blocked (403/404) 3.5 All tests pass and backend coverage remains ≥80%

## Response snapshot

Generated spec for `007-multi-user-login`: prioritized user stories (register/login JWT, user-scoped task CRUD, frontend login/redirect/logout), edge cases, functional requirements, entities, and measurable success criteria; added quality checklist with all items passing.

## Outcome

- ✅ Impact: Spec authored and checklist completed for multi-user username/password auth with task isolation.
- 🧪 Tests: Not run at spec stage.
- 📁 Files: Updated spec.md; added requirements checklist.
- 🔁 Next prompts: Proceed to planning/clarify or implementation per workflow.
- 🧠 Reflection: Kept ≤3 stories, clear auth/isolation requirements, no open clarifications.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not run
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
