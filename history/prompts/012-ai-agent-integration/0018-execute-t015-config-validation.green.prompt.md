---
id: 0018
title: Execute T015 config validation
stage: green
date: 2025-12-31T21:00:15Z
surface: codex-cli
model: gpt-5
feature: 012-ai-agent-integration
branch: 012-ai-agent-integration
user: user
command: /sp.execute
labels: [green]
links:
  spec: specs/012-ai-agent-integration/spec.md
  ticket: none
  adr: none
  pr: none
files:
  - path: src/services/chat_provider.py
    reason: add validation and error type
  - path: specs/012-ai-agent-integration/tasks.md
    reason: marked T015 complete
tests:
  - name: UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache uv run pytest -q tests/unit/test_chat_provider.py
    reason: verify config validation
---

## Prompt

## User Input

```text
You are implementing Step 4 of a Todo AI Chatbot. Context: - Steps 1–3 are complete - Chat endpoint already exists with dummy logic - Task tools exist and are validated - Conversation and message persistence exists - Backend is FastAPI (async) Rules: - Do NOT modify DB models - Do NOT change auth logic - Do NOT bypass task tools - Chat must remain stateless - LLM provider must be configurable via env variables - No MCP server yet Task: - Add a model factory that selects provider (OpenAI or Gemini) via env vars - Build a single AI agent using OpenAI Agents SDK - Register task tools with the agent - Replace dummy assistant logic in POST /api/chat with agent execution - Capture tool calls and return them in the response
```

## Response snapshot

Implemented provider config validation and error type in chat_provider.

## Outcome

- ✅ Impact: T015 completed; config validation tests now pass.
- 🧪 Tests: uv run pytest -q tests/unit/test_chat_provider.py.
- 📁 Files: Updated `src/services/chat_provider.py` and tasks checklist.
- 🔁 Next prompts: Refactor model factory wiring (T016).
- 🧠 Reflection: Validation aligns provider requirements with test cases.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): not-run
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): normalize provider usage in model factory
