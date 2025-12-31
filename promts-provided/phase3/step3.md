# specs.md

## Step 3: Task Tools (Pre-AI, Pre-MCP)

### Objective
Introduce a clean, explicit “tool layer” for task operations that will later be used by the AI agent and MCP server.

After this step:
- All task-related actions are exposed as deterministic tool functions
- Chat logic does NOT manipulate tasks directly
- Tools encapsulate validation, ownership, and business rules
- No AI and no MCP are used yet

This step prepares the system for:
- Step 4: AI Agent integration
- Step 6: MCP server extraction

---

## Design Principles

- Tools are pure, deterministic server-side functions
- Tools MUST be user-scoped
- Tools MUST NOT depend on chat state
- Tools MUST be callable independently (for tests)
- Tools wrap existing task repository logic

---

## In Scope
- Tool definitions for task operations
- Tool input validation
- Tool output normalization
- Reuse of existing task repository functions

## Out of Scope
- OpenAI Agents SDK
- MCP server or protocol
- Natural language parsing
- Chat UI changes
- Tool chaining logic (handled later by agent)

---

## Tool Interface Rules

All tools MUST:
- Accept `user_id` as an explicit parameter
- Validate ownership via repository layer
- Return structured JSON-serializable data
- Raise domain errors (not HTTP responses)

Tools MUST NOT:
- Read from or write to chat tables
- Access request/response objects
- Depend on auth middleware directly

---

## Tool Specifications

### Tool: add_task

Purpose:
Create a new task for the authenticated user.

Inputs:
- user_id: string (required)
- title: string (required)
- description: string (optional)

Behavior:
- Validate title (non-empty, existing repo rules apply)
- Create a new task scoped to user_id
- Set completed = false

Returns:
- task_id: integer
- status: string ("created")
- title: string

---

### Tool: list_tasks

Purpose:
Retrieve tasks for a user with optional filtering.

Inputs:
- user_id: string (required)
- status: string (optional; allowed: "all", "pending", "completed")

Behavior:
- Default status = "all"
- Map status to repo query logic
- Only return tasks belonging to user_id

Returns:
- Array of task objects:
  - id: integer
  - title: string
  - completed: boolean

---

### Tool: complete_task

Purpose:
Mark a task as completed.

Inputs:
- user_id: string (required)
- task_id: integer (required)

Behavior:
- Verify task exists and belongs to user_id
- Set completed = true

Returns:
- task_id: integer
- status: string ("completed")
- title: string

---

### Tool: delete_task

Purpose:
Delete a task permanently.

Inputs:
- user_id: string (required)
- task_id: integer (required)

Behavior:
- Verify task exists and belongs to user_id
- Delete task

Returns:
- task_id: integer
- status: string ("deleted")
- title: string

---

### Tool: update_task

Purpose:
Update a task’s title and/or description.

Inputs:
- user_id: string (required)
- task_id: integer (required)
- title: string (optional)
- description: string (optional)

Behavior:
- Verify task exists and belongs to user_id
- Apply partial updates
- Reject if no fields provided

Returns:
- task_id: integer
- status: string ("updated")
- title: string

---

## Error Handling

Tools SHOULD raise domain-level errors:
- TaskNotFound
- InvalidInput
- UnauthorizedAccess

Chat/API layer will translate these into HTTP responses later.

---

## Acceptance Criteria

### Tool Correctness
- [ ] All five tools are implemented
- [ ] Each tool uses existing task repository logic
- [ ] Tools only operate on user-owned tasks

### Isolation
- [ ] Tools can be called without chat context
- [ ] Tools do not reference request/response objects

### Output Shape
- [ ] Tool outputs match specified return formats
- [ ] All outputs are JSON-serializable

---

## Step Exit Criteria
Step 3 is complete when:
- Task tools are implemented and tested
- Tools can be invoked programmatically
- No AI or MCP dependencies exist yet
- Chat endpoint does NOT directly manipulate tasks
