# Implementation Plan: Frontend bootstrap with backend connectivity

**Branch**: `001-frontend-health` | **Date**: 2024-05-08 | **Spec**: specs/001-frontend-health/spec.md  
**Input**: Frontend bootstrap spec from `/specs/001-frontend-health/spec.md`

## Summary

Spin up a Next.js 16 App Router frontend that renders a homepage displaying the backend `/health` response, document how to launch both apps, and ensure local CORS/proxy configuration allows the browser call so the UI and API coexist without authentication.

## Technical Context

**Language/Version**: Frontend — JavaScript/TypeScript (Next.js 16+); Backend already running on Python 3.13 via UV  
**Primary Dependencies**: `next`, `react`, `node` (frontend); existing UV-managed backend packages remain untouched  
**Storage**: Backend health endpoint (stateless JSON), no new storage required  
**Testing**: Frontend smoke tests via Next.js `npm run lint`/`npm run build`; backend pytest suites already exist  
**Target Platform**: Browser served via Next.js dev server (`http://localhost:3000`)  
**Project Type**: Web application with separate frontend and backend directories  
**Performance Goals**: Load and fetch backend health within 5 seconds on modern dev machines  
**Constraints**: Keep coverage >=80% overall (frontend smoke/run at least Next build), front and backend must start together without CORS failures, use TDD mindset when adding tests  
**Scale/Scope**: Single-page health indicator for now; full task UI deferred

## Constitution Check

GATE: - Tests (unit/integration) are written first for the health fetch, then code to pass them (TDD).  
      - Type hints apply to any new TypeScript/frontend interfaces, and UV remains the package manager for backend/Python.  
      - Coverage floor stays ≥80%; ADR or plan note required if we change architecture beyond this bootstrap.

## Project Structure

### Documentation (this feature)

```text
specs/001-frontend-health/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
├── tasks.md
└── checklists/
    └── requirements.md
```

### Source Code (repository root)

```text
backend/                   # existing Python/UV backend (utilized by README instructions)
├── src/
│   └── ...                # unchanged

frontend/                  # new Next.js app
├── app/                    # App Router entrypoints
├── components/
├── lib/                    # fetch helpers (health client)
├── next.config.js          # configure rewrites/proxy to backend
└── package.json            # scripts for dev/build
```

**Structure Decision**: Choose a separate `frontend/` directory with Next.js 16 App Router, keeping the backend directories untouched. README will describe running both servers (`uv run uvicorn ...` and `npm run dev`), aligning with the existing backend structure.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None (all constitution checks satisfied) | - | - |
