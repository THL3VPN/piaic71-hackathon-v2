# Quickstart: Frontend Chat UI Integration

## Goal

Verify the chat UI can send messages, persist conversation_id, and render history.

## Setup

- Ensure backend is running and `NEXT_PUBLIC_BACKEND_URL` is set in frontend env.
- Ensure a valid auth token exists in localStorage.

## Manual Validation

1. Open the chat UI route or chat panel from `/tasks`.
2. Send a message ("Add a task to buy groceries").
3. Confirm the assistant reply appears with a loading indicator while waiting.
4. Refresh the page and confirm the same conversation and message history loads.
5. Toggle tool call details if enabled and verify the metadata appears.

## Expected Outcomes

- Messages appear in chronological order with roles.
- The UI reuses conversation_id across refreshes.
- Errors are surfaced with a retry option.
