# Feature Specification: Chat Widget Polish

**Feature Branch**: `018-chat-widget-polish`  
**Created**: 2026-01-02  
**Status**: Draft  
**Input**: User description: "promts-provided/phase3/step7.6.md"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Clean Chat Widget Experience (Priority: P1)

As a signed-in user, I can open the chat widget and read/send messages in a clean, familiar layout that fits fully within the window without horizontal scrolling.

**Why this priority**: This is the core value of the step: a polished, readable chat interface that feels modern and reliable.

**Independent Test**: Open the widget, send a message, and confirm the layout fits the viewport with no horizontal scroll while messages wrap correctly.

**Acceptance Scenarios**:

1. **Given** the user opens the chat widget, **When** the chat renders, **Then** the header, message list, and composer fit within the viewport without horizontal scrolling.
2. **Given** a long message is displayed, **When** it renders, **Then** the content wraps within the widget and does not overflow.

---

### User Story 2 - Always-Visible Composer (Priority: P2)

As a signed-in user, I can always see the message composer with a small circular send button and submit via Enter.

**Why this priority**: Sending messages quickly is essential; the composer must stay visible and easy to use.

**Independent Test**: Scroll the message list and verify the input row remains visible; send using Enter and the button.

**Acceptance Scenarios**:

1. **Given** the chat widget is open, **When** I scroll through messages, **Then** the input row remains visible.
2. **Given** I type a message, **When** I press Enter or click the send button, **Then** the message is submitted.

---

### User Story 3 - Concise Assistant Replies (Priority: P3)

As a user, I receive assistant replies that are short and precise, avoiding unnecessary verbosity.

**Why this priority**: Concise responses reduce cognitive load and match the intended user experience.

**Independent Test**: Send a simple request and verify the assistant responds with a short, direct answer.

**Acceptance Scenarios**:

1. **Given** I ask a simple question, **When** the assistant replies, **Then** the response is brief and specific.

---

### Edge Cases

- Long unbroken words or tool output should wrap without causing horizontal scroll.
- Error or empty states should remain readable and aligned with the same typography scale.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The chat widget MUST fit within the viewport and MUST NOT introduce horizontal scrolling.
- **FR-002**: The message list MUST wrap long content and preserve readable spacing between messages.
- **FR-003**: The composer MUST remain visible at the bottom of the chat panel while viewing messages.
- **FR-004**: The send control MUST be a small circular button aligned with the input field.
- **FR-005**: The Enter key MUST submit the message.
- **FR-006**: The chat header MUST display the title “Todo Assistant” with consistent typography hierarchy.
- **FR-007**: Message bubbles MUST be visually distinct for user vs assistant and aligned appropriately.
- **FR-008**: Assistant responses MUST be concise and specific, avoiding unnecessary verbosity.

### Key Entities *(include if feature involves data)*

- **Message**: A chat entry with role (user or assistant), content, and optional tool call details.
- **Conversation**: An ongoing session identifier used to load history and send new messages.

### Assumptions & Dependencies

- The backend continues to return chat responses and history as currently implemented.
- Authentication remains unchanged and continues to provide a valid token for chat requests.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The chat widget renders without horizontal scrolling across common laptop viewport sizes.
- **SC-002**: Users can send a message via Enter or the send button in under 5 seconds.
- **SC-003**: 90% of assistant replies in a sample of 20 simple prompts are concise (under 12 words).
- **SC-004**: Users can identify the chat title and message roles without confusion in a basic usability check.
