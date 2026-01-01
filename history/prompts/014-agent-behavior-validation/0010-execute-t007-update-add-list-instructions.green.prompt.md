---
id: 0010
title: execute-t007-update-add-list-instructions
stage: green
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T007
labels: [t007, green, instructions]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/src/services/agent_runtime.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py
    result: pass
---

## Prompt

Task T007: Refine agent system instructions for add/list intents.

## Response snapshot

Expanded system instructions with explicit tool mapping and status mapping rules to satisfy behavior contracts.

## Outcome

- ✅ Impact: Add/list intent guidance encoded in system instructions.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_create_contract.py tests/contract/test_agent_behavior_list_contract.py tests/integration/test_agent_behavior_add_list_api.py (pass)
- 📁 Files: src/services/agent_runtime.py, specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Ensure confirmations are friendly and concise (T008).
- 🧠 Reflection: Explicit tool names reduce model ambiguity.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
