# Quickstart: Task REST API

## Architecture

- FastAPI app in `src/main.py` mounts a router from `src/api/tasks.py`.
- The router is mounted at `/api/tasks` so clients can reach the CRUD endpoints without touching the CLI entrypoints.
- Routes are thin adapters that fetch the shared SQLModel session, call `src/services/task_repo.py`, and return HTTP responses.
- SQLModel uses the Neon PostgreSQL engine configured via `DATABASE_URL`.

## Interfaces

Routes:

- `GET /api/tasks`: list tasks (ordered by `created_at`, `id`).
- `POST /api/tasks`: create task with `title` + optional `description`.
- `GET /api/tasks/{id}`: return specific task or 404 JSON.
- `PUT /api/tasks/{id}`: update title/description, reuse validation.
- `DELETE /api/tasks/{id}`: remove task, 404 if missing.
- `PATCH /api/tasks/{id}/complete`: toggle completion flag.

## Running locally

1. Export environment:
   ```bash
   export UV_PYTHON=python3.13
   export UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache
   export DATABASE_URL="postgresql://neondb_owner:...@ep-autumn-violet-.../neondb?sslmode=require&channel_binding=require"
   export RUN_DB_TESTS=1
   ```
2. Start server:
   ```bash
   uv run uvicorn src.main:app --reload --port 8000
   ```
3. Verify via curl:
   ```bash
   curl -X POST http://127.0.0.1:8000/api/tasks -H "Content-Type: application/json" \
     -d '{"title":"Wash dishes","description":"Use hypoallergenic soap"}'
   curl http://127.0.0.1:8000/api/tasks
   ```

## Tests

- Unit tests: `RUN_DB_TESTS=1 uv run pytest tests/unit/test_task_service.py` (assert service logic, validation).
- Integration tests: `RUN_DB_TESTS=1 uv run pytest tests/integration/test_task_crud.py tests/integration/test_task_api.py`.
- Full coverage: `RUN_DB_TESTS=1 uv run pytest --cov=src --cov-report=term-missing`.

## Error handling notes

- Missing tasks return `404` with `{"detail":"Task not found"}`.
- Invalid payloads return FastAPI's standard 422 body with field-level messages.
