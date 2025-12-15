# Implementation Plan: Secure API requests with JWT verification

**Branch**: `006-jwt-auth` | **Date**: 2024-10-06 | **Spec**: `/specs/006-jwt-auth/spec.md`
**Input**: Feature specification from `/specs/006-jwt-auth/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Add an auth middleware that enforces `Authorization: Bearer` headers on `/api/*`, validates JWTs signed with `BETTER_AUTH_SECRET`, and decorates `fastapi.Request.state.auth` with the extracted `user_id`. Tests will follow the TDD flow for missing, invalid, and valid tokens.

## Technical Context

**Language/Version**: Python 3.12+ (required)  
**Primary Dependencies**: UV-managed FastAPI, python-jose (or PyJWT), pytest  
**Storage**: SQLite (existing SQLModel task store)  
**Testing**: pytest with explicit auth middleware coverage  
**Target Platform**: Linux server and local developer machines  
**Project Type**: Single web backend (FastAPI)  
**Performance Goals**: Maintain existing throughput; signature checks should stay efficient (policy: reuse loaded secret).  
**Constraints**: Coverage ≥80%, dataclasses for structured request context, TDD-first development, do not spin up external auth providers.  
**Scale/Scope**: Protect the task API for hundreds of local/dev requests per minute.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan documents how TDD will be performed.
- Python 3.12+ with type hints everywhere; dataclasses are the default for structured data.
- UV is the package manager; the environment needs `BETTER_AUTH_SECRET` for runtime.
- Quality bars: all planned changes must maintain ≥80% coverage; add ADR references for any significant design choices (e.g., verifying tokens in middleware rather than at endpoint level).

## Project Structure

### Documentation (this feature)

```text
specs/006-jwt-auth/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
src/
├── main.py             # FastAPI app + router
├── services/
│   ├── task_repo.py    # existing data access
│   └── auth.py         # new JWT middleware/helpers
├── models/
│   └── ...             # SQLModel task definition
└── lib/
    └── jwt_helpers.py  # token validation helpers

tests/
├── unit/
│   └── test_auth_middleware.py  # missing/invalid/valid token tests
└── integration/
    └── test_task_api.py        # ensures middleware wraps existing endpoints
```

**Structure Decision**: Use the existing single backend project layout. Insert JWT helpers under `src/lib` and `src/services`, and expand `tests/unit` with middleware coverage before touching integration tests.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | --- | --- |
