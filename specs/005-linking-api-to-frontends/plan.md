## Implementation Plan: Frontend tasks UI (unauthenticated, DB-backed)

**Branch**: `005-linking-api-to-frontends` | **Date**: 2025-10-07 | **Spec**: specs/005-linking-api-to-frontends/spec.md  
**Input**: Feature specification from `/specs/005-linking-api-to-frontends/spec.md`

## Summary

Bring the existing backend tasks API (`GET /api/tasks`, `POST /api/tasks`) into the Next.js frontend by rendering a responsive list, adding a client-side form to create tasks, showing validation/errors, and refreshing the list so UI and backend stay in sync with ≥80% coverage enforced via Vitest + pytest.

## Technical Context

**Language/Version**: Backend UV-managed Python 3.12+, Frontend Next.js 18.3 (App Router) with TypeScript  
**Primary Dependencies**: backend already uses UV + pytest; frontend will use Next.js + Vitest/Testing Library + ESLint flat config  
**Storage**: PostgreSQL (Neon) provided by backend service, accessible via existing SQLModel task API  
**Testing**: pytest for backend, Vitest for frontend (run via `npm run test`, follow TDD red/green/refactor)  
**Target Platform**: Linux-based dev machine + browser (desktop/mobile)  
**Project Type**: Web app with separated `backend/` Python API and `frontend/` Next.js UI  
**Performance Goals**: Fast list rendering (single-digit fetch latency) and client-side UI updates; maintain responsive layout on mobile widths  
**Constraints**: Keep coverage ≥80%. Type hints mandatory; dataclasses for structured task data in backend models. TDD workflow requires writing failing tests (Vitest/pytest) before implementing features.  
**Scale/Scope**: UI handles dozens of tasks per fetch; backend API remains unmodified (calls must use current endpoints).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (Vitest) before implementing fetch/list logic; backend pytest suites remain untouched.  
- Python 3.12+ runtime for backend with type hints; frontend uses TypeScript hooks and typed fetch helpers.  
- UV handles backend deps; no new system binaries required.  
- Coverage target ≥80% enforced via Vitest/pytest and linting; critical decisions logged in research/ADR.

## Project Structure

### Documentation (this feature)

```text
specs/005-linking-api-to-frontends/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # OpenAPI contract for GET/POST tasks
└── tasks.md             # Phase 2 output (will be created via /sp.tasks)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── layout.tsx
│   └── page.tsx                     # Tasks list + create form
├── lib/
│   └── tasks.ts                     # Fetch helper(s) + types
├── tests/
│   └── page.test.tsx                # Vitest + Testing Library tests\n+├── vitest.config.ts
│   └── vitest.setup.ts
├── eslint.config.mjs
├── next.config.js
├── package.json
└── tsconfig.json
backend/
└── [unchanged; reuse existing SQLModel task APIs under /api/tasks]
```

**Structure Decision**: Reuse the current backend API and extend the Next.js App Router frontend so the UI sits inside `frontend/` (with tests inside `frontend/tests`). The backend tree remains unchanged because existing endpoints already satisfy requirements.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|---------------------------------------|
| None | N/A | N/A |
