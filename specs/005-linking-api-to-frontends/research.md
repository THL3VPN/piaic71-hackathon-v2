## Research – Frontend tasks UI

### Decision 1: Reuse backend tasks API
- **Decision**: Consume the existing `GET /api/tasks` and `POST /api/tasks` endpoints provided by the backend rather than building new endpoints.
- **Rationale**: Avoids duplicating backend logic and keeps the UI focused on displaying/creating tasks; ensures any current business rules stay centralized.
- **Alternatives considered**:
  - Building a dedicated frontend-only mock API: rejected because the spec explicitly requires integration with the real backend.
  - Embedding SQLite in the frontend: rejected to keep the architecture clean and aligned with current backend coverage metrics.

### Decision 2: Client-side fetching + optimistic refresh
- **Decision**: Fetch tasks and submit new ones entirely on the client (Next.js page component) and refresh via re-fetch or state update, respecting TDD.
- **Rationale**: Keeping it client-driven simplifies the UI layers and aligns with the rapid manual "create/add tasks" experience; allows Jest/Vitest tests to mock fetch easily.
- **Alternatives considered**:
  - Using server actions/server-side props: rejected because spec wants interactive UI and immediate list refresh after creation without full reload.

### Decision 3: Vitest + Testing Library for TDD
- **Decision**: Write Vitest tests covering GET/POST flows before implementing UI behavior; use Testing Library for DOM assertions.
- **Rationale**: Vitest integrates with Next (ESM) and runs quickly, supporting the TDD workflow mandated by the constitution.
- **Alternatives considered**:
  - Jest with React Testing Library: more configuration, slower startup; Vitest is adequate and keeps coverage measurable.

### Decision 4: Resilient UI messaging and responsive layout
- **Decision**: Surface fetch failures through an `alert` element with `aria-live` while using Tailwind grid utilities to stack cards on narrow widths.
- **Rationale**: Users should immediately see when the backend is unreachable, and vertical stacking keeps cards legible on mobile.
- **Alternatives considered**:
  - Display a modal or overlay for errors: dismissed as too heavy for this lightweight onboarding route.
