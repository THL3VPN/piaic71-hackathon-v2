---
id: 0015
title: add-mcp-ownership-tests
stage: green
date: 2026-01-01T22:25:56Z
surface: cli
model: gpt-5
feature: 015-mcp-server-extraction
branch: 015-mcp-server-extraction
user: user
command: T014/T015
labels: [t014, t015, mcp, ownership]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_mcp_ownership_contract.py
  - /home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_chat_mcp_ownership_api.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/tasks.md
tests:
  - name: uv run pytest tests/contract/test_mcp_ownership_contract.py tests/integration/test_chat_mcp_ownership_api.py
    result: pass
---

## Prompt

go ahead proceed

## Response snapshot

Added MCP ownership tests for tool handlers and chat flow; tasks marked complete.

## Outcome

- ✅ Impact: Ownership violations return not-found style errors in MCP and chat.
- 🧪 Tests: uv run pytest tests/contract/test_mcp_ownership_contract.py tests/integration/test_chat_mcp_ownership_api.py (pass)
- 📁 Files: tests/contract/test_mcp_ownership_contract.py, tests/integration/test_chat_mcp_ownership_api.py, specs/015-mcp-server-extraction/tasks.md
- 🔁 Next prompts: Confirm remaining tasks (T016–T018).
- 🧠 Reflection: Keep ownership errors consistent across MCP and chat.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
