# Tasks: Username/Password Auth with User-Scoped Tasks

## Phase 1: Setup
- [X] T001 Ensure test env vars set for local runs (`BETTER_AUTH_SECRET`, `DATABASE_URL`, `RUN_DB_TESTS`) in .env/.env.example (depends on none; deliverable: validated env docs)
- [X] T002 Add test fixtures for temporary DB and user/token helpers in tests/conftest.py (depends on T001; deliverable: shared fixtures)

## Phase 2: Foundational Auth/Core
- [X] T003 [US1] RED: Add failing unit test for password hashing/verify helpers in tests/unit/test_auth_passwords.py (depends on T002; deliverable: red test)
- [X] T004 [US1] GREEN: Implement password hash/verify helpers in src/services/auth.py (depends on T003; deliverable: passing test)
- [X] T005 [US1] REFACTOR: Clean auth helper naming/type hints/docstrings in src/services/auth.py (depends on T004; deliverable: tidy code)
- [X] T006 [US1] RED: Add failing unit test for User SQLModel (unique username, password_hash stored) in tests/unit/test_user_model.py (depends on T002; deliverable: red test)
- [X] T007 [US1] GREEN: Implement User model and unique index in src/models/user.py, include in metadata (depends on T006; deliverable: model code)
- [X] T008 [US1] REFACTOR: Update db metadata/create_all to include User; adjust type hints (depends on T007; deliverable: create_all covers User)

## Phase 3: Auth Endpoints (Register/Login)
- [X] T009 [US1] RED: Add failing integration tests for register/login (happy + invalid + duplicate) in tests/integration/test_auth_api.py (depends on T008; deliverable: red tests)
- [X] T010 [US1] GREEN: Implement /api/register and /api/login routes with JWT issuance in src/api/auth.py (depends on T009; deliverable: endpoints + passing tests)
- [X] T011 [US1] REFACTOR: Centralize JWT config (secret, exp) and error responses; docstrings (depends on T010; deliverable: tidy auth module)

## Phase 4: Task Ownership Enforcement
- [X] T012 [US2] RED: Add failing integration tests for owned task CRUD (403 on cross-user, 401 missing token, 422 validation) in tests/integration/test_task_api.py (depends on T010; deliverable: expanded tests)
- [X] T013 [US2] GREEN: Extend Task model with owner_id FK and add filtering/ownership checks in task repo/service in src/services/task_repo.py and src/api/tasks.py (depends on T012; deliverable: passing tests)
- [X] T014 [US2] REFACTOR: Clean auth dependency injection/context to supply user id to task routes; update type hints (depends on T013; deliverable: tidy route deps)

## Phase 5: Frontend Auth Flow
- [X] T015 [US3] RED: Add failing frontend test for landing login/register flow and token storage in frontend/tests/auth-page.test.tsx (depends on T010; deliverable: red test)
- [X] T016 [US3] GREEN: Implement landing page (/), combined login/register UI, token persistence, redirect to /tasks in frontend/app/page.tsx + frontend/lib/auth.ts (depends on T015; deliverable: passing test)
- [X] T017 [US3] RED: Add failing frontend test for tasks page fetching with JWT and logout clearing token in frontend/tests/tasks-auth.test.tsx (depends on T016; deliverable: red test)
- [X] T018 [US3] GREEN: Wire tasks page to attach JWT, show user-owned tasks, add logout button that clears token and routes to / (depends on T017; deliverable: passing test)
- [X] T019 [US3] REFACTOR: Styling cleanup and shared fetch helper for auth headers in frontend/lib/* (depends on T018; deliverable: tidy frontend code)

## Phase 6: Polish & Cross-Cutting
- [X] T020 Update quickstart.md with register/login curl + frontend notes (depends on T011; deliverable: updated docs)
- [X] T021 Add ADR capturing auth choices (bcrypt, HS256, 403 policy) in history/adr/ (depends on T011; deliverable: ADR)
- [ ] T022 Run full backend + frontend tests, verify coverage ≥80%, mark tasks done (depends on T019; deliverable: test report)

## Dependencies Overview
- T001 → T002 → T003/T006 → T004/T007 → T005/T008 → T009 → T010 → T012 → T013 → T014 → T020/T021/T022
- Frontend: T010 → T015 → T016 → T017 → T018 → T019

## Parallel Opportunities
- T003 and T006 can run after fixtures (T002) in parallel ([P] not marked to keep sequencing simple).
- Frontend Phase 5 can begin after auth endpoints (T010) while backend ownership work proceeds, if desired.

## Implementation Strategy
- Strict TDD: each operation starts RED test, then GREEN implementation, then REFACTOR cleanup.
- Keep diffs small (≤3-minute tasks), reversible steps, and clear dependencies.
