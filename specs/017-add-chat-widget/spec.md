# Feature Specification: Floating Chat Widget UX

**Feature Branch**: `017-add-chat-widget`  
**Created**: 2026-01-02  
**Status**: Draft  
**Input**: User description: "# specs.md

## Step 7.5: Floating Chat Widget UX (Bottom-Right Support Style)

### Objective
Replace any separate chat page/tab experience with a modern floating chat widget (bottom-right) that provides an excellent, frictionless, user-friendly chat experience for managing todos via natural language.

This step is UI/UX-focused and must NOT change core backend behavior.
The existing chat contract, conversation persistence, and tool-based task execution remain unchanged.

---

## Prerequisites
- Step 7 is complete: frontend can send messages, reuse a conversation identifier, and render chat history.
- Authentication works; the client can send authenticated requests.
- Backend behavior is stable for chat and task operations.

---

## In Scope
- Floating bottom-right chat launcher button
- Popup chat panel UI (support-style widget)
- Highly user-friendly chat interaction UX (loading, errors, confirmations)
- Conversation continuity (persist the conversation identifier, reload history)
- Optional: lightweight tone improvements via agent instructions (no behavior change)

## Out of Scope
- Separate chat route or dedicated chat tab
- Backend interface changes
- Streaming responses (optional only if already available)
- Multi-conversation management UI (list/switch sessions)
- Admin/support multi-user chat features

---

## UX Requirements

### 1) Chat Launcher (Bottom-Right Widget Button)
- A fixed-position circular button MUST appear at bottom-right on authenticated pages (minimum: the primary tasks page).
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
  - Show assistant typing indicator while waiting for a reply.
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
- The UI MUST store the conversation identifier after the first successful chat response.
- The UI MUST persist the conversation identifier in browser storage using a consistent key.
- On widget open:
  - If a stored conversation identifier exists, load history from the existing chat history service.
  - If not, start fresh when user sends first message.

Logout behavior:
- On logout (or missing token), the widget MUST:
  - hide or become disabled
  - clear the stored conversation identifier

---

### 5) Backend Interaction Contract (Unchanged)
The widget MUST rely on the existing chat service contract without changing it.

---

### 6) Friendly Answers (Tone Requirement)
The assistant responses should be user friendly.

Frontend:
- Render confirmations clearly with friendly, plain language
- Keep messages readable and not overly technical

The assistant experience should remain friendly and clear without changing the underlying behavior.

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
- [ ] Chat button is fixed bottom-right on the primary tasks page
- [ ] Clicking opens a popup chat panel
- [ ] Closing and reopening preserves conversation and history
- [ ] Input is focused on open; Enter sends; loading indicator visible

Chat Functionality
- [ ] Messages successfully round-trip via the existing chat service
- [ ] Conversation identifier is persisted and reused (browser storage)
- [ ] History loads correctly from the existing chat history service
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

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Open Floating Chat and Send a Message (Priority: P1)

As an authenticated user, I want a bottom-right chat widget that opens and lets me send a message so I can manage tasks without leaving the tasks page.

**Why this priority**: This is the primary interaction and the minimum viable experience for the widget.

**Independent Test**: From the tasks page, open the widget, send a message, and verify the assistant reply appears with a loading indicator.

**Acceptance Scenarios**:

1. **Given** I am authenticated on the tasks page, **When** I open the widget and send a message, **Then** my message appears immediately and the assistant reply appears after loading.
2. **Given** the widget is open, **When** I close and reopen it, **Then** the widget remains available and the chat persists.

---

### User Story 2 - Resume Conversation After Refresh (Priority: P2)

As an authenticated user, I want the widget to remember my conversation and load history so I can continue after a refresh.

**Why this priority**: Conversation continuity is a core requirement of the stateless chat experience.

**Independent Test**: Refresh the page and confirm the widget loads recent messages for the stored conversation.

**Acceptance Scenarios**:

1. **Given** I have an active conversation, **When** I refresh and open the widget, **Then** the last messages load in order and the conversation continues.

---

### User Story 3 - Friendly UX with Errors and Empty State (Priority: P3)

As an authenticated user, I want a friendly, accessible chat experience with clear loading, error, and empty states.

**Why this priority**: Polished UX improves trust and reduces confusion during failures or first use.

**Independent Test**: Open the widget with no messages and see prompts; trigger a failure and verify a retry path.

**Acceptance Scenarios**:

1. **Given** no prior messages, **When** I open the widget, **Then** I see example prompts.
2. **Given** a chat request fails, **When** I retry, **Then** the message is resent and a successful reply is shown.

---

### Edge Cases

- What happens when the user has no auth token while the widget is visible?
- How does the widget handle a stored conversation identifier that no longer exists?
- What happens when the chat request fails repeatedly and the user retries multiple times?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a floating chat launcher that is available on authenticated task pages.
- **FR-002**: The system MUST display a popup chat panel that can open and close without losing conversation state.
- **FR-003**: The system MUST send chat messages to the existing chat service with the user token attached.
- **FR-004**: The system MUST persist the active conversation identifier in browser storage and reuse it on reopen.
- **FR-005**: The system MUST load chat history when a stored conversation identifier exists.
- **FR-006**: The system MUST display a loading indicator while waiting for assistant replies.
- **FR-007**: The system MUST show friendly error messaging and allow retry for failed sends.
- **FR-008**: The system MUST provide an accessible input and allow enter-to-send.
- **FR-009**: The system MUST provide a clear visual distinction between user and assistant messages.
- **FR-010**: The system MUST hide or disable the widget when the user is not authenticated.
- **FR-011**: The system MUST clear the stored conversation identifier on logout.
- **FR-012**: The system MUST avoid requiring a dedicated chat page or tab.
- **FR-013**: The system MUST optionally support a collapsed tool-call details view for debugging.

### Key Entities

- **Chat Session**: The persisted conversation identifier and its associated message history used to continue a chat.
- **Chat Message**: A user or assistant message displayed in the widget, optionally with tool call metadata.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can open the widget and send a first message in under 60 seconds without leaving the tasks page.
- **SC-002**: 100% of successful chat requests reuse the stored conversation identifier after the first response.
- **SC-003**: Message history loads and displays in chronological order within 2 seconds on page refresh.
- **SC-004**: Users can recover from a failed send using the retry action without retyping the message.

## Assumptions

- The chat backend contract and authentication behavior remain unchanged.
- The tasks page remains the primary authenticated entry point for chat usage.

## Dependencies

- Existing chat services are available and stable.
- A valid auth token is available in browser storage for authenticated users.
