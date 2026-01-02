# Implementation Plan: Agent Tool Chaining Fix

## Summary

Extend the agent runtime execution to handle a second tool-call round, bounded to avoid infinite loops. Preserve existing tool payload structure and error responses.

## Architecture & Flow

- Update `src/services/agent_runtime.py` to:
  - Execute initial tool calls.
  - Request a second completion.
  - If the second response includes tool calls, execute them once and then request a final completion.
  - Return the final assistant response and accumulated tool_calls.
- Keep MCP client usage as-is; only adjust orchestration logic.

## Testing Strategy

- Add/extend unit tests for the agent runtime to cover two-step tool chaining.
- Validate that tool_calls payload includes both tool results.
- Ensure error handling remains unchanged.
