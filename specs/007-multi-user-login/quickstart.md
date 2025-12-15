# Quickstart: Username/Password Auth with User-Scoped Tasks

## Backend

```bash
cp .env.example .env
export BETTER_AUTH_SECRET=replace-with-shared-secret       # or your value
export DATABASE_URL="postgresql://user:pass@host/db?sslmode=require&channel_binding=require"
export RUN_DB_TESTS=1  # optional if you want DB integration tests
./scripts/bootstrap.sh backend
```

## Frontend

```bash
# syncs frontend/.env.local from .env and runs Next dev
./scripts/bootstrap.sh frontend
```

## Manual flow (curl)

```bash
# Register
curl -X POST http://localhost:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}'

# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret"}' | jq -r .token)

# Create task (scoped to alice)
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"My task"}'

# List tasks (only alice’s)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/tasks
```

## Frontend flow

- Visit `http://localhost:3000`
- Use the combined Login/Register page to create an account or log in
- After login you are redirected to `/tasks`, which lists only your tasks and attaches the JWT automatically

## Tests

```bash
BETTER_AUTH_SECRET=replace-with-shared-secret \
DATABASE_URL=sqlite+aiosqlite:///:memory: \
RUN_DB_TESTS=0 \
UV_CACHE_DIR="$(pwd)/.uv-cache" \
uv run python3.13 -m pytest --cov=src

# Frontend
(cd frontend && npm run test)
```
