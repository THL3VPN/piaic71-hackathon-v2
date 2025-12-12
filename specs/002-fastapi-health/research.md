# Research: FastAPI Health Service

## Decisions

### Framework and runtime
- **Decision**: Use FastAPI with uvicorn entrypoint.
- **Rationale**: Meets acceptance criteria for `/health`, supports type hints/docstrings, minimal overhead.
- **Alternatives considered**: Flask/Starlette directly—FastAPI gives built-in OpenAPI and type-friendly patterns with little extra cost.

### Endpoint contract
- **Decision**: `GET /health` returns HTTP 200 with JSON `{"status": "ok"}`.
- **Rationale**: Explicit, simple payload aligned to acceptance; easy to assert in tests and curls.
- **Alternatives considered**: Include uptime/version—out of scope for minimal bootstrap; keep minimal per acceptance.

### Architecture shape
- **Decision**: Single FastAPI app with router module `src/api/health.py`; `src/main.py` hosts app and uvicorn entry.
- **Rationale**: Keeps code small, testable, and aligned with repo structure; easy to extend later.
- **Alternatives considered**: Monolithic single file—router module separation improves clarity/testability with no real cost.

### Testing strategy
- **Decision**: pytest with FastAPI TestClient for unit-level endpoint tests; optional live/integration test if needed.
- **Rationale**: Fast feedback, satisfies coverage requirement, no external deps.
- **Alternatives considered**: Hitting live uvicorn process—not needed for this minimal scope; optional if desired later.

### Error handling
- **Decision**: Rely on FastAPI defaults; ensure `/health` always returns 200/JSON absent external deps.
- **Rationale**: No auth/DB; minimal surface; default handlers suffice.
- **Alternatives considered**: Custom middleware—unnecessary for single endpoint.
