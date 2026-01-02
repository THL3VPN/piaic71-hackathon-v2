# specs.md

## Step 5: Natural Language Coverage & Agent Behavior Validation

### Objective
Ensure the AI agent reliably understands and executes natural language task commands using the Step 3 tools, following the defined Agent Behavior Specification.

This step focuses on:
- Intent recognition
- Correct tool selection
- Tool chaining (when required)
- Friendly confirmations
- Graceful error handling

No new infrastructure is introduced in this step.

---

## Prerequisites
- Step 1: Conversation & Message persistence completed
- Step 2: Stateless chat endpoint completed
- Step 3: Task tools implemented and validated
- Step 4: AI agent integrated with env-driven LLM provider

---

## In Scope
- Validation of natural language commands
- Agent behavior refinement (prompt/instructions only)
- Tool selection correctness
- Tool chaining logic
- Error handling and confirmations

## Out of Scope
- MCP server
- Frontend chat UI
- Streaming responses
- Model switching logic (already handled in Step 4)

---

## Agent Behavior Requirements

### Task Creation
When user intent indicates adding/creating/remembering:
- Agent MUST call `add_task`
- Agent MUST extract a reasonable task title
- Agent MUST confirm creation

Examples:
- "Add a task to buy groceries"
- "I need to remember to pay bills"

---

### Task Listing
When user intent indicates listing tasks:
- Agent MUST call `list_tasks`
- Agent MUST infer status when possible

Status Mapping:
- "all" → status="all"
- "pending", "open", "remaining" → status="pending"
- "completed", "done" → status="completed"

Examples:
- "Show me all my tasks"
- "What's pending?"
- "What have I completed?"

---

### Task Completion
When user intent indicates completion:
- Agent MUST call `complete_task`
- Agent MUST require or infer a task_id
- If task_id is missing:
  - Agent SHOULD list tasks first or ask a clarification question

Examples:
- "Mark task 3 as complete"
- "I finished the groceries task"

---

### Task Deletion
When user intent indicates deletion:
- Agent MUST call `delete_task`
- If task_id is ambiguous:
  - Agent MUST call `list_tasks` first
  - Agent MUST ask for confirmation if multiple matches exist

Examples:
- "Delete the meeting task"
- "Remove task 2"

---

### Task Update
When user intent indicates update/change:
- Agent MUST call `update_task`
- Agent MUST update only provided fields
- Agent MUST reject updates with no fields

Examples:
- "Change task 1 to call mom tonight"
- "Rename groceries to buy groceries and fruits"

---

## Tool Chaining Rules

The agent MAY chain tools in a single turn when required.

Allowed chains:
- list_tasks → delete_task
- list_tasks → complete_task
- list_tasks → update_task

Rules:
- Tool chaining MUST be deterministic
- Agent MUST explain what it is doing in the final response

---

## Error Handling Requirements

### Task Not Found
If a tool raises a task-not-found error:
- Agent MUST respond politely
- Agent MUST NOT crash
- Agent SHOULD suggest listing tasks

Example response:
"I couldn’t find that task. Would you like me to show your current tasks?"

---

### Ambiguous Requests
If intent or task reference is unclear:
- Agent MUST ask a follow-up question
- Agent MUST NOT guess

Example:
"I see more than one matching task. Which one should I update?"

---

## Response Style Requirements

- Friendly and concise
- Action confirmations included
- No internal tool or system details exposed
- No hallucinated task state

---

## Validation Test Cases (Manual via curl)

The following commands MUST work correctly via `/api/chat`:

1. "Add a task to buy groceries"
2. "Show me all my tasks"
3. "What's pending?"
4. "Mark task 3 as complete"
5. "Delete the meeting task"
6. "Change task 1 to Call mom tonight"
7. "I need to remember to pay bills"
8. "What have I completed?"

Each test MUST:
- Invoke correct tool(s)
- Mutate DB correctly
- Return friendly confirmation
- Populate `tool_calls` correctly

---

## Acceptance Criteria

Functional:
- [ ] All natural language commands execute correct tools
- [ ] Tool chaining works where required
- [ ] Errors are handled gracefully

Persistence:
- [ ] Chat messages stored correctly
- [ ] Task DB reflects chat actions

Model Independence:
- [ ] Behavior works identically across GPT or Gemini
- [ ] Only env vars change when switching models

---

## Step Exit Criteria
Step 5 is complete when:
- All specified natural language commands behave correctly
- Tool usage matches Agent Behavior Specification
- No hallucinated task state is observed
- System is ready for MCP extraction (Step 6)
