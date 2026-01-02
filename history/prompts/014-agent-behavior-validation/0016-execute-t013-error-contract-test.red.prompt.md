---
id: 0016
title: execute-t013-error-contract-test
stage: red
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T013
labels: [t013, red, contract]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_agent_behavior_errors_contract.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_errors_contract.py tests/integration/test_agent_behavior_errors_api.py
    result: pass
---

## Prompt

Task T013: Create contract test for task-not-found response guidance.

## Response snapshot

Added contract test asserting task-not-found guidance in system instructions; test passed on first run.

## Outcome

- ✅ Impact: Error guidance covered by contract test.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_errors_contract.py tests/integration/test_agent_behavior_errors_api.py (pass)
- 📁 Files: tests/contract/test_agent_behavior_errors_contract.py, specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Add integration error test (T014).
- 🧠 Reflection: Keep error guidance explicit and user-friendly.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
