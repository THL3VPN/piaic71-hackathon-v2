# Research: Floating Chat Widget UX

## Decision 1: Widget placement and layering
- **Decision**: Use a fixed bottom-right container with a high z-index and a toggleable panel above it.
- **Rationale**: Matches common support-widget UX and avoids interference with existing layout.
- **Alternatives considered**: Inline chat panel within tasks page (rejected because it violates the floating widget requirement).

## Decision 2: Reuse existing chat UI logic
- **Decision**: Reuse existing chat message/rendering logic and wrap it in a widget shell.
- **Rationale**: Minimizes risk, preserves current behavior, and keeps changes localized.
- **Alternatives considered**: Rebuild a new message renderer (rejected due to regression risk).

## Decision 3: Accessibility behaviors
- **Decision**: Focus the input on open and support Escape to close.
- **Rationale**: Matches expected widget accessibility patterns and reduces friction.
- **Alternatives considered**: No focus management (rejected due to accessibility expectations).
