---
id: 0010
title: Execute T007 agent runtime unit
stage: red
date: 2025-12-31T20:45:35Z
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
  - path: tests/unit/test_agent_runtime.py
    reason: added failing agent runtime unit test
  - path: specs/012-ai-agent-integration/tasks.md
    reason: marked T007 complete

tests:
  - name: UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache uv run pytest -q tests/unit/test_agent_runtime.py
    reason: expected red (import error)
---

## Prompt

## User Input

```text
You are implementing Step 4 of a Todo AI Chatbot. Context: - Steps 1–3 are complete - Chat endpoint already exists with dummy logic - Task tools exist and are validated - Conversation and message persistence exists - Backend is FastAPI (async) Rules: - Do NOT modify DB models - Do NOT change auth logic - Do NOT bypass task tools - Chat must remain stateless - LLM provider must be configurable via env variables - No MCP server yet Task: - Add a model factory that selects provider (OpenAI or Gemini) via env vars - Build a single AI agent using OpenAI Agents SDK - Register task tools with the agent - Replace dummy assistant logic in POST /api/chat with agent execution - Capture tool calls and return them in the response
```

## Response snapshot

Added a unit test for agent runtime behavior, currently failing due to missing module.

## Outcome

- ✅ Impact: T007 red test added for agent runtime.
- 🧪 Tests: uv run pytest -q tests/unit/test_agent_runtime.py (import error as expected).
- 📁 Files: Added unit test and updated tasks checklist.
- 🔁 Next prompts: Continue with T008.
- 🧠 Reflection: Defined the runtime interface expectations before implementation.

## Evaluation notes (flywheel)

- Failure modes observed: import error for agent_runtime
- Graders run and results (PASS/FAIL): not-run
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
