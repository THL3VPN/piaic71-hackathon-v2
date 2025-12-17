# TaskBoard (FastAPI + Next.js)

## Quick start (local)

1) Create `.env`:

```bash
cp .env.example .env
```

2) Start backend:

```bash
./scripts/bootstrap.sh backend
```

3) Start frontend (separate terminal):

```bash
./scripts/bootstrap.sh frontend
```

Open `http://localhost:3000`.

## Environment variables

These are the variables you typically need to change:

- `DATABASE_URL` (backend): Postgres connection string (Neon/Render/etc.)
- `BETTER_AUTH_SECRET` (backend): JWT signing secret (must stay consistent)
- `NEXT_PUBLIC_BACKEND_URL` (frontend): Base URL of the backend (no trailing slash)
- `NEXT_PUBLIC_API_BASE_URL` (backend CORS): The *frontend origin* to allow for CORS.
  - Example: `https://piaic71-hackathon-v2-frontend.vercel.app`
  - This must match the browser origin exactly (scheme + host + port), no trailing slash.

## Tests

- Backend:

```bash
BETTER_AUTH_SECRET=replace-with-shared-secret \
DATABASE_URL=sqlite+aiosqlite:///:memory: \
RUN_DB_TESTS=0 \
UV_CACHE_DIR="$(pwd)/.uv-cache" \
uv run python3.13 -m pytest --cov=src
```

- Frontend:

```bash
cd frontend
npm test
```
