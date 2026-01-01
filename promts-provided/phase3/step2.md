# specs.md

## Step 2: Stateless Chat Endpoint (Dummy Assistant)

### Objective
Introduce a stateless chat API endpoint that persists conversation state to the database and returns a dummy assistant response.

This step proves the full stateless request cycle:
- Fetch history from DB
- Store user message
- Generate assistant response (dummy, no AI)
- Store assistant message
- Return conversation_id + response

This step does NOT include:
- OpenAI Agents SDK
- MCP server/tools
- Natural language command execution
- Task operations via chat
- Frontend chat UI (optional later)

---

## Prerequisites
- Step 1 (Conversation + Message persistence) is complete
- Step 1.5 (GET conversation messages) is complete
- Authentication identifies the current user (server-side)
- Existing `/health` continues to validate Neon connectivity

---

## In Scope
- New chat endpoint: POST /api/chat
- Stateless request cycle using database persistence
- Conversation creation when conversation_id is not provided
- Message persistence for both user and assistant roles
- Response payload includes conversation_id and tool_calls (empty for this step)

## Out of Scope
- AI agent logic
- MCP server/tools and tool invocations
- Streaming responses
- Frontend chat UI
- Advanced conversation management (listing, deleting conversations)

---

## Endpoint Specification

### POST /api/chat

Authentication:
- Required (Bearer token)

Request Body:
- conversation_id: integer (optional)
- message: string (required)

Request Example:
    {
      "conversation_id": 12,
      "message": "Add a task to buy groceries"
    }

Behavior:
1) Derive user_id from authentication context (server-side)
2) If conversation_id is missing:
   - Create a new Conversation for this user
   - Use the new conversation id
3) If conversation_id is provided:
   - Verify the conversation belongs to the authenticated user
   - If not found for this user, return HTTP 404
4) Fetch conversation message history from DB (up to limit 50)
5) Store the incoming user message to DB as:
   - role = "user"
   - content = request.message
6) Generate a dummy assistant response (no AI):
   - Response content MUST be deterministic and safe
   - Suggested format:
     - "OK (dummy): <echo of message>"
   - The dummy response MUST NOT call any tools
7) Store assistant response to DB as:
   - role = "assistant"
   - content = dummy response
8) Return the response payload to the client

Response (200):
- conversation_id: integer
- response: string
- tool_calls: array (MUST be empty in Step 2)

Response Example:
    {
      "conversation_id": 12,
      "response": "OK (dummy): Add a task to buy groceries",
      "tool_calls": []
    }

---

## Data Persistence Requirements

### Conversation Ownership
- user_id MUST be derived from auth context
- conversation_id MUST be validated as owned by the user
- If not owned or not found, return HTTP 404

### Message Storage
- The user message MUST be stored before generating the assistant response
- The assistant message MUST be stored after generation
- Both messages MUST store:
  - user_id (from auth)
  - conversation_id
  - role
  - content
  - created_at (server-generated)

### History Retrieval (for statelessness)
- The server MUST fetch prior messages for the conversation from DB each request
- The server MUST NOT store conversation state in memory between requests
- History limit default: 50 messages

---

## Error Handling

- 401 Unauthorized:
  - Missing or invalid token
- 404 Not Found:
  - conversation_id provided but not found for this user
- 422 Unprocessable Entity:
  - Missing required fields (message)
  - Invalid types (conversation_id not int, message not string)

---

## Non-Functional Requirements

### Statelessness
- No in-memory chat state
- Each request reconstructs context from DB

### Safety
- Dummy response must not contain secrets
- Dummy response must not perform task operations
- tool_calls must be an empty list

### Observability (Recommended)
- Log request_id, conversation_id, and message counts fetched/stored

---

## Acceptance Criteria

### Create New Conversation
- [ ] POST /api/chat without conversation_id creates a new conversation
- [ ] Response includes a valid conversation_id
- [ ] User message + assistant message are stored in DB

### Continue Existing Conversation
- [ ] POST /api/chat with conversation_id appends two new messages
- [ ] History is fetched from DB each time (stateless)

### Ownership Enforcement
- [ ] User cannot use another user’s conversation_id (returns 404)

### Response Contract
- [ ] response field contains dummy assistant text
- [ ] tool_calls is always an empty array

---

## Step Exit Criteria
Step 2 is complete when:
- POST /api/chat is implemented and deployed locally
- New conversation creation works
- Existing conversation continuation works
- Messages are persisted correctly
- Ownership checks are enforced
- tool_calls is returned as an empty list
