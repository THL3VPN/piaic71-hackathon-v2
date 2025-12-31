# specs.md

## Step 1: Conversation & Message Persistence

### Objective
Enable database-backed storage of chat conversations and messages so that future chatbot interactions can be fully stateless.

After this step:
- The backend can store chat conversations
- The backend can store chat messages
- Chat history can be retrieved after server restarts

This step does NOT include:
- Chat endpoint
- AI agents
- MCP tools
- Natural language processing
- Frontend chat UI

---

## Design Principles

- All chat state MUST be stored in the database
- The backend MUST remain stateless
- User identity MUST come from authentication context
- One user MUST NOT access another user’s conversations or messages

---

## In Scope
- Conversation database model
- Message database model
- Persistence logic for conversations and messages
- Ownership enforcement (user-scoped access)

## Out of Scope
- Chat API endpoint
- OpenAI Agents SDK
- MCP server/tools
- Task operations via chat
- Frontend changes

---

## Data Models

### Conversation
Represents a single chat session for a user.

Fields:
- id: integer, primary key
- user_id: string, derived from authenticated user
- created_at: datetime, server-generated
- updated_at: datetime, server-generated

Rules:
- A conversation belongs to exactly one user
- A user may have multiple conversations
- Users MUST NOT access conversations they do not own

---

### Message
Represents a single message in a conversation.

Fields:
- id: integer, primary key
- user_id: string, derived from authenticated user
- conversation_id: integer, foreign key to Conversation.id
- role: string, allowed values are "user" or "assistant"
- content: string, message text
- created_at: datetime, server-generated

Rules:
- Messages belong to one conversation
- Messages belong to one user
- Messages MUST be returned in chronological order
- Users MUST NOT access messages from conversations they do not own

---

## Persistence Operations (Internal Only)

### Create Conversation
Creates a new conversation for the authenticated user.

Inputs:
- user_id (from auth context)

Behavior:
- Inserts a new Conversation record
- Returns the created conversation id

---

### Add Message
Appends a message to an existing conversation.

Inputs:
- user_id (from auth context)
- conversation_id
- role ("user" or "assistant")
- content

Behavior:
- Verifies the conversation belongs to the user
- Inserts a new Message record
- Rejects if conversation does not belong to user

---

### Get Conversation History
Fetches message history for a conversation.

Inputs:
- user_id (from auth context)
- conversation_id
- limit (default 50)

Behavior:
- Verifies the conversation belongs to the user
- Returns messages ordered by created_at ascending
- Returns an error if conversation does not exist or is not owned by user

---

## Non-Functional Requirements

### Statelessness
- No conversation or message state may be stored in memory
- All required context must come from the database

### Security
- user_id MUST NOT be accepted from request parameters
- Ownership checks MUST be enforced for every operation

### Reliability
- Database operations must be transactional
- Timestamps must be generated server-side

---

## Acceptance Criteria

### Database
- [ ] Conversation table exists in the database
- [ ] Message table exists in the database
- [ ] Tables are deployed to Neon successfully

### Ownership
- [ ] A user can create conversations for themselves
- [ ] A user cannot access another user’s conversations
- [ ] A user cannot access another user’s messages

### History Retrieval
- [ ] Messages are returned in correct chronological order
- [ ] Message history persists after backend restart
- [ ] History retrieval respects the limit parameter

---

## Step Exit Criteria
Step 1 is complete when:
- Conversation and Message models are implemented
- Persistence logic is implemented and tested
- Chat history is fully DB-backed and stateless

/plan

Create: architecture sketch, interfaces, data model, error handling, requirements.
Decisions needing: list important choices with options and tradeoffs.
Testing strategy: unit + integration tests based on acceptance criteria.
Technical details:
- Use a simple, functional approach where it makes sense
- Follow TDD: write tests first, then implementation
- Organize code and tests according to your constitution rules

/sp.tasks

Break plan into small tasks (T001..), each ≤ 3 minutes, testable, reversible.
Add dependencies between tasks; group into phases; mark deliverables per task. Group tasks by operations and for each operation like add use TDD approach so RED Tests, Green Tests and Refactor. After each group we pause for human review and on approval commit to github.

Focus on:
- TDD approach (tests first for each operation)
- Small, step-by-step implementation
- Clear task dependencies
- Easy to undo changes

/sp.implement

Rules: tests first, smallest diff, keep public API stable within a phase.
After each task: run tests, update checklist, note deltas to spec if needed Mark completed tasks in tasks.md
