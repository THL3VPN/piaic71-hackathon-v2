---
id: 0007
title: execute-t004-behavior-create-contract-test
stage: red
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T004
labels: [t004, red, contract]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_agent_behavior_create_contract.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py
    result: fail
---

## Prompt

Task T004: Create contract test for natural language task creation intent.

## Response snapshot

Added contract test that asserts system instructions include add_task guidance; test failed as expected before prompt updates.

## Outcome

- ✅ Impact: Red test captures missing add_task intent mapping in system instructions.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py (fail)
- 📁 Files: tests/contract/test_agent_behavior_create_contract.py, specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Add list intent contract test (T005).
- 🧠 Reflection: Use tool names in instructions to keep intent mapping explicit.

## Evaluation notes (flywheel)

- Failure modes observed: Missing add_task mention in system instructions
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Expand system instructions with explicit tool mapping.
