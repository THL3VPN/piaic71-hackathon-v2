## Data Model – Frontend tasks UI

### Task
- Represents a persisted task stored by the backend.
- Attributes:
  - `id` (UUID or integer): primary identifier used client-side to key list entries.
  - `title` (string, required): text shown prominently in the UI.
  - `description` (string, optional): secondary text displayed when present.
  - `completed` (boolean): determines status badge (e.g., “Done” vs “Pending”).
  - `created_at` (timestamp): used for ordering or display if needed.

### UI State
- `tasks`: array of `Task` objects fetched from `GET /api/tasks`.
- `formErrors`: validation status for the Add Task form (ensures title is required).
- `fetchStatus`: tracks `loading`, `success`, or `error` to control skeleton/alerts.

This frontend does not persist new structures; it relies on the backend’s existing SQLModel table. The UI keeps track of the last fetch/submit status to provide user feedback without duplicating the database.
