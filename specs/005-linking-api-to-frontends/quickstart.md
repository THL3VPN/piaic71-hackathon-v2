# Quickstart: Linking Frontend to Tasks API

## Architecture

- Backend continues to expose task endpoints under `/api` (Python + UV-managed SQLModel service).
- Frontend is a Next.js 18.3 App Router app that renders `/app/page.tsx` with a tasks list and add-task form.
- The UI hits `GET /api/tasks` to list entries, shows title/completion/description, and posts via `POST /api/tasks`.

## Interfaces

- `frontend/app/page.tsx`: handles data fetching, add-task form, validation, and responsive layout.
- Backend `/api/tasks`:
  - `GET /api/tasks`: returns `[ { id, title, description?, completed, created_at } ]`.
  - `POST /api/tasks`: accepts `{ title, description? }`, returns the created record.

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
   npm install       # (skip if already installed)
   npm run dev       # serves the UI at http://localhost:3000
   ```
3. Visit `http://localhost:3000`; the homepage lists tasks, shows completion status, and allows adding a task with a required title. The `/tasks` cards stack responsively on smaller screens, and backend outages show an inline “Backend unavailable” alert that also includes the retry-aware helper logic.

## Tests

- Frontend: `cd frontend && npm run lint` then `npm run test` (Vitest + Testing Library + validation coverage).
- Backend: existing `pytest` suites remain unchanged (ensures `GET/POST /api/tasks` still pass).
