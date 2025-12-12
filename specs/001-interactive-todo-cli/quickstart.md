# Quickstart: Interactive CLI Todo App

## Prerequisites

- Python 3.12+
- UV package manager installed (`pip install uv` if needed)

## Setup

```bash
# from repo root
uv sync
```

## Run the app

```bash
UV_PYTHON=python3.13 uv run python main.py
```

Expected: interactive main menu with options to View, Add, Update, Delete, Mark Complete/Incomplete, Exit. Use arrow keys for selection; in non-interactive environments, inject input mocks.

## Testing (TDD)

```bash
uv run pytest --cov=src --cov-report=term-missing
```

Targets: ≥80% overall coverage (currently 100%).

## Notes

- Tasks are in-memory only; they reset each run.
- Keep titles non-empty; invalid IDs return “task not found” without exiting.
