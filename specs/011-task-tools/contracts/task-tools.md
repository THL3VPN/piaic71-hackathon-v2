# Task Tools Contract

## Overview

Deterministic tool functions for task operations. Tools accept an explicit user_id, perform validation and ownership checks through repository logic, and return structured JSON-serializable outputs. Tools raise domain errors rather than HTTP responses.

## Tool: add_task

**Purpose**: Create a task for a user.

**Inputs**:
- user_id: string (required)
- title: string (required)
- description: string (optional)

**Behavior**:
- Validate title (non-empty)
- Create task owned by user_id
- Set completed = false

**Returns**:
- task_id: integer
- status: string ("created")
- title: string

**Errors**:
- InvalidInput

---

## Tool: list_tasks

**Purpose**: Retrieve tasks for a user with optional status filtering.

**Inputs**:
- user_id: string (required)
- status: string (optional; "all" | "pending" | "completed")

**Behavior**:
- Default status = "all"
- Return only user-owned tasks

**Returns**:
- Array of task objects:
  - id: integer
  - title: string
  - completed: boolean

**Errors**:
- InvalidInput (unsupported status)

---

## Tool: complete_task

**Purpose**: Mark a task as completed.

**Inputs**:
- user_id: string (required)
- task_id: integer (required)

**Behavior**:
- Verify task exists and belongs to user_id
- Set completed = true

**Returns**:
- task_id: integer
- status: string ("completed")
- title: string

**Errors**:
- TaskNotFound
- UnauthorizedAccess

---

## Tool: delete_task

**Purpose**: Delete a task permanently.

**Inputs**:
- user_id: string (required)
- task_id: integer (required)

**Behavior**:
- Verify task exists and belongs to user_id
- Delete task

**Returns**:
- task_id: integer
- status: string ("deleted")
- title: string

**Errors**:
- TaskNotFound
- UnauthorizedAccess

---

## Tool: update_task

**Purpose**: Update a task's title and/or description.

**Inputs**:
- user_id: string (required)
- task_id: integer (required)
- title: string (optional)
- description: string (optional)

**Behavior**:
- Verify task exists and belongs to user_id
- Reject if no fields provided
- Apply partial updates

**Returns**:
- task_id: integer
- status: string ("updated")
- title: string

**Errors**:
- TaskNotFound
- UnauthorizedAccess
- InvalidInput
