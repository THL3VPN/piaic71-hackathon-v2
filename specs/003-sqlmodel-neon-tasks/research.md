# Research: Persistent Task Storage (SQLModel + Neon Postgres)

**Date**: 2025-12-13  
**Branch**: 003-sqlmodel-neon-tasks

## Decisions

### D1: ORM and Driver
- **Decision**: Use SQLModel with async SQLAlchemy engine and psycopg for Postgres.
- **Rationale**: SQLModel aligns with FastAPI ecosystem, provides typed models, and supports async interactions needed for Neon.
- **Alternatives considered**: SQLAlchemy Core (more boilerplate), synchronous engine (blocks event loop), ORMs like Tortoise (less aligned with current stack).

### D2: Schema Management
- **Decision**: Use `SQLModel.metadata.create_all(engine)` on startup for this increment.
- **Rationale**: Fast, code-driven, sufficient for single-table MVP; avoids migration overhead now.
- **Alternatives considered**: Alembic migrations (more robust but heavier for one table), manual SQL DDL (adds maintenance overhead).

### D3: Connection Handling
- **Decision**: Create async engine from `DATABASE_URL`; use session dependency factory (contextmanager) for per-request/per-operation sessions.
- **Rationale**: Avoid global session state, keeps tests isolated; works with Neon serverless.
- **Alternatives considered**: Global session or sync engine (risk of blocking), connection pooling tweaks (premature for current scope).

### D4: Service Layer
- **Decision**: Implement a repository/service module for task CRUD separate from HTTP routes.
- **Rationale**: Supports unit/integration testing without HTTP, aligns with requirement to keep handlers thin.
- **Alternatives considered**: Inline DB logic in routes (violates spec), generic repository abstraction (overkill for single model).

### D5: Validation and Defaults
- **Decision**: Enforce non-empty title before hitting DB; `completed` default false; `created_at` stored in UTC via SQLModel default_factory.
- **Rationale**: Matches acceptance criteria; avoids DB constraint-only validation and timezone drift.
- **Alternatives considered**: DB-only constraints (poorer UX), naive datetime without timezone (risk of skew).

## Open Questions / Clarifications
- None identified; spec is clear for this increment.

## References
- SQLModel docs (async engine, session usage)
- Neon Postgres connection guidance for async SQLAlchemy/psycopg
