# Frontend + Backend Health Bootstrap

## Backend (Python / UV)

```bash
export UV_PYTHON=python3.13
export UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache
export BETTER_AUTH_SECRET=replace-with-shared-secret
uv run uvicorn src.main:app --reload --port 8000
```

All `/api/*` endpoints now require `Authorization: Bearer <token>`. Use the sample token exported via `BETTER_AUTH_TOKEN` (see `specs/006-jwt-auth/quickstart.md`) to exercise the guard manually. Missing or invalid tokens return `401 Unauthorized` with a JSON detail payload describing the failure.

## Frontend (Next.js 16+ App Router)

```bash
cd frontend
npm install
npm run dev
```

The homepage (`http://localhost:3000`) fetches `http://localhost:8000/health` via a proxy rewrite (`/api/health`) and displays the backend status.

### Environment variables

If you need to point the frontend at an alternate backend (e.g., AWS preview), set `NEXT_PUBLIC_BACKEND_URL` before running `npm run dev`. When the variable is present, the rewrite still prefers `/api/health`, but direct fetches will hit `${NEXT_PUBLIC_BACKEND_URL}/health`.

## Fresh clone checklist (backend + frontend)

1) Prereqs: Python 3.13+, [uv](https://github.com/astral-sh/uv) installed, Node 20+, npm.
2) Clone: `git clone <repo>` then `cd piaic71-hackathon-v2`.
3) Backend setup:
   ```bash
   export UV_PYTHON=python3.13
   export UV_CACHE_DIR="$(pwd)/.uv-cache"
   export BETTER_AUTH_SECRET=replace-with-shared-secret
   uv sync  # optional: create/refresh the .venv from uv.lock
   uv run uvicorn src.main:app --reload --port 8000
   ```
   - All `/api/*` calls require `Authorization: Bearer <token>`.
   - Use the demo token from `specs/006-jwt-auth/quickstart.md` or create your own HS256 JWT with `BETTER_AUTH_SECRET`.
4) Frontend setup:
   ```bash
   cd frontend
   npm install
   echo "NEXT_PUBLIC_BETTER_AUTH_TOKEN=<your-demo-token>" > .env.local
   npm run dev -- --hostname 0.0.0.0 --port 3000
   ```
   Open `http://localhost:3000` (or `/tasks`) and ensure the browser sends the bearer token. CORS is configured for `localhost:3000`.
5) Tests:
   - Backend: `BETTER_AUTH_SECRET=replace-with-shared-secret uv run python3.13 -m pytest --cov=src`
   - Frontend: `npm run lint` and `npm run test`
6) Troubleshooting:
   - If browser sees `401` or CORS errors, confirm the token header is present and matches `BETTER_AUTH_SECRET`.
   - Restart `npm run dev` after editing `.env.local`; restart `uvicorn` after changing backend env vars.

## One-command setup via script

1) `cp .env.example .env` and edit the secret/token if needed.
2) Start backend (also syncs frontend env): `./scripts/bootstrap.sh backend`
3) In another terminal start frontend: `./scripts/bootstrap.sh frontend`

The script reads `.env`, writes `frontend/.env.local`, installs deps if missing, and runs servers on `BACKEND_PORT`/`FRONTEND_PORT`.

Notes on `.env` values:
- `DATABASE_URL` is required for the backend (use your Neon/Postgres URL).
- `BETTER_AUTH_SECRET` and `NEXT_PUBLIC_BETTER_AUTH_TOKEN` must match (HS256).
- `RUN_DB_TESTS=1` if you want database integration tests to run; otherwise they skip.

### Tests

- `npm run lint` (ESLint with Next/TypeScript rules + rewrite-aware config).
- `npm run test` (Vitest + Testing Library covering the health card fetch/backoff behavior).
