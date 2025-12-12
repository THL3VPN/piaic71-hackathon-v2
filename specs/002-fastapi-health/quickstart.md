# Quickstart: FastAPI Health Service

## Prerequisites

- Python 3.13+
- UV package manager installed (`pip install uv`)

## Setup

```bash
# from repo root
uv sync
```

## Run the service

```bash
UV_PYTHON=python3.13 uv run uvicorn src.main:app --reload --port 8000
```

## Verify health

```bash
curl -i http://localhost:8000/health
```

Expected: `HTTP/1.1 200 OK` and body `{"status":"ok"}`.

## Testing (TDD)

```bash
UV_PYTHON=python3.13 uv run pytest --cov=src --cov-report=term-missing
```

Coverage target: ≥80% overall (health endpoint covered).
