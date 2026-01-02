---
id: 0002
title: mcp-result-unwrap
stage: green
date: 2026-01-03T04:30:39+05:00
surface: cli
model: gpt-5
feature: 019-agent-tool-chaining
branch: 018-chat-widget-polish
user: user
command: fix
labels: [mcp-client, tool-calls, tests]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/019-agent-tool-chaining/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/src/services/mcp_client.py
  - /home/aie/all_data/piaic71-hackathon-v2/tests/unit/test_mcp_client.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/019-agent-tool-chaining/tasks.md
tests:
  - name: ./.venv/bin/pytest tests/unit/test_mcp_client.py
    result: PASS
    details: "2 passed"
---

## Prompt

Fix MCP list_tasks result shape so tool calls are usable.

## Response snapshot

- Added unit tests for MCP tool result unwrapping.
- Normalized structuredContent with single result key.
- Ran unit test via venv pytest.

## Outcome

- ✅ Impact: list_tasks results now match expected tool payload shape.
- 🧪 Tests: pytest passed (2 tests).
- 📁 Files: mcp_client + new unit test + tasks update.
- 🔁 Next prompts: retest chat on Render.
- 🧠 Reflection: normalize MCP responses consistently for agent prompts.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): add integration test for list_tasks MCP result.
