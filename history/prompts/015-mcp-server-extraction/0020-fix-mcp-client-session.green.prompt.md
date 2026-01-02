---
id: 0020
title: fix-mcp-client-session
stage: green
date: 2026-01-01T23:12:13Z
surface: cli
model: gpt-5
feature: 015-mcp-server-extraction
branch: 015-mcp-server-extraction
user: user
command: bugfix
labels: [mcp, session, bugfix]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/src/services/mcp_client.py
tests:
  - name: not run (runtime fix)
    result: skip
---

## Prompt

getting errors while running curl ...

## Response snapshot

Fixed MCP client session lifecycle to avoid cancel-scope errors on close.

## Outcome

- ✅ Impact: MCP SSE client no longer exits cancel scopes from the wrong task.
- 🧪 Tests: not run (runtime fix)
- 📁 Files: src/services/mcp_client.py
- 🔁 Next prompts: Re-test /api/chat with MCP running.
- 🧠 Reflection: Use async context managers for session lifecycle.

## Evaluation notes (flywheel)

- Failure modes observed: Cancel scope exit in async generator
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
