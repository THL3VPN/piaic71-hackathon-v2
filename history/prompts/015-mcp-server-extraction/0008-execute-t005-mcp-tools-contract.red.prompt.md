---
id: 0008
title: execute-t005-mcp-tools-contract
stage: red
date: 2026-01-02T02:51:16+05:00
surface: cli
model: gpt-5
feature: 015-mcp-server-extraction
branch: 015-mcp-server-extraction
user: user
command: T005
labels: [t005, red, contract]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/tests/contract/test_mcp_tools_contract.py
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/tasks.md
tests:
  - name: uv run pytest tests/contract/test_mcp_tools_contract.py tests/integration/test_mcp_tools_api.py
    result: fail
---

## Prompt

Task T005: Add contract tests for MCP tool payloads.

## Response snapshot

Added MCP tool contract tests; initial run failed due to call_tool response shape.

## Outcome

- ✅ Impact: Contract test captures MCP tool payload expectations.
- 🧪 Tests: uv run pytest tests/contract/test_mcp_tools_contract.py tests/integration/test_mcp_tools_api.py (fail)
- 📁 Files: tests/contract/test_mcp_tools_contract.py, specs/015-mcp-server-extraction/tasks.md
- 🔁 Next prompts: Add integration tests for MCP tool operations (T006).
- 🧠 Reflection: Account for FastMCP call_tool return shape in assertions.

## Evaluation notes (flywheel)

- Failure modes observed: call_tool returned tuple with content/result
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): Normalize call_tool results in tests.
