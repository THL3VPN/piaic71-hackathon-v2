---
id: 0011
title: Execute T008 model factory
stage: green
date: 2025-12-31T20:47:02Z
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
  - path: src/services/chat_model_factory.py
    reason: implemented provider model factory selection
  - path: specs/012-ai-agent-integration/tasks.md
    reason: marked T008 complete

tests:
  - name: UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache uv run pytest -q tests/unit/test_agent_runtime.py
    reason: expected red (agent_runtime import missing)
---

## Prompt

## User Input

```text
You are implementing Step 4 of a Todo AI Chatbot. Context: - Steps 1–3 are complete - Chat endpoint already exists with dummy logic - Task tools exist and are validated - Conversation and message persistence exists - Backend is FastAPI (async) Rules: - Do NOT modify DB models - Do NOT change auth logic - Do NOT bypass task tools - Chat must remain stateless - LLM provider must be configurable via env variables - No MCP server yet Task: - Add a model factory that selects provider (OpenAI or Gemini) via env vars - Build a single AI agent using OpenAI Agents SDK - Register task tools with the agent - Replace dummy assistant logic in POST /api/chat with agent execution - Capture tool calls and return them in the response
```

## Response snapshot

Implemented provider-aware model factory selection for chat models.

## Outcome

- ✅ Impact: T008 completed with model factory selection.
- 🧪 Tests: uv run pytest -q tests/unit/test_agent_runtime.py (import error expected).
- 📁 Files: Updated model factory and tasks checklist.
- 🔁 Next prompts: Continue with T009.
- 🧠 Reflection: Factory now enforces provider selection and key presence.

## Evaluation notes (flywheel)

- Failure modes observed: agent_runtime import error
- Graders run and results (PASS/FAIL): not-run
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
