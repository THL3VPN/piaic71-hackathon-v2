---
id: 0008
title: Execute T005 agent chat contract
stage: red
date: 2025-12-31T20:42:44Z
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
  - path: tests/contract/test_agent_chat_contract.py
    reason: added failing agent chat contract test
  - path: specs/012-ai-agent-integration/tasks.md
    reason: marked T005 complete

tests:
  - name: UV_CACHE_DIR=/home/aie/all_data/piaic71-hackathon-v2/.uv-cache uv run pytest -q tests/contract/test_agent_chat_contract.py
    reason: expected red; command timed out
---

## Prompt

## User Input

```text
You are implementing Step 4 of a Todo AI Chatbot. Context: - Steps 1–3 are complete - Chat endpoint already exists with dummy logic - Task tools exist and are validated - Conversation and message persistence exists - Backend is FastAPI (async) Rules: - Do NOT modify DB models - Do NOT change auth logic - Do NOT bypass task tools - Chat must remain stateless - LLM provider must be configurable via env variables - No MCP server yet Task: - Add a model factory that selects provider (OpenAI or Gemini) via env vars - Build a single AI agent using OpenAI Agents SDK - Register task tools with the agent - Replace dummy assistant logic in POST /api/chat with agent execution - Capture tool calls and return them in the response
```

## Response snapshot

Added a contract test asserting the chat response includes tool call details when the agent performs a task operation.

## Outcome

- ✅ Impact: T005 red test added for agent chat contract.
- 🧪 Tests: uv run pytest -q tests/contract/test_agent_chat_contract.py (timed out).
- 📁 Files: Added contract test and updated tasks checklist.
- 🔁 Next prompts: Continue with T006.
- 🧠 Reflection: Locked response shape expectations before implementing agent logic.

## Evaluation notes (flywheel)

- Failure modes observed: pytest run timed out
- Graders run and results (PASS/FAIL): not-run
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
