# Tasks: Secure API requests with JWT verification (006-jwt-auth)

**Input**: Spec/plan outlines for JWT auth protections
**Tests**: pytest-first for every story (fail before implementing)

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Add `BETTER_AUTH_SECRET=` entry to `.env.example` so newcomers know the secret is required for auth-protected APIs (depends on nothing)
- [x] T002 Update `README.md` to describe the new JWT guard, link to the quickstart token, and mention how to set `BETTER_AUTH_SECRET` locally (depends on T001)

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T003 Create `src/services/auth.py` with the `AuthenticatedContext` dataclass plus helpers to load `BETTER_AUTH_SECRET` and raise a uniform `401` response (depends on T002)
- [x] T004 Extend `src/services/auth.py` with reusable auth errors (detail payloads + logging) so future middleware emits consistent JSON for missing/invalid tokens (depends on T003)

## Phase 3: User Story 1 - Enforce header presence (Priority: P1)

**Goal**: Ensure `/api/*` refuses requests missing or misformatted the `Authorization: Bearer <token>` header.
**Independent Test**: pytest hitting `/api/tasks` without/with bad header returns `401` before DB access.

### Tests (TDD first)
- [x] T005 [US1] Write `tests/unit/test_auth_middleware.py` test that calls `/api/tasks` without `Authorization` and asserts on `401` + error granularity (starts red) (depends on Phase 2)
- [x] T006 [US1] Extend `tests/unit/test_auth_middleware.py` with a second test where `Authorization` uses `Token` instead of `Bearer` and still expects `401` (depends on T005)

### Implementation
- [x] T007 [US1] Implement HTTP middleware in `src/services/auth.py` to parse the header, reject missing/prefix errors, and raise the canonical auth error (depends on T006)
- [x] T008 [US1] Wire the middleware into `src/main.py` so every `/api/` request passes through it before reaching route logic (depends on T007)

## Phase 4: User Story 2 - Verify JWT signature & identity (Priority: P2)

**Goal**: Validate tokens against `BETTER_AUTH_SECRET` and expose the decoded `user_id` (or `sub`) via `request.state.auth` so handlers can trust the caller.
**Independent Test**: Pytest supplies signed and tampered tokens and inspects the resulting status/context.

### Tests (TDD first)
- [x] T009 [US2] Add test in `tests/unit/test_auth_middleware.py` that submits `/api/tasks` with an HS256 token signed with the wrong secret and asserts `401` (depends on T008)
- [x] T010 [US2] Add a test that submits a valid token (signed with `BETTER_AUTH_SECRET`) and expects `200` plus a signal that `user_id` is available (depends on T009)

### Implementation
- [x] T011 [US2] Extend `src/services/auth.py` with JWT decoding (via PyJWT/`python-jose`), verify expiry/signature, and attach `AuthenticatedContext` to `request.state` (depends on T010)
- [x] T012 [US2] Update `src/api/tasks.py` endpoints to depend on a new FastAPI dependency that reads `request.state.auth` (same file, adds `auth_context: AuthenticatedContext = Depends(auth.get_authenticated_context)`) so handlers can access `user_id` without direct JWT parsing (depends on T011)

## Phase 5: User Story 3 - Manual test token (Priority: P3)

**Goal**: Provide devs with a reproducible JWT + documentation so they can manually verify the protected endpoints.
**Independent Test**: `curl`/HTTPie commands with the sample token succeed; substituting garbage fails.

- [x] T013 [US3] Replace the placeholder in `specs/006-jwt-auth/quickstart.md` with a real JWT signed with `BETTER_AUTH_SECRET`, show the curl commands, and mention how to regenerate if needed (depends on T012)
- [x] T014 [US3] Add a short note in `README.md` (or a dedicated section) describing how to use that token for manual verification, including the expected `401`/`200` outcomes (depends on T013)

## Phase 6: Polish & Cross-Cutting Concerns

- [x] T015 Update `tests/integration/test_task_crud.py` to include the valid JWT header so the auth guard no longer breaks the existing task integration flow (depends on T012)
- [x] T016 Run `BETTER_AUTH_SECRET=secret uv run pytest --cov=src` locally and capture the command/result in quickstart/README to show the auth tests are green (manual verification - no file change but log the step in quickstart) (depends on T015)
- [x] T017 Confirm the new auth middleware is documented in an ADR or `docs/` file referencing the shared secret decision (depends on T016)

## Dependencies & Execution Order

- Phase 1 → Phase 2 → User Story phases → Polish
- Tests (US1/US2) must fail before their implementation tasks (T005/T006 before T007, T009/T010 before T011)
- Phase 2 is a prerequisite for all user stories; no story work until T004 is complete
- US2 (T009-T012) depends on US1 middleware being wired first
- Polish tasks happen after user stories finish to avoid regressions
