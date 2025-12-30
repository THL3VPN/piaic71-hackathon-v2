# Feature Specification: Chat Storage Persistence

**Feature Branch**: `008-chat-storage`  
**Created**: 2025-12-31  
**Status**: Draft  
**Input**: User description: "Enable database-backed storage of chat conversations and messages so that future chatbot interactions can be fully stateless. After this step: - The backend can store chat conversations - The backend can store chat messages - Chat history can be retrieved after server restarts This step does NOT include: - Chat endpoint - AI agents - MCP tools - Natural language processing - Frontend chat UI --- - All chat state MUST be stored in the database - The backend MUST remain stateless - User identity MUST come from authentication context - One user MUST NOT access another user’s conversations or messages --- - Conversation database model - Message database model - Persistence logic for conversations and messages - Ownership enforcement (user-scoped access) - Chat API endpoint - OpenAI Agents SDK - MCP server/tools - Task operations via chat - Frontend changes --- Represents a single chat session for a user. Fields: - id: integer, primary key - user_id: string, derived from authenticated user - created_at: datetime, server-generated - updated_at: datetime, server-generated Rules: - A conversation belongs to exactly one user - A user may have multiple conversations - Users MUST NOT access conversations they do not own --- Represents a single message in a conversation. Fields: - id: integer, primary key - user_id: string, derived from authenticated user - conversation_id: integer, foreign key to Conversation.id - role: string, allowed values are user or assistant - content: string, message text - created_at: datetime, server-generated Rules: - Messages belong to one conversation - Messages belong to one user - Messages MUST be returned in chronological order - Users MUST NOT access messages from conversations they do not own --- Creates a new conversation for the authenticated user. Inputs: - user_id (from auth context) Behavior: - Inserts a new Conversation record - Returns the created conversation id --- Appends a message to an existing conversation. Inputs: - user_id (from auth context) - conversation_id - role (user or assistant) - content Behavior: - Verifies the conversation belongs to the user - Inserts a new Message record - Rejects if conversation does not belong to user --- Fetches message history for a conversation. Inputs: - user_id (from auth context) - conversation_id - limit (default 50) Behavior: - Verifies the conversation belongs to the user - Returns messages ordered by created_at ascending - Returns an error if conversation does not exist or is not owned by user --- - No conversation or message state may be stored in memory - All required context must come from the database - user_id MUST NOT be accepted from request parameters - Ownership checks MUST be enforced for every operation - Database operations must be transactional - Timestamps must be generated server-side --- - [ ] Conversation table exists in the database - [ ] Message table exists in the database - [ ] Tables are deployed to Neon successfully - [ ] A user can create conversations for themselves - [ ] A user cannot access another user’s conversations - [ ] A user cannot access another user’s messages - [ ] Messages are returned in correct chronological order - [ ] Message history persists after backend restart - [ ] History retrieval respects the limit parameter --- Step 1 is complete when: - Conversation and Message models are implemented - Persistence logic is implemented and tested - Chat history is fully DB-backed and stateless"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a conversation (Priority: P1)

As an authenticated user, I start a new chat session and receive a new conversation identifier.

**Why this priority**: A conversation must exist before any messages can be stored or retrieved.

**Independent Test**: Create a conversation for a signed-in user and verify it can be referenced for later actions.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they request a new conversation, **Then** the system creates a conversation tied to that user and returns its identifier.
2. **Given** a different authenticated user, **When** they request a new conversation, **Then** the system creates a distinct conversation owned by that user.

---

### User Story 2 - Append a message (Priority: P2)

As an authenticated user, I add a message to an existing conversation I own.

**Why this priority**: Messages are the primary content of chat history.

**Independent Test**: Create a conversation, append a message, and verify the message is stored for that conversation.

**Acceptance Scenarios**:

1. **Given** a conversation owned by the user, **When** they append a message with a valid role and content, **Then** the message is stored and associated with that conversation.
2. **Given** a conversation owned by another user, **When** a different user attempts to append a message, **Then** the system denies the request.

---

### User Story 3 - Retrieve message history (Priority: P3)

As an authenticated user, I retrieve message history for my conversation in chronological order.

**Why this priority**: Users need their full chat history to persist across sessions and restarts.

**Independent Test**: Append multiple messages and retrieve history to verify ordering and limit handling.

**Acceptance Scenarios**:

1. **Given** a conversation with multiple messages, **When** the user requests history, **Then** messages are returned in chronological order.
2. **Given** a conversation with more than the default limit, **When** the user requests history without specifying a limit, **Then** only the most recent 50 messages are returned.

---

### Edge Cases

- What happens when a user requests history for a conversation that does not exist?
- How does the system handle an invalid message role outside of the allowed set?
- What happens when a user requests history with a limit of 0 or a negative number?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST persist conversation records with server-generated creation and update timestamps.
- **FR-002**: System MUST persist message records linked to a single conversation and user.
- **FR-003**: System MUST derive user identity from the authenticated context, not from request parameters.
- **FR-004**: System MUST prevent users from accessing or mutating conversations they do not own.
- **FR-005**: System MUST prevent users from accessing or mutating messages in conversations they do not own.
- **FR-006**: System MUST return conversation messages in chronological order by creation time.
- **FR-007**: System MUST support a history retrieval limit with a default of 50 messages.
- **FR-008**: System MUST reject message creation when the conversation is not owned by the user.
- **FR-009**: System MUST keep all chat state in persistent storage so history survives server restarts.
- **FR-010**: System MUST process persistence operations transactionally to avoid partial writes.

### Key Entities *(include if feature involves data)*

- **Conversation**: Represents a single chat session owned by one user, with creation and update timestamps.
- **Message**: Represents one entry in a conversation with role, content, timestamps, and ownership linkage.

### Assumptions

- Message roles are limited to "user" and "assistant".
- History retrieval uses a default limit of 50 when not specified.
- Ownership checks are required for all conversation and message operations.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of attempts to access another user’s conversations or messages are denied.
- **SC-002**: Users can retrieve chat history after a service restart with no loss of previously stored messages.
- **SC-003**: 95% of users can retrieve a conversation’s messages in the correct order on the first attempt.
- **SC-004**: Automated tests for conversation and message persistence run first and pass, with overall coverage maintained at or above 80%.
