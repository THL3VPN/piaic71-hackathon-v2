# Research: Chat Widget Polish

## Decision 1: Use Tailwind CSS for widget styling

**Decision**: Adopt Tailwind CSS utility classes for the chat widget UI.

**Rationale**: The step requires precise control over spacing, alignment, and responsive behavior with a clean, consistent visual system. Tailwind utilities enable faster iteration and consistent typography/spacing without scattered custom CSS.

**Alternatives considered**:
- Extend `globals.css` only: possible but slower to iterate and harder to keep consistency.
- CSS modules per component: more structure, but introduces more files and slower iterations for tight UI polish work.

## Decision 2: Concise replies handled by backend

**Decision**: Do not alter assistant content in the UI; rely on existing backend prompt behavior for conciseness.

**Rationale**: Backend changes are out of scope for this step; UI should not truncate or rewrite assistant responses.

**Alternatives considered**:
- Client-side truncation or summarization: rejected due to potential loss of meaning and inconsistency with server truth.
