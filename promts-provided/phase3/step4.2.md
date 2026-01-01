Here’s the spec outline for “Real-time agent replies + tool calling” that should drive the next task set.

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
  - Contract/integration tests pass for tool invocation and response shape.