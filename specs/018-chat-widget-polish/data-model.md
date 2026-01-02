# Data Model: Chat Widget Polish

## Entities

### Conversation
- **Purpose**: Identifies the active chat session for loading history and continuing the conversation.
- **Key attributes**: `conversation_id` (string or number, provided by backend).

### Message
- **Purpose**: Represents a chat message in the UI.
- **Key attributes**:
  - `role`: user | assistant
  - `content`: string
  - `tool_calls` (optional): structured tool invocation details for display

## Relationships

- A conversation contains many messages.
- Messages are rendered in chronological order.
