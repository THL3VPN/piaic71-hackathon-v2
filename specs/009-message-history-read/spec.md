# Feature Specification: Message History Read

**Feature Branch**: `009-message-history-read`  
**Created**: 2025-01-02  
**Status**: Draft  
**Input**: User description: "Complete Step 1 persistence by adding a read API to retrieve conversation message history from the database, enabling the stateless chat cycle in later steps. This step adds: - An authenticated endpoint to fetch messages for a conversation - Ownership enforcement (user can only read their own conversation history) - A safe default limit and ordering guarantee This step does NOT add: - Chat endpoint (/api/chat) - AI agents - MCP tools - Frontend chat UI --- - GET endpoint to retrieve messages for a conversation - Ownership checks (conversation must belong to current user) - Limit parameter (default 50) - Chronological ordering (oldest to newest) - Pagination cursors - Full-text search - Streaming - Conversation listing endpoint --- Authentication: - Required (Bearer token, same as other protected endpoints) Path Parameters: - conversation_id: integer (required) Query Parameters: - limit: integer (optional, default 50, max 200) Response (200): - Returns an array of message objects ordered by created_at ascending Message Object Fields: - id: integer - conversation_id: integer - role: string (user or assistant) - content: string - created_at: datetime (ISO string) Example Response: [ { id: 101, conversation_id: 12, role: user, content: Add a task to buy groceries, created_at: 2025-12-31T12:00:00Z }, { id: 102, conversation_id: 12, role: assistant, content: Sure — what items should I include?, created_at: 2025-12-31T12:00:02Z } ] --- - The backend MUST derive user identity from authentication context - The backend MUST verify the conversation belongs to the authenticated user - If the conversation does not exist for this user, return HTTP 404 (do not leak existence) - Messages MUST be returned in chronological order by created_at ascending (oldest first) - Default limit is 50 messages - If provided, limit MUST be clamped to a maximum of 200 - If limit is <= 0, return HTTP 422 or treat as default (implementation choice, must be consistent) - 401 Unauthorized: missing/invalid token - 404 Not Found: conversation not found for this user - 422 Unprocessable Entity: invalid query params (e.g., limit not an integer) --- Functional - [ ] User can fetch messages for their own conversation - [ ] Messages are ordered oldest to newest - [ ] Default limit returns up to 50 messages - [ ] Limit parameter returns up to the requested amount (clamped to max) Security - [ ] User cannot fetch another user’s conversation messages (returns 404) Reliability - [ ] Works after backend restart (data persists in Neon) --- Step 1.5 is complete when: - The GET messages endpoint is deployed - Ownership enforcement is verified - Ordering and limit behaviors are verified"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Read conversation history (Priority: P1)

As an authenticated user, I can retrieve the messages for a specific conversation so I can continue a chat after reconnecting.

**Why this priority**: Restoring history is required to make stateless chat possible in later steps.

**Independent Test**: With a valid token and conversation ID, requesting history returns ordered messages for that conversation.

**Acceptance Scenarios**:

1. **Given** a user owns a conversation with messages, **When** they request its history without a limit, **Then** they receive up to 50 messages ordered oldest to newest.
2. **Given** a user owns a conversation with more than 50 messages, **When** they request history with a limit of 10, **Then** they receive 10 oldest messages in chronological order.
3. **Given** a user requests a conversation they do not own, **When** they request history, **Then** they receive a not found response.

---

### User Story 2 - Control history size (Priority: P2)

As an authenticated user, I can set a message limit when fetching history so I can reduce payload size for large conversations.

**Why this priority**: It provides control over payload size without adding pagination in this step.

**Independent Test**: Request history with limits below, above, and within allowed ranges and verify clamping and validation behavior.

**Acceptance Scenarios**:

1. **Given** a user requests history with limit 200, **When** the request is processed, **Then** at most 200 messages are returned.
2. **Given** a user requests history with limit 500, **When** the request is processed, **Then** no more than 200 messages are returned.
3. **Given** a user requests history with limit 0 or negative, **When** the request is processed, **Then** the request fails with a validation error.

---

### Edge Cases

- What happens when a conversation exists but has no messages?
- How does the system handle invalid or missing authentication tokens?
- What happens when the limit parameter is non-numeric?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow an authenticated user to retrieve messages for a specific conversation.
- **FR-002**: System MUST enforce that users can only read conversations they own.
- **FR-003**: System MUST return messages in chronological order (oldest first).
- **FR-004**: System MUST apply a default limit of 50 messages when no limit is provided.
- **FR-005**: System MUST clamp any provided limit to a maximum of 200 messages.
- **FR-006**: System MUST reject limits less than or equal to zero with a validation error.
- **FR-007**: System MUST return a not found response when the conversation does not exist for the authenticated user.
- **FR-008**: System MUST return a validation error for invalid limit values (non-integer).
- **FR-009**: System MUST return authentication errors when tokens are missing or invalid.

### Key Entities *(include if feature involves data)*

- **Conversation**: A single chat session owned by one user, identified by an ID.
- **Message**: A single entry in a conversation, including role, content, and timestamp.
- **Authenticated User**: The user identity derived from the authentication context for access checks.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of history requests from authenticated owners return ordered messages within the requested or default limits.
- **SC-002**: 100% of unauthorized or non-owner history requests return a not found response.
- **SC-003**: 100% of invalid limit requests return a validation error.
- **SC-004**: Automated tests for history retrieval are written before implementation and pass while maintaining overall coverage at or above 80%.

## Assumptions

- If limit is missing, the system uses the default of 50.
- Limits less than or equal to zero are treated as invalid and return a validation error.
