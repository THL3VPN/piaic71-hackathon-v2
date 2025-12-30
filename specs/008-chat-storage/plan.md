# Implementation Plan: Chat Storage Persistence

**Branch**: `008-chat-storage` | **Date**: 2025-12-31 | **Spec**: /home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/spec.md
**Input**: Feature specification from `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/spec.md`

**Note**: This plan follows the Spec-Kit workflow and constitution requirements.

## Summary

Persist chat conversations and messages in the database with strict user ownership, ensuring history survives restarts while the backend remains stateless. The approach adds new Conversation and Message models, repository-style persistence services, and storage-focused API contracts for creating conversations, appending messages, and retrieving history with ordering and limits.

## Technical Context

**Language/Version**: Python 3.13 (meets Python 3.12+ requirement)  
**Primary Dependencies**: FastAPI, SQLModel, SQLAlchemy (async), psycopg, uvicorn, pytest, pytest-cov, httpx  
**Storage**: Neon PostgreSQL via `DATABASE_URL` (async engine)  
**Testing**: pytest (TDD) with pytest-cov (≥80% coverage)  
**Target Platform**: Linux server (containerized deployment)  
**Project Type**: Backend API service (FastAPI)  
**Performance Goals**: 95% of history retrieval requests return within 1 second for up to 50 messages  
**Constraints**: Stateless service, ownership enforced per request, user_id derived from auth context only, timestamps server-generated, transactional writes, type hints everywhere, ADR required for material decisions  
**Scale/Scope**: Single service; per-user conversations; default history limit 50; supports thousands of conversations per user

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (pytest), executed to red, then implemented to green; plan documents how TDD will be performed.
- Python 3.12+ with type hints everywhere; dataclasses are the default for structured data where applicable.
- UV is the package/environment manager; no additional system dependencies are required beyond PostgreSQL connectivity.
- Quality bars: all planned changes must maintain ≥80% coverage; ADRs required only for material architectural changes (none identified yet).

## Architecture Sketch

- **API Layer**: New storage-focused endpoints to create conversations, append messages, and list history; all endpoints require auth.
- **Service/Repo Layer**: Conversation and Message persistence functions enforce ownership checks and transactional operations.
- **Data Layer**: SQLModel models for Conversation and Message, linked by foreign key with indexed user ownership.
- **Auth Integration**: User identity sourced from existing auth middleware context only.

## Interfaces (API Contracts)

Contracts will be defined in `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/contracts/chat-storage.openapi.yaml` with:
- `POST /api/conversations` → create conversation, returns conversation id and timestamps
- `POST /api/conversations/{conversation_id}/messages` → append message with role/content
- `GET /api/conversations/{conversation_id}/messages?limit=` → retrieve history ordered by created_at asc

## Data Model

Detailed entity definitions are documented in `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/data-model.md`.

## Error Handling

- **401 Unauthorized**: Missing/invalid auth token.
- **403 Forbidden**: User attempts to access a conversation or message they do not own.
- **404 Not Found**: Conversation does not exist for the given identifier.
- **422 Unprocessable Entity**: Invalid role, empty content, or invalid limit.
- **500 Internal Error**: Unexpected persistence failures (should be rare; logged and surfaced with generic message).

## Requirements Traceability

- FR-001/FR-002/FR-009 → SQLModel Conversation/Message with server timestamps and persistence in PostgreSQL.
- FR-003/FR-004/FR-005/FR-008 → Auth-context user_id; ownership checks in repo layer and API guards.
- FR-006/FR-007 → Ordered history queries with validated limit parameter.
- FR-010 → Session-managed transactions around create/update operations.

## Testing Strategy (TDD)

- **Unit Tests**: Repository functions for conversation/message creation, ownership enforcement, ordering, limit handling, and role validation.
- **Integration Tests**: API-level tests for create conversation, append message, and history retrieval using an isolated test database.
- **Coverage**: Maintain ≥80% overall, with new tests added for all acceptance scenarios and edge cases.

## Project Structure

### Documentation (this feature)

```text
/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
/home/aie/all_data/piaic71-hackathon-v2/src/
├── api/
├── models/
├── services/
└── main.py

/home/aie/all_data/piaic71-hackathon-v2/tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: Single backend service under `/home/aie/all_data/piaic71-hackathon-v2/src/` with tests in `/home/aie/all_data/piaic71-hackathon-v2/tests/`.

## Complexity Tracking

No constitution violations anticipated; no complexity exceptions required.

## Decisions Needing Tradeoffs

1. **Message ordering source**
   - Option A: Order by `created_at` only (simple, stable)
   - Option B: Order by `created_at`, then `id` (stable tie-break)
   - Decision: Option B for deterministic ordering on equal timestamps.
2. **History limit validation**
   - Option A: Reject non-positive limits (422)
   - Option B: Coerce to default limit
   - Decision: Option A to prevent ambiguous client behavior.
3. **Conversation updated_at behavior**
   - Option A: Update on each new message
   - Option B: Update only on explicit conversation updates
   - Decision: Option A for accurate last-activity tracking.

## Phase 0: Outline & Research

**Output**: `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/research.md`

Research tasks:
- Confirm best practices for ownership enforcement in async SQLModel repositories.
- Confirm transaction handling patterns for create + append message flows.
- Confirm recommended validation for message role and history limit parameters.

## Phase 1: Design & Contracts

**Prerequisites**: Phase 0 complete

Artifacts:
- `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/data-model.md`
- `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/contracts/chat-storage.openapi.yaml`
- `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/quickstart.md`

Agent context update:
- Run `/home/aie/all_data/piaic71-hackathon-v2/.specify/scripts/bash/update-agent-context.sh codex`

Re-check Constitution Check after Phase 1.

## Phase 2: Task Breakdown

Tasks will be generated in `/home/aie/all_data/piaic71-hackathon-v2/specs/008-chat-storage/tasks.md` via `/sp.tasks`.

## Post-Design Constitution Check

- TDD workflow documented with unit + integration tests.
- Python 3.13 meets 3.12+ requirement; type hints planned throughout.
- UV remains package manager; no new system dependencies introduced.
- Coverage ≥80% maintained; no ADR required for this feature scope.
