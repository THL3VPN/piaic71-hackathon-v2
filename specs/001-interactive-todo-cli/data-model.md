# Data Model: Interactive CLI Todo App

## Entities

### Task
- **Purpose**: Represents a todo item in the in-memory session.
- **Fields**:
  - `id: int` — unique within the session (incrementing).
  - `title: str` — required, non-empty, trimmed of leading/trailing whitespace.
  - `completed: bool` — default `False`, toggled via user action.
- **Validation rules**:
  - Title MUST not be empty or whitespace-only.
  - ID lookups MUST confirm existence; invalid IDs return “task not found.”
- **State transitions**:
  - Create → adds task to in-memory list with `completed=False`.
  - Update → replaces title when valid ID and non-empty title provided.
  - Toggle → flips `completed` boolean.
  - Delete → removes task by ID; remaining IDs stay stable for the session.

### Session Task List
- **Purpose**: In-memory collection that lives for the duration of the process.
- **Behaviors**:
  - Supports append, update, toggle, delete, and list operations.
  - Returns user-facing results/messages for success or “task not found” without raising fatal errors.
- **Constraints**:
  - No persistence to disk or external stores.
  - Expected size: modest (<1k tasks); no performance optimizations required beyond O(n) list operations.
