# Data Model: Real-Time Agent Tool Calls

## Entities

### Chat Response

- Represents the assistant response for a chat request.
- Includes response text and tool call details for transparency.

### Tool Call

- Fields: name, inputs (arguments), outputs (result).
- Returned in the chat response payload.

### Conversation History

- Stored messages used to rebuild context per request.
- No schema changes required; uses existing message storage.
