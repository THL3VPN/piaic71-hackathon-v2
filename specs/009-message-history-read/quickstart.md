# Quickstart: Message History Read

## Prerequisites

- Backend running with `DATABASE_URL` configured.
- Valid bearer token from `/api/login`.
- An existing conversation with messages.

## Example Requests

### Fetch message history (default limit)

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/conversations/12/messages
```

### Fetch message history with limit

```bash
curl -s \
  -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/conversations/12/messages?limit=25"
```

### Expect not found for other users

```bash
curl -i \
  -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/conversations/9999/messages
```

## Validation Checklist

- Returns messages ordered oldest to newest.
- Default limit returns up to 50 messages.
- Limit is clamped to 200 when higher.
- Limit <= 0 returns 422.
- Non-owner access returns 404.
