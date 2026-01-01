# Feature Specification: Real-Time Agent Tool Calls

**Feature Branch**: `013-agent-tool-calls`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "Here’s the spec outline for “Real-time agent replies + tool calling” that should drive the next task set.

  Feature Goal
  Enable live agent responses using OpenAI Agents SDK with registered task tools; tool calls must be executed and returned in the chat response.

  Scope (In)

  - Agent runtime uses OpenAI Agents SDK
  - Task tools are registered and invoked by the agent
  - Tool call payloads are captured and returned in /api/chat response
  - Chat remains stateless; history comes from DB each request

  Out of Scope

  - DB model changes
  - Auth changes
  - MCP tools/servers
  - Frontend changes

  Functional Requirements

  - FR-001: Agent runtime must create an SDK agent using configured provider/model.
  - FR-002: Agent runtime must register existing task tools.
  - FR-003: Tool calls must execute through the existing tool layer (no bypass).
  - FR-004: Response must include tool_calls with tool name, arguments, and result.
  - FR-005: Errors from tools must produce a friendly assistant response while preserving HTTP auth/validation errors.

  Acceptance Criteria

  - A chat request asking to create a task returns a non-empty tool_calls array.
  - Created task is visible via /api/tasks.
  - Responses contain both response text and tool_calls.
  - Stateless history is honored with configured history limit.
  - Contract/integration tests pass for tool invocation and response shape."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Execute task tools via chat (Priority: P1)

As an authenticated user, I can ask the assistant to create or update a task and receive a response that confirms the tool action.

**Why this priority**: Tool-driven task updates are the primary value of chat and must work before any refinements.

**Independent Test**: Send a single chat request that asks for a task change and verify a tool call is returned and the task exists.

**Acceptance Scenarios**:

1. **Given** an authenticated user, **When** they ask to create a task, **Then** the response includes a tool call and the task appears in their task list.
2. **Given** an authenticated user, **When** they ask to complete a task, **Then** the response confirms completion and the task status reflects the change.

---

### User Story 2 - Tool call transparency (Priority: P2)

As an authenticated user, I can see which tool was invoked and what it returned in the chat response payload.

**Why this priority**: Transparency is required for auditing and debugging task actions without exposing implementation details.

**Independent Test**: Inspect a chat response payload after a tool action and verify it includes tool name, arguments, and result.

**Acceptance Scenarios**:

1. **Given** a chat request that triggers a tool, **When** the response is returned, **Then** it includes a tool_calls array with tool name, inputs, and outputs.

---

### User Story 3 - Robust tool error handling (Priority: P3)

As an authenticated user, I receive a friendly assistant response when a tool operation fails.

**Why this priority**: Failures must be understandable and non-disruptive while maintaining security and validation behavior.

**Independent Test**: Trigger a known tool error (for example, referencing a missing task) and confirm a friendly response is returned.

**Acceptance Scenarios**:

1. **Given** a chat request that cannot be fulfilled by a tool, **When** the tool fails, **Then** the assistant returns a friendly message and no unauthorized data is exposed.

---

### Edge Cases

- What happens when the provider configuration is invalid or missing?
- How does the system handle a tool execution error for a non-existent task?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use a configurable agent runtime to generate real chat replies for authenticated users.
- **FR-002**: System MUST register the existing task tools for agent invocation.
- **FR-003**: System MUST execute task changes through the tool layer only.
- **FR-004**: System MUST return tool call details (name, inputs, outputs) in chat responses.
- **FR-005**: System MUST keep chat stateless by rebuilding context from stored messages each request.
- **FR-006**: System MUST scope all tool calls to the authenticated user.
- **FR-007**: System MUST return friendly assistant messages for tool errors while preserving auth/validation HTTP errors.

### Assumptions

- The authenticated chat endpoint and message persistence are already available.
- Task tools are already implemented and validated.
- Provider configuration values are supplied through environment settings.

### Key Entities *(include if feature involves data)*

- **Chat Response**: The user-visible assistant reply, including tool call details.
- **Tool Call**: A record of tool name, inputs, and outputs returned in the response.
- **Conversation History**: Stored messages used to rebuild context per request.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 95% of chat requests that require task operations complete with a tool call and confirmation in tests.
- **SC-002**: 100% of tool-invoking chat responses include tool call details in the payload in tests.
- **SC-003**: Users can complete a task creation request in a single chat turn during testing scenarios.
- **SC-004**: Stateless history reconstruction succeeds after a service restart in all test runs.
