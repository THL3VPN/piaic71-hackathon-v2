---
id: 0021
title: Execute T018 agent history tests
stage: red
date: 2025-12-31T21:23:06Z
surface: codex-cli
model: gpt-5
feature: 012-ai-agent-integration
branch: 012-ai-agent-integration
user: user
command: /sp.execute
labels: [red]
links:
  spec: specs/012-ai-agent-integration/spec.md
  ticket: none
  adr: none
  pr: none
files:
  - path: tests/integration/test_agent_chat_history.py
    reason: add history reconstruction test
  - path: src/services/chat_service.py
    reason: fix tool call payload formatting
  - path: specs/012-ai-agent-integration/tasks.md
    reason: marked T018 complete
tests:
  - name: UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache uv run pytest -q tests/integration/test_agent_chat_history.py
    reason: confirm failing history test
---

## Prompt

## User Input

```text
You are implementing Step 4 of a Todo AI Chatbot. Context: - Steps 1–3 are complete - Chat endpoint already exists with dummy logic - Task tools exist and are validated - Conversation and message persistence exists - Backend is FastAPI (async) Rules: - Do NOT modify DB models - Do NOT change auth logic - Do NOT bypass task tools - Chat must remain stateless - LLM provider must be configurable via env variables - No MCP server yet Task: - Add a model factory that selects provider (OpenAI or Gemini) via env vars - Build a single AI agent using OpenAI Agents SDK - Register task tools with the agent - Replace dummy assistant logic in POST /api/chat with agent execution - Capture tool calls and return them in the response
```

## Response snapshot

Added integration test for history limit and fixed tool call payload formatting.

## Outcome

- ✅ Impact: T018 completed with a failing history test.
- 🧪 Tests: uv run pytest -q tests/integration/test_agent_chat_history.py (timeout).
- 📁 Files: Added history test, fixed tool call payload format, updated tasks checklist.
- 🔁 Next prompts: Implement history limit in agent runtime (T019).
- 🧠 Reflection: Need to resolve aiosqlite test timeout before relying on integration runs.

## Evaluation notes (flywheel)

- Failure modes observed: aiosqlite operations hang during tests
- Graders run and results (PASS/FAIL): not-run
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): avoid DB I/O in history test or adjust env
