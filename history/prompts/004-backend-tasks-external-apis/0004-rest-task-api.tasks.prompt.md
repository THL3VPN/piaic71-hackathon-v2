---
id: 0004
title: rest-task-api
stage: tasks
date: 2024-05-08
surface: shell
model: codex
feature: 004-backend-tasks-external-apis
branch: 004-backend-tasks-external-apis
user: aie
command: uv run pytest --cov=src --cov-report=term-missing
labels: []
links:
  spec: specs/004-backend-tasks-external-apis/spec.md
  ticket:
  adr:
  pr:
files:
  - src/api/tasks.py
  - src/services/db.py
  - tests/integration/test_task_api.py
  - specs/004-backend-tasks-external-apis/tasks.md
tests:
  - RUN_DB_TESTS=1 uv run pytest --cov=src --cov-report=term-missing
---

## Prompt

Rerun the coverage suite, confirm polish tasks (T022-T025) are resolved, and prepare final notes about the REST API coverage/data consistency.

## Response snapshot

Simplified the SQLAlchemy session helper, tightened the API tests (error payload validation + new schema), reran the full coverage command successfully, and updated the task list to reflect T022-T024.

## Outcome

- ✅ Impact: Coverage suite now passes and the REST API endpoints stay narrowly tested per story.
- 🧪 Tests: RUN_DB_TESTS=1 uv run pytest --cov=src --cov-report=term-missing (PASS)
- 📁 Files: src/api/tasks.py; src/services/db.py; tests/integration/test_task_api.py; specs/004-backend-tasks-external-apis/tasks.md
- 🔁 Next prompts: T025 (commit/push final state)
- 🧠 Reflection: Keep dependency helpers straightforward to avoid FastAPI dependency parsing issues.

## Evaluation notes (flywheel)

- Failure modes observed: FastAPI dependencies hiccuped when session helper used decorators; validation type differs between missing fields and simple value errors.
- Graders run and results (PASS/FAIL): coverage suite PASS
- Prompt variant (if applicable): base
- Next experiment (smallest change to try): none
