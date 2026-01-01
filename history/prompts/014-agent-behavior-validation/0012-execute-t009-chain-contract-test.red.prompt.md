---
id: 0012
title: execute-t009-chain-contract-test
stage: red
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T009
labels: [t009, red, contract]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_agent_behavior_chain_contract.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_chain_contract.py tests/integration/test_agent_behavior_chain_api.py
    result: pass
---

## Prompt

Task T009: Create contract test for tool chaining rules.

## Response snapshot

Added contract test to assert tool chaining guidance exists in system instructions; test passed on first run.

## Outcome

- ✅ Impact: Tool chaining guidance is now covered by contract test.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_chain_contract.py tests/integration/test_agent_behavior_chain_api.py (pass)
- 📁 Files: tests/contract/test_agent_behavior_chain_contract.py, specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Add integration test for ambiguous chain behavior (T010).
- 🧠 Reflection: Contract tests should keep instruction rules explicit and deterministic.

## Evaluation notes (flywheel)

- Failure modes observed: None (tests passed on first run)
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
