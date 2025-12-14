# Frontend + Backend Health Bootstrap

## Backend (Python / UV)

```bash
export UV_PYTHON=python3.13
export UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache
uv run uvicorn src.main:app --reload --port 8000
```

## Frontend (Next.js 16+ App Router)

```bash
cd frontend
npm install
npm run dev
```

The homepage (`http://localhost:3000`) fetches `http://localhost:8000/health` via a proxy rewrite (`/api/health`) and displays the backend status.

### Environment variables

If you need to point the frontend at an alternate backend (e.g., AWS preview), set `NEXT_PUBLIC_BACKEND_URL` before running `npm run dev`. When the variable is present, the rewrite still prefers `/api/health`, but direct fetches will hit `${NEXT_PUBLIC_BACKEND_URL}/health`.

### Tests

- `npm run lint` (ESLint with Next/TypeScript rules + rewrite-aware config).
- `npm run test` (Vitest + Testing Library covering the health card fetch/backoff behavior).
