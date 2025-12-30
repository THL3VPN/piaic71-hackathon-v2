# Quickstart: Chat Storage Persistence

## Purpose

This feature adds persistent storage for chat conversations and messages with strict user ownership.

## Pre-requisites

- Backend configured with `DATABASE_URL`
- Auth token available for an existing user

## Example Flow

1. Create a conversation
2. Append a message
3. Retrieve message history (default limit 50)

## Testing

- Unit tests cover repository validation, ownership enforcement, ordering, and limits.
- Integration tests cover the three API flows above using an isolated database.

## Notes

- All chat state is stored in the database.
- User identity is derived from auth context only.
