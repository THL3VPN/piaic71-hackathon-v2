# Quickstart: Stateless Chat Endpoint

## Prerequisites

- Backend running with `DATABASE_URL` configured.
- Valid bearer token from `/api/login`.
- Step 1 and 1.5 already implemented (conversation/message persistence and history retrieval).

## Example Requests

### Start a new conversation

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}' \
  http://localhost:8000/api/chat
```

### Continue an existing conversation

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"conversation_id": 12, "message": "Add eggs"}' \
  http://localhost:8000/api/chat
```

## Validation Checklist

- Response includes conversation_id, response string, and tool_calls (empty).
- User and assistant messages are stored per request.
- Requests with non-owned conversation_id return 404.
- Invalid payloads return 422.
