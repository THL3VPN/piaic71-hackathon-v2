# specs.md

## Step 1.5: Conversation History Retrieval (Messages GET)

### Objective
Complete Step 1 persistence by adding a read API to retrieve conversation message history from the database, enabling the stateless chat cycle in later steps.

This step adds:
- An authenticated endpoint to fetch messages for a conversation
- Ownership enforcement (user can only read their own conversation history)
- A safe default limit and ordering guarantee

This step does NOT add:
- Chat endpoint (/api/chat)
- AI agents
- MCP tools
- Frontend chat UI

---

## In Scope
- GET endpoint to retrieve messages for a conversation
- Ownership checks (conversation must belong to current user)
- Limit parameter (default 50)
- Chronological ordering (oldest to newest)

## Out of Scope
- Pagination cursors
- Full-text search
- Streaming
- Conversation listing endpoint

---

## Endpoint Specification

### GET /api/conversations/{conversation_id}/messages

Authentication:
- Required (Bearer token, same as other protected endpoints)

Path Parameters:
- conversation_id: integer (required)

Query Parameters:
- limit: integer (optional, default 50, max 200)

Response (200):
- Returns an array of message objects ordered by created_at ascending

Message Object Fields:
- id: integer
- conversation_id: integer
- role: string ("user" or "assistant")
- content: string
- created_at: datetime (ISO string)

Example Response:
    [
      {
        "id": 101,
        "conversation_id": 12,
        "role": "user",
        "content": "Add a task to buy groceries",
        "created_at": "2025-12-31T12:00:00Z"
      },
      {
        "id": 102,
        "conversation_id": 12,
        "role": "assistant",
        "content": "Sure — what items should I include?",
        "created_at": "2025-12-31T12:00:02Z"
      }
    ]

---

## Behavior Requirements

### Ownership Enforcement
- The backend MUST derive user identity from authentication context
- The backend MUST verify the conversation belongs to the authenticated user
- If the conversation does not exist for this user, return HTTP 404 (do not leak existence)

### Ordering
- Messages MUST be returned in chronological order by created_at ascending (oldest first)

### Limits
- Default limit is 50 messages
- If provided, limit MUST be clamped to a maximum of 200
- If limit is <= 0, return HTTP 422 or treat as default (implementation choice, must be consistent)

### Error Handling
- 401 Unauthorized: missing/invalid token
- 404 Not Found: conversation not found for this user
- 422 Unprocessable Entity: invalid query params (e.g., limit not an integer)

---

## Acceptance Criteria

Functional
- [ ] User can fetch messages for their own conversation
- [ ] Messages are ordered oldest to newest
- [ ] Default limit returns up to 50 messages
- [ ] Limit parameter returns up to the requested amount (clamped to max)

Security
- [ ] User cannot fetch another user’s conversation messages (returns 404)

Reliability
- [ ] Works after backend restart (data persists in Neon)

---

## Step Exit Criteria
Step 1.5 is complete when:
- The GET messages endpoint is deployed
- Ownership enforcement is verified
- Ordering and limit behaviors are verified
