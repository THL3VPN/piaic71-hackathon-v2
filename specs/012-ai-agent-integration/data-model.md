# Data Model: AI Agent Integration

## Entities

### Conversation

Represents a user-owned chat session.

**Key attributes**:
- id (integer)
- user_id (string)
- created_at (datetime)
- updated_at (datetime)

### Message

Represents a single user or assistant message.

**Key attributes**:
- id (integer)
- conversation_id (integer)
- user_id (string)
- role (string: user | assistant)
- content (string)
- created_at (datetime)

### Tool Call

Represents an executed tool call recorded for audit and response payloads.

**Key attributes**:
- name (string)
- arguments (object)
- result (object)

### Provider Configuration

Represents runtime configuration for selecting an AI provider and model.

**Key attributes**:
- provider (string)
- model_name (string)
- history_limit (integer)

## Relationships

- Conversation owns Messages.
- Tool Calls are associated with an assistant response.

## Validation Rules

- Tool calls must be JSON-serializable.
- history_limit must default to 50 when not configured.
- provider must be one of the supported providers.
