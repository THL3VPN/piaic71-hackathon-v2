# Tasks: Frontend bootstrap with backend connectivity

**Input**: spec.md, plan.md, research.md, data-model.md, quickstart.md, contracts/openapi.yaml  
**Prerequisites**: Next.js App Router frontend in `frontend/`, backend already running in `backend/`  
**Tests**: TDD enforced – each operation starts with failing client or unit test covering the health fetch or proxy config; maintain ≥80% coverage

## Phase 1: Setup (project scaffolding)

**Purpose**: Create the Next.js App Router app that will fetch backend `/health` and document how to run both apps.

- [X] T001 Create `frontend/` directory with `package.json`, `next.config.js`, and App Router entry files (`app/page.tsx`) plus fetch helper (deliverable: scaffolded Next.js app)  
- [X] T002 Add README instructions covering `uv run uvicorn src.main:app --reload --port 8000` and `cd frontend && npm run dev` (deliverable: README section under docs)  
- [X] T003 Write a failing smoke test (e.g., Next lint/build) for the new frontend to confirm the project compiles once dependencies are added (deliverable: red `npm run lint` or `npm run build`)  

## Phase 2: Foundational (health contract + proxy)

**Purpose**: Align API contract and development proxy so the frontend can call `/health` reliably.

- [X] T004 [P] Add `contracts/openapi.yaml` describing GET `/health` so the frontend team understands the response shape (deliverable: contract file)  
- [X] T005 [P] Configure `frontend/next.config.js` rewrites to proxy `/api/health` → backend port 8000 (deliverable: proxy config)  
- [X] T006 [P] Expand README quickstart with proxy/CORS notes and required env var (deliverable: CORS section)  

## Phase 3: User Story 1 – Display backend health (P1)

**Goal**: Fetch `/health` and render result in a labeled card.

**Independent Test**: Start frontend+backend, open homepage, ensure health fetch executes (verified by failing test that expects “Backend: OK” text).

### Tests for US1

- [X] T007 [US1] RED: Write a failing frontend integration/unit test (e.g., jest/next-testing-library) asserting the card calls the fetch helper and renders “Backend: OK” after Promise resolves.  
- [X] T008 [US1] GREEN: Implement `frontend/app/page.tsx` to render a card that fetches `NEXT_PUBLIC_BACKEND_URL` or `/api/health`, displays status or error, and updates state (deliverable: card component).  
- [X] T009 [US1] REFACTOR: Clean up the fetch helper + component to use shared interfaces from `frontend/lib/health.ts`, add TypeScript types for `HealthStatus` (deliverable: typed helper).  

## Phase 4: User Story 2 – Documentation & dev workflow (P2)

**Goal**: Ensure README guides running both apps and tests show the health behavior.

**Independent Test**: Running README commands should start both servers and show `Backend: OK` in the browser.

- [X] T010 [US2] RED: Add a failing doc/test entry ensuring README mentions both backend and frontend commands (deliverable: check script or doc-only test).  
- [X] T011 [US2] GREEN: Expand README to include exact commands/ports and mention `NEXT_PUBLIC_BACKEND_URL`/proxy configuration (deliverable: new README section).  
- [X] T012 [US2] REFACTOR: Verify README describes how to run `npm run lint`/`next build` so future smoke tests have guidance (deliverable: README test commands).  

## Phase 5: User Story 3 – CORS/proxy resilience (P3)

**Goal**: Handle backend failure gracefully and avoid CORS errors.

**Independent Test**: Fail the fetch (simulate backend down) and assert UI still renders error text.

- [X] T013 [US3] RED: Create a frontend test mocking a failed fetch (network error) and expecting “Backend: unavailable” to display.  
- [X] T014 [US3] GREEN: Update the component to catch fetch errors/timeouts and display `message` or fallback text, keeping page interactive.  
- [X] T015 [US3] REFACTOR: Ensure proxy/cross-origin notes live in README and Next config includes both rewrites and env var default (deliverable: polished proxy config).  

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T016 Update quickstart.md with new frontend steps + smoke test results (deliverable: enhanced quickstart).  
- [X] T017 Document decision tradeoffs (research.md updated) and add ADR note if needed (deliverable: recorded decisions).  
- [X] T018 Run frontend smoke test (`cd frontend && npm run lint`/`npm run build`) and record success (deliverable: test log referenced in quickstart).  
- [X] T019 After human review, mark tasks done and prep commit (deliverable: checklist update + plan for commit).  

## Dependencies & Execution Order

1. Phase 1 tasks set up repo scaffolding and README.  
2. Phase 2 ensures proxy/CORS ready before fetching.  
3. US1 requires proxy to exist before fetching health.  
4. US2 documentation builds on US1 components.  
5. US3 error handling depends on fetch logic and proxy work.  
6. Phase 6 wraps up docs/tests before commit.

## Parallel Opportunities

- Parallelize Phase 1 scaffolding and README updates (T001/T002) since they touch different dirs.  
- Tasks T004–T006 about contract/proxy/docs can run together before US1.  
- Within each user story, RED and GREEN tasks follow TDD; REFACTOR tasks (T009/T012/T015) can be parallel once functionality passes.

## Implementation Strategy

1. MVP: render backend health card (US1) once proxy ready.  
2. Incrementally add docs/test support (US2) then error handling (US3).  
3. After each phase verify via Next dev server + README commands before marking tasks.  
4. Keep tasks ≤3 minutes; revert by skipping next step if failure occurs.
