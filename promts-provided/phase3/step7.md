# specs.md

## Step 7: Frontend Chat UI Integration (OpenAI ChatKit)

### Objective
Add a chatbot interface in the frontend so authenticated users can chat with the Todo AI assistant to manage their tasks using natural language.

After this step:
- A logged-in user can open a chat panel/page
- The UI sends messages to `POST /api/chat`
- The UI persists and reuses `conversation_id` for continuity
- The UI renders chat history (user + assistant messages)
- The UI optionally renders tool call traces for debugging

This step does NOT change:
- Backend stateless architecture
- Agent behavior rules
- MCP server/tool definitions

---

## Prerequisites
- Step 2: `/api/chat` exists and persists messages
- Step 4: Agent responds intelligently and returns `tool_calls`
- Step 6: MCP server is integrated (tools invoked via MCP)
- Auth is working in frontend (token stored and attached to API calls)

---

## In Scope
- Chat UI route/component using OpenAI ChatKit
- API client wrapper for `/api/chat` (and optional history endpoint)
- Conversation lifecycle management in UI (create or continue conversation)
- Rendering of messages and basic loading/error states
- Optional debug display for `tool_calls`

## Out of Scope
- Streaming responses (unless already supported and easy)
- Multi-chat conversation listing UI
- Message editing, reactions, attachments
- Advanced analytics/telemetry

---

## UX Requirements

### Entry Points
At least one of the following MUST be implemented:
- A "Chat" button on `/tasks` page that opens a chat panel/modal, OR
- A dedicated page route `/chat`

Recommended:
- Add a chat drawer/panel accessible from `/tasks` so task management + chat live together.

---

## Frontend State & Persistence

### Auth
- All chat requests MUST include `Authorization: Bearer <token>` header
- Token source: existing frontend auth storage (localStorage)

### conversation_id
- The frontend MUST store the active `conversation_id` locally (React state)
- The frontend SHOULD persist `conversation_id` across refreshes:
  - store in localStorage as `active_conversation_id` OR
  - store in URL query param `?conversation_id=...`
- When user logs out, conversation_id SHOULD be cleared

### Chat History
Two acceptable approaches:

Option A (recommended): Load history from backend
- On chat open, call:
  - `GET /api/conversations/{conversation_id}/messages?limit=50`
- Render returned messages

Option B (minimal): Render from local UI only
- Render messages added during the current session
- Still store messages server-side via `/api/chat`
- This is acceptable but less polished

---

## API Contract

### POST /api/chat
Request:
- conversation_id: optional integer
- message: required string

Response:
- conversation_id: integer
- response: string
- tool_calls: array

UI behavior:
- If no conversation_id exists, send only message; save returned conversation_id
- Append user message immediately (optimistic)
- Append assistant response after API returns
- If API fails, show retry and do not lose the user message

---

## UI Behavior Rules

### Sending a Message
1) User types message and hits send
2) UI appends user's message immediately
3) UI shows loading indicator for assistant
4) UI calls `/api/chat`
5) UI appends assistant response
6) UI stores/updates conversation_id
7) If tool_calls are returned:
   - store them in message metadata
   - optionally show in a collapsible "Details" area

### Error Handling
- If request fails:
  - show an error toast or inline error
  - allow retry
  - keep the typed message in the UI

### Empty State
- If no messages yet:
  - show a short hint list (examples from Natural Language Commands)

---

## UI Components (Suggested)

### Message List
- Render messages with:
  - role (user/assistant)
  - content
  - timestamp (optional)
- Auto-scroll to bottom on new messages

### Composer
- Text input + Send button
- Disable send while request in-flight (or allow queueing if simple)

### Tool Call Debug (Optional)
- A toggle "Show details"
- For each assistant message show:
  - tool name(s)
  - arguments
  - result summary

---

## Acceptance Criteria

Functional
- [ ] Logged-in user can open chat UI
- [ ] User can send a message and see assistant reply
- [ ] conversation_id is created on first message and reused thereafter
- [ ] Refreshing the page does not lose the active conversation (if persistence implemented)
- [ ] Messages render in correct chronological order

Integration
- [ ] `/api/chat` is called with Bearer token
- [ ] Backend returns conversation_id and UI uses it
- [ ] tool_calls returned by backend are captured (display optional)

Quality
- [ ] Loading state is visible while waiting
- [ ] Error state is handled gracefully with retry

---

## Step Exit Criteria
Step 7 is complete when:
- Chat UI is available to authenticated users
- Messages round-trip via `/api/chat` successfully
- conversation_id continuity works
- Basic UX states (loading/error/empty) are implemented
