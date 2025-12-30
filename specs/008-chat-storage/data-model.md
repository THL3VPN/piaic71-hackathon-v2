# Data Model: Chat Storage Persistence

## Conversation

**Purpose**: Represents a single chat session owned by one user.

**Fields**:
- `id` (integer, primary key)
- `user_id` (string, derived from authenticated user)
- `created_at` (datetime, server-generated)
- `updated_at` (datetime, server-generated)

**Relationships**:
- One Conversation has many Messages.

**Validation Rules**:
- `user_id` must be present from auth context.

**State Transitions**:
- `updated_at` changes when a new message is appended.

## Message

**Purpose**: Represents a single message within a conversation.

**Fields**:
- `id` (integer, primary key)
- `user_id` (string, derived from authenticated user)
- `conversation_id` (integer, foreign key to Conversation.id)
- `role` (string, allowed values: "user", "assistant")
- `content` (string, message text)
- `created_at` (datetime, server-generated)

**Relationships**:
- Each Message belongs to one Conversation and one User.

**Validation Rules**:
- `role` must be one of the allowed values.
- `content` must be non-empty.
- `conversation_id` must reference an existing Conversation owned by the user.
