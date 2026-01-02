---
id: 0008
title: execute-t005-behavior-list-contract-test
stage: red
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T005
labels: [t005, red, contract]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_agent_behavior_list_contract.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py
    result: fail
---

## Prompt

Task T005: Create contract test for task listing intent mapping.

## Response snapshot

Added contract test asserting list_tasks and status mapping appear in system instructions; test failed as expected before prompt updates.

## Outcome

- ✅ Impact: Red test captures missing list_tasks status mapping in system instructions.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py (fail)
- 📁 Files: tests/contract/test_agent_behavior_list_contract.py, specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Add integration test for add/list (T006).
- 🧠 Reflection: Status mappings must be explicit to avoid model drift.

## Evaluation notes (flywheel)

- Failure modes observed: Missing list_tasks status mapping in system instructions
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Add explicit status mapping rules.
