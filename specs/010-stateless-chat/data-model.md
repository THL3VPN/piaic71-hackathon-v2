# Data Model: Stateless Chat Endpoint

## Entities

### Conversation

- **Purpose**: Represents a chat session owned by one authenticated user.
- **Key Attributes**: id, user_id, created_at, updated_at.
- **Relationships**: One Conversation has many Messages; ownership enforced by user_id.

### Message

- **Purpose**: Represents a stored chat message in a conversation.
- **Key Attributes**: id, conversation_id, user_id, role, content, created_at.
- **Relationships**: Each Message belongs to one Conversation and one user.

### Authenticated User

- **Purpose**: Identity derived from auth context for access checks.
- **Key Attributes**: user_id (string identifier).
- **Relationships**: Owns Conversations and Messages.

## Validation Rules

- conversation_id must be owned by the authenticated user when provided.
- message is required and must be a non-empty string.
- History retrieval uses a default limit of 50 messages per request.
- tool_calls in responses is always an empty array in this step.

## State Transitions

- Conversation is created when no conversation_id is provided.
- Messages are appended: user message first, then assistant response.
