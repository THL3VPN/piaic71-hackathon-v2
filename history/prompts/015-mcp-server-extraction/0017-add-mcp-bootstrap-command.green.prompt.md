---
id: 0017
title: add-mcp-bootstrap-command
stage: green
date: 2026-01-01T22:41:39Z
surface: cli
model: gpt-5
feature: 015-mcp-server-extraction
branch: 015-mcp-server-extraction
user: user
command: misc
labels: [bootstrap, mcp, env]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/015-mcp-server-extraction/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/scripts/bootstrap.sh
  - /home/aie/all_data/piaic71-hackathon-v2/mcp_server/app.py
  - /home/aie/all_data/piaic71-hackathon-v2/.env
  - /home/aie/all_data/piaic71-hackathon-v2/.env.example
tests:
  - name: not run (bootstrap change)
    result: skip
---

## Prompt

okie do it

## Response snapshot

Added an MCP bootstrap command and MCP host/port env defaults; MCP server now runs SSE on configured port.

## Outcome

- ✅ Impact: MCP server can be launched via `./scripts/bootstrap.sh mcp` with env defaults.
- 🧪 Tests: not run (bootstrap change)
- 📁 Files: scripts/bootstrap.sh, mcp_server/app.py, .env, .env.example
- 🔁 Next prompts: Optionally run full suite or manual quickstart.
- 🧠 Reflection: Keep MCP server on a separate port to avoid backend conflicts.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
