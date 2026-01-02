# Feature Specification: Agent Tool Chaining Fix

**Feature Branch**: `019-agent-tool-chaining`
**Created**: 2026-02-01
**Status**: Draft
**Input**: User description: "Fix agent tool chaining so multi-step task requests (e.g., list then complete/update) succeed without fallback responses."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Multi-step tool calls succeed (Priority: P1)

As an authenticated user, I can issue natural language requests that require more than one tool call (for example, list tasks then complete or update one), and the assistant completes the request without returning the fallback error.

**Why this priority**: This restores the primary behavior expected in Step 5/6; multi-step actions are common and currently failing.

**Independent Test**: A chat request that triggers a list_tasks call followed by complete_task or update_task returns a successful assistant response and tool_calls for both tools.

**Acceptance Scenarios**:

1. **Given** a user with at least one task, **When** they request completion by title, **Then** the agent performs list_tasks followed by complete_task and returns a success response.
2. **Given** a user with at least one task, **When** they request an edit by title, **Then** the agent performs list_tasks followed by update_task and returns a success response.

### Edge Cases

- What happens when the second tool call fails (e.g., task not found)?
- How does the system respond if the model returns tool_calls after the second step?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The agent runtime MUST support a second round of tool calls after the initial tool execution.
- **FR-002**: The agent runtime MUST include both tool call results in the returned tool_calls payload.
- **FR-003**: If a tool error occurs in any round, the assistant MUST return the existing friendly error response.
- **FR-004**: The tool-call loop MUST be bounded (maximum two rounds) to avoid infinite tool call cycles.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Multi-step task requests (list then complete/update) return a non-fallback assistant response.
- **SC-002**: tool_calls includes entries for each tool invoked in the sequence.
- **SC-003**: Tool error handling remains consistent with existing behavior.
