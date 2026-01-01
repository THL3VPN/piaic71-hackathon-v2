# Quickstart: AI Agent Integration

## Goal

Validate that the chat endpoint uses the agent, invokes tools, and returns tool call details while remaining stateless and configurable by environment.

## Suggested Tests

1. **Agent executes tool calls**
   - Send a chat message asking to create a task
   - Confirm tool call details in the response and task creation in DB

2. **Tool error handling**
   - Send a chat message that refers to a missing task
   - Confirm the assistant responds with a friendly error message

3. **Provider configuration**
   - Start with provider configuration A and send a chat message
   - Switch to provider configuration B and send a chat message
   - Confirm the agent responds without code changes

4. **Stateless history**
   - Send a message, restart service, send another message
   - Confirm response uses DB-backed history (within configured limit)

5. **Tool call audit**
   - Confirm tool call details are included in response payloads

## Validation Notes (2025-12-31)

Quickstart coverage status:
- Unit: `tests/unit/test_agent_runtime.py` (pass)
- Unit: `tests/unit/test_chat_provider.py` (pass)
- Integration: `tests/integration/test_agent_chat_history.py` (pass)
