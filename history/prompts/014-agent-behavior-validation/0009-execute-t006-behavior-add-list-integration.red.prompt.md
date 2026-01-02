---
id: 0009
title: execute-t006-behavior-add-list-integration
stage: red
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T006
labels: [t006, red, integration]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_agent_behavior_add_list_api.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py
    result: fail
---

## Prompt

Task T006: Add integration test for natural language add/list flows.

## Response snapshot

Added integration test using stubbed agent responses for add and list intents; suite failed overall due to contract tests.

## Outcome

- ✅ Impact: Integration coverage added for add/list behavior in chat.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py (fail)
- 📁 Files: tests/integration/test_agent_behavior_add_list_api.py, specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Refine system instructions to satisfy contract tests (T007/T008).
- 🧠 Reflection: Integration tests should remain deterministic via stubs.

## Evaluation notes (flywheel)

- Failure modes observed: Contract tests failing due to instruction gaps
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Expand system instructions.
