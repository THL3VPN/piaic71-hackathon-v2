# Feature Specification: MCP Server Extraction

**Feature Branch**: `015-mcp-server-extraction`
**Created**: 2026-01-02
**Status**: Draft
**Input**: User description: "promts-provided/phase3/step6"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task tools available via MCP (Priority: P1)

As an authenticated user, task operations are executed through MCP tools so task changes remain correct and ownership-safe.

**Why this priority**: The MCP server is the core architectural change and must expose all task tools correctly before any integration work matters.

**Independent Test**: Invoke each MCP tool and verify task creation, listing, completion, update, and deletion for a single user.

**Acceptance Scenarios**:

1. **Given** a valid user id, **When** the MCP tool `add_task` is invoked, **Then** the task is created and the tool returns the correct fields.
2. **Given** tasks for a user, **When** `list_tasks` is invoked with each status mapping, **Then** the returned tasks match the requested status.

---

### User Story 2 - Chat uses MCP tools without behavior change (Priority: P2)

As an authenticated user, chat behavior stays the same as Step 5 while task operations are executed through MCP tools instead of local tool calls.

**Why this priority**: Users must not see behavior regressions during the architecture change.

**Independent Test**: Run the Step 5 chat scenarios and verify tool_calls reflect MCP tool usage and outcomes match prior behavior.

**Acceptance Scenarios**:

1. **Given** a natural language command (add/list/complete/update/delete), **When** `/api/chat` is called, **Then** the response matches Step 5 behavior and tool_calls reflect MCP tools.
2. **Given** an authenticated user, **When** a task is updated via chat, **Then** the task is updated in the database and the response confirms it.

---

### User Story 3 - Ownership and statelessness preserved (Priority: P3)

As an authenticated user, I cannot access another user's tasks, and the system remains stateless across requests.

**Why this priority**: Ownership and statelessness are core safety guarantees.

**Independent Test**: Attempt cross-user tool actions and confirm not-found style errors with no data leakage.

**Acceptance Scenarios**:

1. **Given** a task owned by another user, **When** a tool is invoked with a different user id, **Then** the tool returns a not-found style error.

---

### Edge Cases

- What happens when a task id exists for another user (ownership violation)?
- How does the MCP server handle invalid or missing tool parameters?
- What happens when the MCP server is unavailable during a chat request?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expose task operations as MCP tools: add_task, list_tasks, complete_task, delete_task, update_task.
- **FR-002**: MCP tools MUST be stateless and use the database as the source of truth.
- **FR-003**: MCP tools MUST enforce user ownership and return not-found style errors for unauthorized access.
- **FR-004**: The chat backend MUST invoke MCP tools for task operations and MUST NOT call local task tool functions.
- **FR-005**: Chat behavior MUST remain identical to Step 5 (intent mapping, confirmations, tool chaining, and error responses).
- **FR-006**: Tool call logging MUST be returned in `/api/chat` responses.
- **FR-007**: The backend MUST pass the authenticated user id to MCP tools.
- **FR-008**: The MCP server MUST be runnable as a dedicated service using the Official MCP SDK.
- **FR-009**: Environment configuration MUST support MCP server URL and model provider settings without hardcoding secrets.

### Assumptions

- Task tools are already implemented and validated in the backend.
- Chat endpoint and persistence are already working and stateless.
- A Neon database is available via environment configuration.

### Key Entities *(include if feature involves data)*

- **MCP Server**: A dedicated service that exposes task tools.
- **MCP Tool**: A task operation callable by the agent (add/list/complete/delete/update).
- **Tool Call Record**: The tool invocation details returned in chat responses.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of tool invocations for the five task operations succeed for valid inputs in validation runs.
- **SC-002**: 0 cross-user task operations succeed; all ownership violations return not-found style errors.
- **SC-003**: Step 5 natural language validation commands pass unchanged using the external tool interface.
- **SC-004**: 100% of chat responses that invoke tools include tool_calls reflecting the external tool usage.
