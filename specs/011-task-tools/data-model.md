# Data Model: Task Tools Layer

## Entities

### Task

Represents a user-owned task.

**Key attributes**:
- id (integer)
- user_id (string)
- title (string)
- description (string, optional)
- completed (boolean)

### Tool Result

Represents a structured output returned by tool functions.

**Key attributes**:
- task_id (integer)
- status (string: created | updated | completed | deleted)
- title (string)

### Tool Error

Represents domain-level errors raised by tools.

**Types**:
- TaskNotFound
- InvalidInput
- UnauthorizedAccess

## Relationships

- Task is owned by a single user (user_id).
- Tool results reference a single task via task_id.

## Validation Rules

- Title must be non-empty (trimmed).
- list_tasks status filter must be one of: all, pending, completed.
- update_task requires at least one field (title or description).
