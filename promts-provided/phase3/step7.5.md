# specs.md

## Step 7.5: Floating Chat Widget UX (Bottom-Right Support Style)

### Objective
Replace any separate chat page/tab experience with a modern floating chat widget (bottom-right) that provides an excellent, frictionless, user-friendly chat experience for managing todos via natural language.

This step is UI/UX-focused and must NOT change core backend behavior.
The existing `/api/chat` contract, conversation persistence, and tool-based task execution remain unchanged.

---

## Prerequisites
- Step 7 is complete: frontend can send messages to `POST /api/chat`, reuse `conversation_id`, and render chat history.
- Authentication works; token is stored in localStorage and sent as Bearer token.
- Backend Step 4/5/6 behavior is stable (agent + tools/MCP).

---

## In Scope
- Floating bottom-right chat launcher button
- Popup chat panel UI (support-style widget)
- Highly user-friendly chat interaction UX (loading, errors, confirmations)
- Conversation continuity (persist conversation_id, reload history)
- Optional: lightweight tone improvements via agent instructions (no behavior change)

## Out of Scope
- Separate `/chat` route or dedicated chat tab
- Backend endpoint changes
- Streaming responses (optional only if already available)
- Multi-conversation management UI (list/switch sessions)
- Admin/support multi-user chat features

---

## UX Requirements

### 1) Chat Launcher (Bottom-Right Widget Button)
- A fixed-position circular button MUST appear at bottom-right on authenticated pages (minimum: `/tasks`).
- Button MUST be visible above page content and not blocked by other UI.
- Button MUST toggle chat visibility (open/close).
- Button MUST have:
  - chat icon (e.g., 💬)
  - accessible label for screen readers (e.g., "Open chat")

States:
- Closed: only the button is visible.
- Open: a popup panel appears above the button; button remains visible or becomes a close button.

---

### 2) Popup Chat Panel
When opened, the chat widget MUST display a popup panel that resembles common website support chat.

Layout (recommended defaults):
- Width: 320–420px (responsive)
- Height: 420–600px (responsive)
- Rounded corners + subtle shadow
- Fixed bottom-right placement above the launcher button

Panel Sections:
1. Header:
   - Title: "Todo Assistant"
   - Close button (X)
2. Body:
   - Scrollable message list
   - Auto-scroll to most recent message
3. Composer:
   - Text input
   - Send button
   - Enter-to-send supported
   - Disabled while request is in-flight (or allow queueing if already implemented)

Widget behavior:
- Closing the widget MUST NOT delete conversation state or messages.
- Reopening MUST show the same message history and continue the same conversation.

---

### 3) Chat Experience Quality (User Friendly)
The chat experience MUST feel fast, friendly, and easy.

Requirements:
- Optimistic UI:
  - User message appears instantly on send.
- Loading state:
  - Show assistant typing indicator while waiting for `/api/chat`.
- Error state:
  - Friendly error message:
    - "Something went wrong. Try again?"
  - Provide a Retry action (resend last message).
- Message rendering:
  - Clear distinction between user vs assistant messages (bubble alignment).
  - Minimal, clean styling (good spacing, readable text).
- Empty state:
  - When no messages exist, show 3–6 example prompts:
    - "Add a task to buy groceries"
    - "Show my pending tasks"
    - "Mark task 3 as complete"
    - "Delete the meeting task"
    - "Change task 1 to 'Call mom tonight'"

Accessibility:
- Focus moves to input when widget opens.
- Escape key closes widget (recommended).
- Visible focus rings for keyboard navigation.

---

### 4) Conversation Continuity (No Tab Required)
- The app MUST NOT require a separate chat tab or route for chat usage.
- The widget MUST be available from the primary task page experience.

Conversation ID handling:
- The UI MUST store `conversation_id` after first `/api/chat` call.
- The UI MUST persist conversation_id in localStorage:
  - key: `active_conversation_id`
- On widget open:
  - If `active_conversation_id` exists, load history via:
    - `GET /api/conversations/{conversation_id}/messages?limit=50`
  - If not, start fresh when user sends first message.

Logout behavior:
- On logout (or missing token), the widget MUST:
  - hide or become disabled
  - clear `active_conversation_id`

---

### 5) Backend Interaction Contract (Unchanged)
The widget MUST call existing endpoints exactly:

#### POST /api/chat
Request:
- { "message": string } for first message OR
- { "conversation_id": number, "message": string } for subsequent messages

Response:
- { "conversation_id": number, "response": string, "tool_calls": array }

Rules:
- All requests MUST include:
  - Authorization: Bearer <token>

#### GET /api/conversations/{conversation_id}/messages?limit=50
- Used to load history on widget open (recommended)

---

### 6) Friendly Answers (Tone Requirement)
The assistant responses should be user friendly.

Frontend:
- Render confirmations clearly, optionally with subtle emojis (✅ 📝)
- Keep messages readable and not overly technical

Backend (optional, minimal change allowed):
- If needed, adjust agent system instructions to emphasize:
  - "Be friendly, concise, and helpful."
  - "Confirm actions in simple language."
- No functional behavior change is allowed (tools and logic remain same).

---

## Tool Call Debug Display (Optional)
For development/demo, the widget MAY provide a collapsible section per assistant message:
- "Details"
- shows tool_calls name + args + result summary

This MUST be off by default in production UI unless explicitly enabled.

---

## Acceptance Criteria
The step is complete when:

Widget UX
- [ ] Chat button is fixed bottom-right on `/tasks`
- [ ] Clicking opens a popup chat panel
- [ ] Closing and reopening preserves conversation and history
- [ ] Input is focused on open; Enter sends; loading indicator visible

Chat Functionality
- [ ] Messages successfully round-trip via `POST /api/chat`
- [ ] conversation_id is persisted and reused (localStorage)
- [ ] History loads correctly from GET messages endpoint
- [ ] Errors are user-friendly and retryable

No Separate Tab
- [ ] No dedicated chat tab or route is required to use chat

User Experience
- [ ] The chat feels simple and pleasant to use
- [ ] Assistant responses appear friendly and clear

---

## Step Exit Criteria
Step 7.5 is complete when:
- Floating widget replaces any chat tab/page dependency
- Conversation continuity works across closes and refreshes
- UX states (empty/loading/error) are implemented
- All existing backend behavior remains unchanged
