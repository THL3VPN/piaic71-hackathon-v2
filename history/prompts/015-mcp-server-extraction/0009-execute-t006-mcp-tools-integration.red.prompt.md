---
id: 0009
title: execute-t006-mcp-tools-integration
stage: red
date: 2026-01-02T02:51:16+05:00
surface: cli
model: gpt-5
feature: 015-mcp-server-extraction
branch: 015-mcp-server-extraction
user: user
command: T006
labels: [t006, red, integration]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/integration/test_mcp_tools_api.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/tasks.md
tests:
  - name: uv run pytest tests/contract/test_mcp_tools_contract.py tests/integration/test_mcp_tools_api.py
    result: fail
---

## Prompt

Task T006: Add integration tests for MCP tool operations.

## Response snapshot

Added integration tests for MCP add/list/update/complete/delete; initial run failed due to result shape.

## Outcome

- ✅ Impact: Integration coverage added for MCP tool operations.
- 🧪 Tests: uv run pytest tests/contract/test_mcp_tools_contract.py tests/integration/test_mcp_tools_api.py (fail)
- 📁 Files: tests/integration/test_mcp_tools_api.py, specs/015-mcp-server-extraction/tasks.md
- 🔁 Next prompts: Implement MCP tool handlers and entrypoint (T007/T008).
- 🧠 Reflection: Normalize MCP call_tool outputs in tests.

## Evaluation notes (flywheel)

- Failure modes observed: call_tool result format mismatched expectations
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Unwrap result payload in tests.
