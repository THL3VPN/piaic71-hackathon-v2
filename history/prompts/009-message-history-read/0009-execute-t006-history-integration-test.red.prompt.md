---
id: 0009
title: Execute T006 history integration test
stage: red
date: 2025-12-30T23:45:58Z
surface: codex-cli
model: gpt-5
feature: 009-message-history-read
branch: 009-message-history-read
user: user
command: /sp.execute
labels: [t006, red]
links:
  spec: specs/009-message-history-read/spec.md
  ticket: none
  adr: none
  pr: none
files:
  - path: tests/integration/test_message_history_api.py
    reason: added integration test for history endpoint
  - path: specs/009-message-history-read/tasks.md
    reason: marked T006 complete
  - path: specs/009-message-history-read/checklists/requirements.md
    reason: noted T006 red test
  - path: tests/contract/test_chat_storage_contract.py
    reason: test failure observed (GET history not implemented)
  - path: tests/contract/test_message_history_contract.py
    reason: test failure observed (GET history not implemented)
  - path: tests/integration/test_chat_storage_api.py
    reason: test failure observed (GET history not implemented)
tests:
  - name: uv run pytest -q
    result: failed
    reason: GET /api/conversations/{conversation_id}/messages returns 405
---

## Prompt

User said: "continue"

## Response snapshot

Added integration test for message history retrieval; tests fail as expected (missing GET endpoint).

## Outcome

- ✅ Impact: T006 completed (red test added).
- 🧪 Tests: Failed; GET history endpoint not yet implemented (405).
- 📁 Files: Added integration test and updated tasks/checklist.
- 🔁 Next prompts: Execute T007 (unit test)
- 🧠 Reflection: None.

## Evaluation notes (flywheel)

- Failure modes observed: Missing GET history endpoint.
- Graders run and results (PASS/FAIL): Not run.
- Prompt variant (if applicable): n/a.
- Next experiment (smallest change to try): Add unit test for message repo query ordering/ownership.
