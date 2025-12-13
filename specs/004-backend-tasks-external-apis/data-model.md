# Data Model: Task REST API

- **Task**
  - **Fields**:
    - `id`: auto-increment primary key (int)
    - `title`: required non-empty trimmed string
    - `description`: optional string
    - `completed`: boolean default `False`
    - `created_at`: timestamp (UTC) set once on insert
  - **Validation rules**:
    - `title` cannot be blank or whitespace
    - `completed` only toggled via dedicated PATCH
    - `created_at` read-only once persisted
  - **Relationships**: Currently standalone, no foreign keys; future features may relate tasks to users.
  - **State transitions**: `completed` flips via PATCH; deletion removes record; updates mutate `title`/`description` but leave `created_at`.
