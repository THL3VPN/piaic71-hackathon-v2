# Data Model: Username/Password Auth with User-Scoped Tasks

## Entities

- **User**
  - id (int, PK)
  - username (str, unique, required)
  - password_hash (str, bcrypt)
  - created_at (datetime, default now)

- **Task** (extends existing fields)
  - id (int, PK)
  - title (str, required, non-empty)
  - description (str, optional)
  - completed (bool, default false)
  - created_at (datetime, default now)
  - owner_id (int, FK → User.id, required)

## Relationships

- One User to many Tasks (owner_id).

## Validation Rules

- Username must be unique and non-empty.
- Password must be hashed; never persisted or logged in plaintext.
- Task title required and non-empty.
- Task operations enforce ownership: caller’s `sub` must match task.owner_id.
