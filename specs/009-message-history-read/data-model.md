# Data Model: Message History Read

## Entities

### Conversation

- **Purpose**: Represents a single chat session owned by one authenticated user.
- **Key Attributes**: id, user_id, created_at, updated_at.
- **Relationships**: One Conversation has many Messages; ownership enforced by user_id.

### Message

- **Purpose**: Represents a single chat message in a conversation.
- **Key Attributes**: id, conversation_id, user_id, role, content, created_at.
- **Relationships**: Each Message belongs to one Conversation and one user.

### Authenticated User

- **Purpose**: Identity derived from auth context used for ownership checks.
- **Key Attributes**: user_id (string identifier).
- **Relationships**: Owns Conversations and Messages.

## Validation Rules

- Only the authenticated user can access messages for their own conversation.
- Role values are limited to "user" or "assistant" (existing rule).
- Message history retrieval uses a default limit of 50 if unspecified.
- Limit values are clamped to a maximum of 200; values <= 0 are invalid.
- Messages are returned in chronological order (created_at ascending, then id ascending).

## State Transitions

- None for this feature; read-only retrieval.
