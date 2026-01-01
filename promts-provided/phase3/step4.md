# specs.md

## Step 4: AI Agent Integration (Model-Agnostic, Env-Driven)

### Objective
Integrate an AI agent into the chat flow that understands natural language and performs task operations via the Step 3 tool layer, while keeping the LLM provider and API key fully configurable via environment variables.

This step enables intelligent chat behavior today and allows seamless switching between GPT-4, Gemini, or any OpenAI-compatible model in the future without code rewrites.

---

## Design Goals

- LLM provider MUST be swappable via environment variables
- Agent orchestration MUST be independent of the model vendor
- All task mutations MUST go through tools
- Chat flow MUST remain stateless and DB-backed

---

## Prerequisites
- Step 1: Conversation & Message persistence completed
- Step 1.5: Conversation history retrieval completed
- Step 2: Stateless chat endpoint (dummy assistant) completed
- Step 3: Task tools layer completed and validated

---

## In Scope
- OpenAI Agents SDK integration
- Model factory abstraction (env-driven)
- Single general-purpose AI agent
- Tool binding using Step 3 tools
- Replacement of dummy assistant logic in `/api/chat`
- Tool call capture and persistence

## Out of Scope
- MCP server
- Multiple agents or skills
- Frontend chat UI
- Streaming responses

---

## Environment Variables

The backend MUST support the following variables:

Required:
- `CHAT_MODEL_PROVIDER` (enum: `openai`, `gemini`)
- `CHAT_MODEL_NAME` (e.g. `gpt-4o-mini`, `gemini-2.0-flash`)

Provider-Specific:
- `OPENAI_API_KEY` (required if provider = `openai`)
- `GEMINI_API_KEY` (required if provider = `gemini`)

Optional:
- `CHAT_HISTORY_LIMIT` (default: 50)

No other part of the codebase may reference model names or API keys directly.

---

## Model Factory Specification

A single model factory MUST exist.

Responsibilities:
- Read env variables
- Construct the correct OpenAI-compatible client
- Return an `OpenAIChatCompletionsModel`

Rules:
- Only this factory may import `AsyncOpenAI`
- All agents must receive their model from this factory

---

## Agent Definition

### Agent Type
- Single agent
- Stateless per request
- No memory outside DB history

### System Instructions (Behavior Contract)
The agent MUST:

- Use tools for all task mutations
- Never assume task state without tool results
- Confirm actions in a friendly tone
- Handle ambiguity by asking follow-up questions
- Handle task-not-found gracefully

The agent MUST NOT:

- Modify tasks directly
- Invent task IDs
- Access the database
- Depend on model-specific behavior

---

## Tool Integration

### Registered Tools
The agent MUST be registered with:
- add_task
- list_tasks
- complete_task
- delete_task
- update_task

Tool Invocation Rules:
- Tools MUST be deterministic
- Tools MUST enforce ownership via `user_id`
- The agent MUST rely on tool results for responses

---

## Chat Endpoint Behavior

### POST /api/chat

Request Body:
- conversation_id: integer (optional)
- message: string (required)

Request Flow:
1) Derive `user_id` from authentication context
2) Create or validate conversation_id
3) Fetch conversation history from DB (limit from env)
4) Persist user message
5) Run AI agent with:
   - system instructions
   - conversation history
   - current user message
   - registered tools
6) Execute any tool calls
7) Persist assistant response
8) Return response payload

Response Body:
- conversation_id: integer
- response: string
- tool_calls: array of:
  - name
  - arguments
  - result

---

## Statelessness Guarantee

- No in-memory agent state between requests
- Conversation context reconstructed from DB every time
- Backend instances are horizontally scalable

---

## Error Handling

- Tool errors MUST be translated into friendly assistant messages
- Model/API errors MUST return a safe fallback message
- HTTP errors (401, 404, 422) remain unchanged

---

## Acceptance Criteria

Functional:
- [ ] Agent performs correct task operations via chat
- [ ] Tools are invoked for task mutations
- [ ] Assistant responses confirm actions

Configurability:
- [ ] Switching GPT-4 → Gemini requires only env changes
- [ ] No code changes required to swap providers

Persistence:
- [ ] User and assistant messages are stored
- [ ] Tool calls are included in responses

Security:
- [ ] Agent operates only on authenticated user’s tasks
- [ ] Cross-user access is impossible

---

## Step Exit Criteria
Step 4 is complete when:
- AI agent replaces dummy logic
- Task tools are invoked via agent
- Chat remains stateless and DB-backed
- Model provider can be swapped via env variables
- No MCP server is involved yet
