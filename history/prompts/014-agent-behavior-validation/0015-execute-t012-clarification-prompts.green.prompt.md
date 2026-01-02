---
id: 0015
title: execute-t012-clarification-prompts
stage: green
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T012
labels: [t012, green, instructions]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_chain_contract.py tests/integration/test_agent_behavior_chain_api.py
    result: pass
---

## Prompt

Task T012: Add clarification prompts for ambiguous task references.

## Response snapshot

Verified system instructions already instruct the agent to ask follow-up questions and avoid guessing.

## Outcome

- ✅ Impact: Clarification guidance confirmed without additional code changes.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_chain_contract.py tests/integration/test_agent_behavior_chain_api.py (pass)
- 📁 Files: specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Start US3 tests (T013-T014).
- 🧠 Reflection: Ambiguity handling should remain explicit and concise.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
