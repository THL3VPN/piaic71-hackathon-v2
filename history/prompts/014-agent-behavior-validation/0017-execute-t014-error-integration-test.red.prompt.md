---
id: 0017
title: execute-t014-error-integration-test
stage: red
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T014
labels: [t014, red, integration]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_agent_behavior_errors_api.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_errors_contract.py tests/integration/test_agent_behavior_errors_api.py
    result: pass
---

## Prompt

Task T014: Add integration test for task-not-found messaging.

## Response snapshot

Added integration test validating friendly response and tool_calls when a task is missing; tests passed.

## Outcome

- ✅ Impact: Error handling is covered end-to-end for chat behavior.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_errors_contract.py tests/integration/test_agent_behavior_errors_api.py (pass)
- 📁 Files: tests/integration/test_agent_behavior_errors_api.py, specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Confirm error-response guidance (T015).
- 🧠 Reflection: Keep error messages polite and actionable.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
