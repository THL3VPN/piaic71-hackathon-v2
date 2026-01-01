---
id: 0017
title: Execute T014 config validation tests
stage: red
date: 2025-12-31T20:59:13Z
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
  - path: tests/unit/test_chat_provider.py
    reason: add failing validation tests
  - path: specs/012-ai-agent-integration/tasks.md
    reason: marked T014 complete
tests:
  - name: UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache uv run pytest -q tests/unit/test_chat_provider.py
    reason: confirm failing tests
---

## Prompt

## User Input

```text
You are implementing Step 4 of a Todo AI Chatbot. Context: - Steps 1–3 are complete - Chat endpoint already exists with dummy logic - Task tools exist and are validated - Conversation and message persistence exists - Backend is FastAPI (async) Rules: - Do NOT modify DB models - Do NOT change auth logic - Do NOT bypass task tools - Chat must remain stateless - LLM provider must be configurable via env variables - No MCP server yet Task: - Add a model factory that selects provider (OpenAI or Gemini) via env vars - Build a single AI agent using OpenAI Agents SDK - Register task tools with the agent - Replace dummy assistant logic in POST /api/chat with agent execution - Capture tool calls and return them in the response
```

## Response snapshot

Added red tests covering provider config validation scenarios.

## Outcome

- ✅ Impact: T014 completed with failing tests.
- 🧪 Tests: uv run pytest -q tests/unit/test_chat_provider.py (fails: ProviderConfigError missing).
- 📁 Files: Added `tests/unit/test_chat_provider.py`, updated task checklist.
- 🔁 Next prompts: Implement config validation in chat_provider.
- 🧠 Reflection: Tests define required validation errors and success cases.

## Evaluation notes (flywheel)

- Failure modes observed: ImportError due to missing validation symbols
- Graders run and results (PASS/FAIL): not-run
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): add ProviderConfigError + validate_provider_settings
