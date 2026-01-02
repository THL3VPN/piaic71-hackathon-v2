# Data Model: Floating Chat Widget UX

## Entities

### ChatWidgetState
- **open**: boolean
- **loadingHistory**: boolean
- **sending**: boolean
- **error**: string | null
- **retryMessage**: string | null

### ConversationRef
- **id**: number | null
- **persisted**: boolean

### ChatMessage
- **role**: "user" | "assistant"
- **content**: string
- **created_at**: string | undefined
- **tool_calls**: ToolCall[] | undefined

### ToolCall (optional)
- **name**: string
- **arguments**: object
- **result**: object

## Relationships
- ChatWidgetState owns a list of ChatMessage and the ConversationRef.
- ToolCall is nested within assistant ChatMessage.

## Validation Rules
- Message content must be non-empty before send.
- ConversationRef id is present only after first successful response.
