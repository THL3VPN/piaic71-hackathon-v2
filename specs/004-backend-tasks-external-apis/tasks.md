# Tasks: Task REST API (unauthenticated, DB-backed)

**Input**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/openapi.yaml`  
**Prerequisites**: `plan.md` (required), `spec.md` (user stories with priorities), research/data-model/contracts/quickstart for context  
**Tests**: TDD enforced—each story starts with failing pytest, covering service and HTTP levels; maintain ≥80% coverage.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the HTTP routing surface and mount it so the FastAPI app can delegate do services.

- [X] T001 Create `src/api/tasks.py` with an `APIRouter` stub and imports for SQLModel session dependency (deliverable: new router file).  
- [ ] T002 Register the `tasks` router in `src/main.py` with prefix `/api/tasks` so the FastAPI app exposes the new endpoints (depends on T001).  
- [ ] T003 Document the new API addition in `specs/004-backend-tasks-external-apis/quickstart.md` (deliverable: architecture + curl instructions match router).  

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Ensure consistent error handling and service wiring before writing story-specific endpoints.

- [ ] T004 [P] Write a failing unit test in `tests/unit/test_task_api.py` verifying that fetching a missing task via the service raises `HTTPException(status_code=404, detail="Task not found")` (deliverable: red test demonstrating missing-task handling).  
- [ ] T005 [P] Implement `src/services/task_repo.py` helper (e.g., `async def get_or_404(session, id)`) or router-level guard that raises the shared 404 before story-specific logic runs (depends on T004).  
- [ ] T006 [P] Add shared Pydantic response/validation models if needed (e.g., `TaskRead`, `TaskCreate`, `TaskUpdate`) in `src/models/task.py` or new schema module so routes/clients reuse them (deliverable: clean schema definitions used by multiple stories).  

**Checkpoint**: Foundation done—routes can now rely on consistent error responses and shared schemas.

---

## Phase 3: User Story 1 - Create & list tasks (Priority: P1) 🎯 MVP

**Goal**: Support `POST /api/tasks` and `GET /api/tasks` leveraging service logic so new tasks appear in the list.

**Independent Test**: `tests/integration/test_task_api.py` POSTs and GETs to verify persistence + default fields while the service-level tests ensure title trimming.

### Tests for User Story 1

- [ ] T007 [US1] Write a failing integration test in `tests/integration/test_task_api.py` that POSTs a new task and asserts the subsequent `GET /api/tasks` includes it with `completed=false` and trimmed title (deliverable: red integration test).  
- [ ] T008 [US1] Write a failing unit test in `tests/unit/test_task_service.py` (or a new file) verifying `create_task` trims titles and persists defaults before route implementation (deliverable: red service test).  

### Implementation for User Story 1

- [ ] T009 [US1] Implement POST handler in `src/api/tasks.py` to validate `TaskCreate`, call `task_repo.create_task`, and return 201 with the result (depends on T007/T008).  
- [ ] T010 [US1] Implement GET handler in `src/api/tasks.py` to list tasks ordered by `created_at`/`id`, returning the schema list (depends on T009).  
- [ ] T011 [US1] Refactor service/route wiring to reuse shared schemas and ensure responses are serialized via Pydantic models (deliverable: tidy route/service layer, depends on T009/T010).  

**Checkpoint**: US1 delivers create+list flows usable independently.

---

## Phase 4: User Story 2 - Inspect & update a task (Priority: P2)

**Goal**: Implement `GET /api/tasks/{id}` and `PUT /api/tasks/{id}` while reusing the `task_repo` to validate/return updated records.

**Independent Test**: Unit test ensures `get_task` + update logic works; integration test exercises both endpoints and the 404 path.

### Tests for User Story 2

- [ ] T012 [US2] Write a failing integration test in `tests/integration/test_task_api.py` that fetches a task by ID, updates it with PUT, and expects the returned object to reflect changes (deliverable: red integration test).  
- [ ] T013 [US2] Write a failing unit test in `tests/unit/test_task_service.py` covering `task_repo.update_task` (or similar) to confirm validation rejects blank titles before endpoint code (deliverable: red service test).  

### Implementation for User Story 2

- [ ] T014 [US2] Implement GET by ID handler in `src/api/tasks.py`, using the missing-task guard from T005 to return 404 consistently (depends on T012).  
- [ ] T015 [US2] Implement PUT handler in `src/api/tasks.py` calling a new `task_repo.update_task` method and returning the updated task (depends on T013/T014).  
- [ ] T016 [US2] Add or extend service helper(s) in `src/services/task_repo.py` to handle updates while keeping validation centralized (depends on T015).  

**Checkpoint**: US2 ensures clients can inspect + mutate tasks safely.

---

## Phase 5: User Story 3 - Delete & toggle completion (Priority: P3)

**Goal**: Support `DELETE /api/tasks/{id}` and `PATCH /api/tasks/{id}/complete` with consistent success/404 responses.

**Independent Test**: Integration tests confirm deletion removes records and toggle flips `completed` while unit tests validate the service toggles state.

### Tests for User Story 3

- [ ] T017 [US3] Write a failing integration test in `tests/integration/test_task_api.py` that deletes a task and verifies subsequent GET returns 404 (deliverable: red integration test).  
- [ ] T018 [US3] Write a failing integration test (or unit test) confirming PATCH toggles `completed` twice and returns correct JSON (deliverable: red test).  

### Implementation for User Story 3

- [ ] T019 [US3] Implement DELETE handler in `src/api/tasks.py`, leveraging the shared 404 guard and returning 204 (depends on T017).  
- [ ] T020 [US3] Implement PATCH `/complete` handler that calls `task_repo.toggle_complete` and returns the updated task (depends on T018).  
- [ ] T021 [US3] Ensure service helpers handle toggle logic cleanly (deliverable: target method in `task_repo.py`, depends on T020).  

**Checkpoint**: All REST endpoints now functional with consistent error handling.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Cross-story cleanup, docs, and final checks.

- [ ] T022 Update `tests/integration/test_task_api.py` to assert error payload format for 404/422 when invalid data or missing IDs are submitted (deliverable: robust spec).  
- [ ] T023 Run `RUN_DB_TESTS=1 uv run pytest --cov=src --cov-report=term-missing` and record results in `specs/004-backend-tasks-external-apis/quickstart.md` under Tests (depends on earlier story completion).  
- [ ] T024 Review and tidy `src/api/tasks.py` + service helpers for docstrings/type hints, ensuring each new function stays easy to undo (deliverable: cleaned code).  
- [ ] T025 Commit ✅ and push after verifying story checkpoints; note completed tasks in `tasks.md` before final human review (depends on T024).  

---

## Dependencies & Execution Order

1. **Setup (Phase 1)** → provides router wiring and doc updates.  
2. **Foundational (Phase 2)** → ensures error handling + schemas so all stories rely on the same guard.  
3. **User Story 1 (P1)** → create/list endpoints (MVP).  
4. **User Story 2 (P2)** → inspect/update builds on US1 data and guard.  
5. **User Story 3 (P3)** → delete/toggle leverages prior services.  
6. **Polish (Phase 6)** → runs after all stories complete.

## Parallel Opportunities

- Phase 1 tasks are short and can run sequentially but also in parallel if different files.  
- Phase 2 tests/helpers (T004–T006) are independent, so they may run simultaneously.  
- Within each story, writing tests (e.g., T007/T008) can happen in parallel with data modeling updates.  
- Stories themselves can be implemented in parallel once foundation passes, though prioritizing P1 → P2 → P3 keeps feedback short.

## Implementation Strategy

1. **MVP Focus**: Finish Phase 1–3 and validate create/list flow before touching updates/deletions.  
2. **Incremental Delivery**: After US1 passes (POST + GET), add US2 (inspect/update) then US3 (delete/toggle), running each story’s tests to red/green before proceeding.  
3. **Review Points**: Pause after each story to run relevant tests, capture results, and confirm error schema before merging.  
4. **Undo Workflow**: Keep tasks tiny (≤3 minutes) so any failure can be reverted by reverting the last commit or skipping the next task.
