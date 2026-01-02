# specs.md

## Step 6: MCP Server Extraction (Official MCP SDK)

### Objective
Extract the task tools from the backend into a dedicated MCP server built with the Official MCP SDK. The AI agent must invoke task operations via MCP tools instead of calling local Python tool functions.

After this step:
- Task operations are exposed as MCP tools (stateless, DB-backed)
- The AI agent uses MCP tools to manage tasks
- The backend remains stateless and continues to persist chat history to DB
- Behavior remains identical to Step 5 (only architecture changes)

---

## Prerequisites
- Step 3: Task tools implemented and validated (local tool layer)
- Step 4: AI agent integrated and working via `/api/chat`
- Step 5: Natural language behavior validated

---

## In Scope
- New MCP server service using the Official MCP SDK
- MCP tools:
  - add_task
  - list_tasks
  - complete_task
  - delete_task
  - update_task
- Stateless tool implementations that operate on the Neon DB
- Agent/tool invocation path updated to call MCP tools
- Tool call logging returned as `tool_calls` in `/api/chat`

## Out of Scope
- Frontend chat UI changes
- Streaming responses
- Multi-agent orchestration
- Advanced tool discovery or permissions
- Non-task tools

---

## Architecture

### Services
- Backend (FastAPI):
  - Handles auth
  - Persists conversations and messages
  - Runs agent orchestration
  - Calls MCP tools for task operations

- MCP Server (Official MCP SDK):
  - Exposes task operations as tools
  - Stateless: no in-memory state
  - Uses DB (Neon) as source of truth

---

## Environment Variables

Backend:
- `MCP_SERVER_URL` (e.g. http://localhost:9000 or deployed URL)
- `CHAT_MODEL_PROVIDER`, `CHAT_MODEL_NAME`
- Provider key: `OPENAI_API_KEY` or `GEMINI_API_KEY`
- `CHAT_HISTORY_LIMIT` (optional)

MCP Server:
- `DATABASE_URL` (required)
- Any DB-related settings used by the repo today
- (Optional) `LOG_LEVEL`

No secrets may be hardcoded.

---

## MCP Tool Specifications (Must Match Hackathon Spec)

### Tool: add_task
Purpose: Create a new task

Parameters:
- user_id: string (required)
- title: string (required)
- description: string (optional)

Returns:
- task_id: integer
- status: string ("created")
- title: string

Example Input:
    {"user_id":"ziakhan","title":"Buy groceries","description":"Milk, eggs, bread"}

Example Output:
    {"task_id":5,"status":"created","title":"Buy groceries"}

---

### Tool: list_tasks
Purpose: Retrieve tasks

Parameters:
- user_id: string (required)
- status: string (optional: "all", "pending", "completed")

Returns:
- Array of task objects:
  - id: integer
  - title: string
  - completed: boolean

Example Input:
    {"user_id":"ziakhan","status":"pending"}

Example Output:
    [{"id":1,"title":"Buy groceries","completed":false}]

---

### Tool: complete_task
Purpose: Mark a task as complete

Parameters:
- user_id: string (required)
- task_id: integer (required)

Returns:
- task_id: integer
- status: string ("completed")
- title: string

---

### Tool: delete_task
Purpose: Delete a task

Parameters:
- user_id: string (required)
- task_id: integer (required)

Returns:
- task_id: integer
- status: string ("deleted")
- title: string

---

### Tool: update_task
Purpose: Update task title/description

Parameters:
- user_id: string (required)
- task_id: integer (required)
- title: string (optional)
- description: string (optional)

Returns:
- task_id: integer
- status: string ("updated")
- title: string

---

## Statelessness & Ownership Requirements

### MCP Server Statelessness
- MCP server MUST NOT store state in memory between requests
- All state MUST be persisted in the database

### Ownership Enforcement
- MCP tools MUST only operate on tasks belonging to `user_id`
- If a task_id does not belong to `user_id`, tool MUST return a not-found style error (do not leak existence)

---

## Backend Integration Requirements

### Tool Invocation Path
- The agent MUST call MCP tools rather than local task tool functions
- The backend MUST pass the authenticated `user_id` to MCP tools
- The backend MUST capture tool calls and include them in the `/api/chat` response

### No Behavior Regression
- Natural language behavior from Step 5 MUST remain correct
- Chat persistence rules remain unchanged
- Only the tool execution path changes

---

## Observability (Recommended)
- Log MCP tool name + duration per call
- Include conversation_id in logs
- Include tool calls in response payload

---

## Acceptance Criteria

### MCP Server
- [ ] MCP server starts successfully using Official MCP SDK
- [ ] All five tools are discoverable and invocable
- [ ] Tools correctly read/write tasks in Neon DB
- [ ] Tools enforce user ownership

### Backend + Agent
- [ ] `/api/chat` continues to work with same behavior as Step 5
- [ ] tool_calls in response reflect MCP tool invocations
- [ ] No local task tool functions are called by the agent path

### Regression
- [ ] Step 5 validation commands still pass unchanged
- [ ] Backend remains stateless

---

## Step Exit Criteria
Step 6 is complete when:
- MCP server is deployed/runnable
- Backend calls MCP tools for all task operations
- Step 5 natural language validation passes with MCP-backed tools
- No behavior changes observed compared to Step 5