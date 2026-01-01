# Quickstart: Agent Behavior Validation

## Goal

Validate that the agent understands natural language task commands, selects the correct tools, and responds with friendly confirmations while remaining stateless.

## Setup

- Backend running with a configured model provider.
- Authorization token available for the test user.

## Manual Validation (curl)

Replace `$TOKEN` with a valid JWT.

1. Add a task
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Add a task to buy groceries"}' | jq
```

2. List all tasks
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Show me all my tasks"}' | jq
```

3. List pending tasks
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"What\'s pending?"}' | jq
```

4. Complete a task by id
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Mark task 3 as complete"}' | jq
```

5. Delete a task with ambiguous title
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Delete the meeting task"}' | jq
```

6. Update a task
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Change task 1 to Call mom tonight"}' | jq
```

7. Add a reminder
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"I need to remember to pay bills"}' | jq
```

8. List completed tasks
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"What have I completed?"}' | jq
```

## Expected Outcomes

- Each command returns a friendly confirmation.
- Tool calls are present in the response payload and match the intended action.
- When ambiguous, the agent asks a clarification or lists tasks before acting.
- No internal system details are exposed.

## Validation Notes (2026-01-02)

Quickstart coverage status:
- Contract: `tests/contract/test_agent_behavior_create_contract.py` (pass)
- Contract: `tests/contract/test_agent_behavior_list_contract.py` (pass)
- Integration: `tests/integration/test_agent_behavior_add_list_api.py` (pass)
- Contract: `tests/contract/test_agent_behavior_chain_contract.py` (pass)
- Integration: `tests/integration/test_agent_behavior_chain_api.py` (pass)
- Contract: `tests/contract/test_agent_behavior_errors_contract.py` (pass)
- Integration: `tests/integration/test_agent_behavior_errors_api.py` (pass)
