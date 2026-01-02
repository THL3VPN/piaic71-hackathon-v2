# Quickstart: Floating Chat Widget UX

## Goal

Validate the floating widget experience on the tasks page without using a dedicated chat route.

## Setup

- Start backend and frontend locally.
- Log in and land on the tasks page.

## Manual Validation

1. On the tasks page, find the bottom-right chat launcher.
2. Open the widget; input should focus automatically.
3. Send a message and confirm optimistic rendering + assistant reply.
4. Close and reopen the widget; messages and conversation resume.
5. Refresh the page; open the widget and confirm history reloads.
6. Trigger a failure (e.g., stop backend), verify friendly error and retry behavior.

## Expected Outcomes

- Widget stays available on the tasks page without navigating away.
- Conversation continues across close/open and refresh.
- Loading and error states are visible and user friendly.
