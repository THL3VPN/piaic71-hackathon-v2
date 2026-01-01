# Quickstart: Real-Time Agent Tool Calls

## Goal

Validate that the chat endpoint uses the agent, invokes tools, and returns tool call details while remaining stateless and configurable by environment.

## Suggested Tests

1. **Agent executes tool calls**
   - Send a chat message asking to create a task
   - Confirm tool call details in the response and task creation in DB

2. **Tool error handling**
   - Send a chat message that refers to a missing task
   - Confirm the assistant responds with a friendly error message

3. **Tool call transparency**
   - Verify tool call details include name, inputs, and outputs

4. **Stateless history**
   - Send a message, restart service, send another message
   - Confirm response uses DB-backed history (within configured limit)

## Validation Notes (2026-01-01)

Quickstart coverage status:
- Contract: `tests/contract/test_agent_tool_calls_contract.py` (pass)
- Integration: `tests/integration/test_agent_tool_calls_api.py` (pass)
- Integration: `tests/integration/test_agent_tool_calls_payload.py` (pass)
- Integration: `tests/integration/test_agent_tool_calls_errors.py` (pass)

Latest validation run:
- `uv run pytest -q tests/contract/test_agent_tool_calls_contract.py`
