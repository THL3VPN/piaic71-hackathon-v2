# Quickstart: Next.js frontend health bootstrap

## Architecture

- Backend continues in `backend/` (existing UV-managed Python app serving `/health`).
- Frontend is a Next.js 16+ App Router app in `frontend/`.
- The homepage renders a “Backend health” card and fetches `GET /health` via a client component.
- `next.config.js` defines rewrites so `/api/health` routes to `http://localhost:8000/health`, avoiding CORS in dev.

## Interfaces

- `frontend/app/page.tsx` (or tsx) renders the homepage and calls the backend health endpoint.
- The backend `/health` endpoint returns JSON `{ "status": "ok" }` (existing contract).
- Fetch errors show a fallback message (“Backend: unavailable”).

## Running locally

1. Start the backend (from repo root):
   ```bash
   export UV_PYTHON=python3.13
   export UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache
   uv run uvicorn src.main:app --reload --port 8000
   ```
2. Start the frontend:
   ```bash
   cd frontend
   npm install       # or yarn
   npm run dev       # runs Next dev server on http://localhost:3000
   ```
3. Open http://localhost:3000; the homepage displays “Backend: OK” after calling `/api/health` (proxy ensures no CORS errors).

## Tests

- Frontend: `cd frontend && npm run lint` and `npm run test` to cover linting and the health card behavior.
- Backend: existing pytest suites remain (no new tests yet from this spec).

## Error handling notes

- The frontend handles fetch failures by showing “Backend: unavailable (error message)” and logging the failure. The Vitest suite mocks a failed fetch to keep this behavior covered.
