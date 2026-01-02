# Quickstart: MCP Server Extraction

## Goal

Validate MCP tool availability and ensure `/api/chat` uses MCP tools without behavior changes.

## Setup

- Start the MCP server with `DATABASE_URL` configured.
- Start the backend with `MCP_SERVER_URL` pointing to the MCP server.
- Set provider configuration and auth token for chat validation.

### Example local run

```bash
# MCP server (uses .env)
./scripts/run-mcp.sh
```

```bash
# Backend (uses .env)
./scripts/run-backend.sh
```

## Manual Validation (curl)

Replace `$TOKEN` and `$MCP_URL` with real values.

1. MCP add_task
```bash
curl -s -X POST $MCP_URL/mcp/tools/add_task \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","title":"Buy groceries","description":"Milk"}' | jq
```

2. MCP list_tasks
```bash
curl -s -X POST $MCP_URL/mcp/tools/list_tasks \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","status":"pending"}' | jq
```

3. MCP complete_task
```bash
curl -s -X POST $MCP_URL/mcp/tools/complete_task \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","task_id":1}' | jq
```

4. MCP delete_task
```bash
curl -s -X POST $MCP_URL/mcp/tools/delete_task \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","task_id":1}' | jq
```

5. MCP update_task
```bash
curl -s -X POST $MCP_URL/mcp/tools/update_task \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo","task_id":1,"title":"Buy groceries and fruit"}' | jq
```

6. Chat behavior (Step 5 commands)
```bash
curl -s -X POST http://localhost:8000/api/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Add a task to buy groceries"}' | jq
```

## Expected Outcomes

- MCP tools return correct results for valid user ids and inputs.
- Ownership violations return not-found style errors.
- `/api/chat` responses match Step 5 behavior and include MCP tool_calls.

## Validation Record

- Date: 2026-01-01
- Status: Not run (requires running MCP server + backend with real env vars)
- Notes: Use the commands above after `MCP_SERVER_URL`, `DATABASE_URL`, and auth token are set.
