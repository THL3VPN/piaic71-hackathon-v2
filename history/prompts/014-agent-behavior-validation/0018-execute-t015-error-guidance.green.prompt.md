---
id: 0018
title: execute-t015-error-guidance
stage: green
date: 2026-01-02T02:11:49+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: T015
labels: [t015, green, instructions]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests:
  - name: uv run pytest tests/contract/test_agent_behavior_errors_contract.py tests/integration/test_agent_behavior_errors_api.py
    result: pass
---

## Prompt

Task T015: Refine error-response guidance in agent instructions.

## Response snapshot

Confirmed existing system instructions already include task-not-found guidance; no code changes required.

## Outcome

- ✅ Impact: Error guidance verified as present and covered by tests.
- 🧪 Tests: uv run pytest tests/contract/test_agent_behavior_errors_contract.py tests/integration/test_agent_behavior_errors_api.py (pass)
- 📁 Files: specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Run quickstart validation (T016).
- 🧠 Reflection: Keep error guidance aligned with user-facing tone requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
