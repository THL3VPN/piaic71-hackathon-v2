---
id: 0018
title: simplify-mcp-env
stage: green
date: 2026-01-01T22:44:38Z
surface: cli
model: gpt-5
feature: 015-mcp-server-extraction
branch: 015-mcp-server-extraction
user: user
command: misc
labels: [env, mcp]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/mcp_server/app.py
  - /home/aie/all_data/piaic71-hackathon-v2/scripts/bootstrap.sh
  - /home/aie/all_data/piaic71-hackathon-v2/.env
  - /home/aie/all_data/piaic71-hackathon-v2/.env.example
  - /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/quickstart.md
tests:
  - name: not run (env change)
    result: skip
---

## Prompt

instead of 3 variables MCP_HOST, MCP_PORT, MCP_SERVER_URL , just have a single variable MCP_SERVER_URL , host and port can be extracted from the complete url

## Response snapshot

Simplified MCP env to a single MCP_SERVER_URL and parsed host/port in the MCP server.

## Outcome

- ✅ Impact: MCP server derives bind host/port from MCP_SERVER_URL; env files simplified.
- 🧪 Tests: not run (env change)
- 📁 Files: mcp_server/app.py, scripts/bootstrap.sh, .env, .env.example, specs/015-mcp-server-extraction/quickstart.md
- 🔁 Next prompts: Optional full test run.
- 🧠 Reflection: Single source of truth for MCP address reduces config drift.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
