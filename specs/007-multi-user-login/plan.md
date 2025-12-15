# Implementation Plan: Username/Password Auth with User-Scoped Tasks

**Branch**: `007-multi-user-login` | **Date**: 2025-12-15 | **Spec**: specs/007-multi-user-login/spec.md
**Input**: Feature specification from `/specs/007-multi-user-login/spec.md`

## Summary

Deliver username/password auth with JWT issuance, enforced on all task endpoints, and user-owned tasks scoped per authenticated user. Backend: FastAPI + SQLModel on PostgreSQL (Neon via `DATABASE_URL`), password hashing (bcrypt), JWT signing with shared secret. Frontend: login/register landing at `/`, store JWT, route to `/tasks`, and attach token to API calls. TDD with pytest (unit + integration), maintain ≥80% coverage.

## Technical Context

**Language/Version**: Python 3.13 (per repo) with type hints everywhere.  
**Primary Dependencies**: FastAPI, SQLModel + psycopg (Neon), passlib[bcrypt] for password hashing, jose/pyjwt for JWT, anyio/pytest for async tests.  
**Storage**: Neon PostgreSQL via `DATABASE_URL`; tasks and users in SQLModel.  
**Testing**: pytest (unit + integration), TDD red/green, coverage ≥80%.  
**Target Platform**: Linux host, uv-managed virtualenv.  
**Project Type**: Web app with backend API + Next.js frontend.  
**Performance Goals**: Low latency CRUD; no heavy perf targets (NEEDS CLARIFICATION if required).  
**Constraints**: TDD required; dataclasses/SOLID for domain; ADR for major auth/storage decisions; maintain JWT compatibility with existing Better Auth flows.  
**Scale/Scope**: Multi-user tasks; expected small user count initially (NEEDS CLARIFICATION for scale).

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan documents how TDD will be performed.
- Python 3.12+ with type hints everywhere; dataclasses are the default for structured data.
- UV is the package/environment manager; note any required system dependencies.
- Quality bars: all planned changes must maintain ≥80% coverage; add ADR references for any significant design choices.
- Plan passes gates: TDD, type hints, uv, coverage ≥80%, ADR for auth model and hashing/JWT decisions.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend (monorepo root)
├── src/
│   ├── api/          # FastAPI routes (health, tasks, auth to add)
│   ├── models/       # SQLModel entities: Task, User
│   ├── services/     # auth (hash/JWT), db, task_repo, user_repo
│   └── cli/          # existing CLI app (unchanged)
├── tests/
│   ├── unit/
│   └── integration/

frontend/
├── app/              # Next.js App Router pages (/ , /tasks)
├── lib/              # fetch helpers, auth token handling
└── tests/            # vitest
```

**Structure Decision**: Use existing backend `src`/`tests` and `frontend` dirs; add auth/user modules within `src/api`/`src/services`/`src/models`; frontend stays in `frontend/app` and `frontend/lib`.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |

## Phase 0: Outline & Research

- Unknowns to resolve:
  - Password hashing choice: bcrypt vs argon2; default to bcrypt for existing passlib footprint unless ADR chooses argon2.  
  - JWT expiry/claims: default exp (e.g., 24h) and required claims (sub, username); refresh/rotation out of scope unless required.  
  - Cross-user denial code: consistent 403 vs 404; choose one and document in ADR.  
  - Frontend token storage: localStorage vs cookie; default to localStorage for parity with current pattern; flag CSRF considerations.
- Research tasks:
  - Best practices for bcrypt parameters under passlib and async FastAPI.
  - JWT signing/verification with shared secret; how to include user id and username minimally.
  - SQLModel patterns for user-task FK and per-request session scope.
- Deliverable: `research.md` capturing decisions, rationale, and alternatives.

## Phase 1: Design & Contracts

- Data model: define `User` (id, username unique, password_hash, timestamps), `Task` adds `owner_id` FK to User. Capture in `data-model.md`.
- Contracts: REST endpoints in `contracts/` for `/api/register`, `/api/login`, `/api/tasks` CRUD/toggle with auth enforcement and error shapes (401/403). Include payloads and response schemas (high level).
- Quickstart: `quickstart.md` with env setup (`DATABASE_URL`, `BETTER_AUTH_SECRET`), sample curl for register/login/token use, and frontend env sync via bootstrap script.
- Agent context: run `.specify/scripts/bash/update-agent-context.sh codex` to record new tech (bcrypt, user entity).
- Re-evaluate Constitution Check after design: ensure TDD, typing, coverage, ADRs for hashing/deny-code decisions.
