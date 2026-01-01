# Data Model: Frontend Chat UI Integration

## Entities

### Chat Conversation
- Represents the active conversation identifier stored in client state.
- Attributes: conversation_id (integer), persistence source (local storage).
- Relationship: one active conversation per authenticated user session.

### Chat Message
- Represents a single message displayed in the UI.
- Attributes: role (user/assistant), content (string), created_at (timestamp), tool_calls (optional metadata).
- Relationship: belongs to a conversation; ordered chronologically.
