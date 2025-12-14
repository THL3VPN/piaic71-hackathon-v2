## Research – Frontend health bootstrap

### Decision 1: Next.js App Router for landing page
- **Decision**: Build the bootstrap UI with Next.js 16+ App Router to align with modern Next.js structure and support server/client boundaries immediately.
- **Rationale**: App Router simplifies routing and layout composition, and the spec explicitly calls for Next.js 16+; sticking with it avoids later migration overhead.
- **Alternatives considered**:
  - Pages Router: rejected because Next.js is explicitly versioned; App Router matches current Next.js best practices.
  - Vanilla HTML + fetch: rejected because it lacks the requested framework and tooling benefits.

### Decision 2: Health fetch via client-side component with proxy/rewrites
- **Decision**: Perform the `/health` request client-side inside a React component using `fetch` and configure `next.config.js` rewrites to proxy `/api/health` to the backend (or document how to set `NEXT_PUBLIC_BACKEND_URL`).
- **Rationale**: Client-side fetch keeps the indicator fresh and easy to test while proxies avoid CORS noise during development; rewriting ensures the browser hits the same origin for Next dev server.
- **Alternatives considered**:
  - Server-side fetch: would require additional backend wiring and produce identical UI, so skipped to keep bootstrap simple.
  - CORS header adjustments only: acceptable but harder to guarantee across environments, so proxy rewrites recommended.

### Decision 3: README-driven dev workflow
- **Decision**: Document both the backend UV command and the frontend Next command plus ports/URLs in README for reproducible local runs.
- **Rationale**: Without clear instructions, the dual-app bootstrap is hard to replicate; docs ensure manual verification success metrics are met.
- **Alternatives considered**:
  - Inline comments only: rejected because they can be missed; README offers a single source of truth.

### Decision 4: Vitest + Testing Library for UI coverage
- **Decision**: Use Vitest with DOM+Testing Library to cover the health card behavior instead of wiring a heavier Jest setup.
- **Rationale**: Vitest integrates well with Vite/Next tooling, provides jsdom by default, and keeps test runs fast; mocking `fetch` in `tests/page.test.tsx` gives us the failing/tested flows requested in the spec.
- **Alternatives considered**:
  - Jest + React Testing Library: more configuration required; Vitest already supports ESM and shares API with Jest, so it's more lightweight.
