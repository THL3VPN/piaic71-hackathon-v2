# Quickstart: Chat Widget Polish

## Prerequisites

- Backend running with valid JWT auth
- Frontend dependencies installed

## Run Frontend

```bash
cd frontend
npm install
npm run dev
```

## Validate UI Requirements

1. Log in and open the Tasks page.
2. Open the chat widget.
3. Verify the widget fits within the viewport with no horizontal scroll.
4. Send a message and confirm:
   - The composer stays visible at the bottom.
   - The send button is a small circular control.
   - Enter submits the message.
5. Confirm message labels are compact and do not add extra verbosity.
6. Confirm user/assistant messages are aligned and wrapped as bubbles.
7. Confirm assistant replies are concise for simple requests.
