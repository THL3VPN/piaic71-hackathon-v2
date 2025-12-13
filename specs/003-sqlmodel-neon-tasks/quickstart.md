# Quickstart: Persistent Task Storage (SQLModel + Neon)

## Prerequisites
- Python 3.13 available; UV installed
- Set `DATABASE_URL` to your Neon Postgres connection (e.g., `postgresql://neondb_owner:...` to use uvicorn or tests)

## Neon setup
To exercise database-heavy tests or run the service against Neon:
```bash
export DATABASE_URL="postgresql://neondb_owner:npg_xnOe7Ta9oWIt@ep-autumn-violet-a43cnvj3-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
export RUN_DB_TESTS=1
```

## Setup
```bash
export UV_PYTHON=python3.13
export UV_CACHE_DIR=.uv-cache
uv sync
```

## Run service
```bash
UV_PYTHON=python3.13 UV_CACHE_DIR=.uv-cache uv run uvicorn src.main:app --reload --port 8000
```

## Run tests (unit + integration)
```bash
UV_PYTHON=python3.13 UV_CACHE_DIR=.uv-cache uv run pytest --cov=src --cov-report=term-missing
```

With Neon connectivity (set `DATABASE_URL` and `RUN_DB_TESTS=1`), rerun the same command to include the database-heavy suites that otherwise skip in the default environment.

For integration tests hitting Neon: ensure `RUN_DB_TESTS=1` plus your `DATABASE_URL` are exported before running pytest. Without them the DB-heavy tests are skipped to avoid sqlite deadlocks.

## Expected behaviors
- Startup applies SQLModel metadata to create the Task table if missing.
- `create_task` rejects empty titles and returns persisted record with defaults.
- `get_task` returns task or a not-found signal without raising unhandled exceptions.
- `list_tasks` returns tasks ordered deterministically (created_at ascending) and returns an empty list when no data.
