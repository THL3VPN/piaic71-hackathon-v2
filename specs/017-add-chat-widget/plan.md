# Implementation Plan: Floating Chat Widget UX

**Branch**: `017-add-chat-widget` | **Date**: 2026-01-02 | **Spec**: specs/017-add-chat-widget/spec.md
**Input**: Feature specification from `/specs/017-add-chat-widget/spec.md`

## Summary

Replace the standalone chat experience with a bottom-right floating widget on authenticated pages, preserving existing chat behavior and persistence. The work is frontend-only: extract or wrap the existing chat UI into a toggleable widget, integrate it into the tasks page, and maintain conversation continuity and friendly UX states. Tests remain vitest-first (red/green/refactor) with coverage preserved.

## Technical Context

**Language/Version**: TypeScript 5.3 + React 18.3 (Next.js App Router)  
**Primary Dependencies**: Next.js, React, Testing Library, Vitest  
**Storage**: Browser storage for conversation identifier  
**Testing**: Vitest + Testing Library (tests written first)  
**Target Platform**: Modern browsers (desktop + mobile)  
**Project Type**: Web application (frontend-only change)  
**Performance Goals**: Widget opens within 200ms; message list scroll remains smooth under 200 messages  
**Constraints**: No backend changes; keep existing auth and chat contract; maintain existing tasks UI; keep coverage ≥80%  
**Scale/Scope**: Single floating widget integrated on authenticated pages, no multi-thread UI

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first and driven to red/green using the existing frontend test stack (Vitest + Testing Library).  
- Python 3.12+ and dataclass guidance does not apply (frontend-only scope).  
- Quality bars: coverage ≥80% maintained; no ADR needed (no material architecture change).  
- Tooling: npm for frontend dependencies; no changes to backend tooling.

## Project Structure

### Documentation (this feature)

```text
specs/017-add-chat-widget/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
frontend/
├── app/
│   ├── tasks/
│   │   └── page.tsx
│   └── components/        # new widget shell (if needed)
├── lib/
│   ├── chat.ts
│   ├── chatStorage.ts
│   └── auth.ts
└── tests/
    ├── chat-widget.test.tsx
    ├── chat-history.test.tsx
    └── chat-errors.test.tsx
```

**Structure Decision**: Frontend-only updates under `frontend/app/` and `frontend/lib/` with new widget component(s) and focused tests in `frontend/tests/`.

## Phase 0: Outline & Research

### Research Questions

- Confirm best practice for floating widget placement and overlay layering in the existing design system.
- Determine whether to reuse the current chat page markup or extract shared components for widget use.
- Define accessibility behaviors (focus management, Escape to close) consistent with current UI patterns.

### Research Output

Documented in `specs/017-add-chat-widget/research.md`.

## Phase 1: Design & Contracts

### Data Model

Define UI state shape for the widget, including:
- Widget open/closed state
- Conversation identifier persistence
- Message list with role and optional tool call details

Documented in `specs/017-add-chat-widget/data-model.md`.

### Contracts

Capture the client’s use of the existing chat service in an OpenAPI snippet for reference.  
Output to `specs/017-add-chat-widget/contracts/chat-widget.openapi.yaml`.

### Quickstart

Add a manual validation checklist for the widget flow in `specs/017-add-chat-widget/quickstart.md`.

## Phase 2: Task Planning (handled by /sp.tasks)

Generate tasks with TDD focus, small reversible steps, and explicit dependencies.

## Risks & Mitigations

- **Risk**: Widget overlays or z-index conflicts with existing layout.  
  **Mitigation**: Add a dedicated container with high z-index and verify on tasks page.
- **Risk**: Conversation state lost on close/open.  
  **Mitigation**: Persist identifier in storage and reload history on open.
- **Risk**: Accessibility regressions.  
  **Mitigation**: Add focus management and keyboard close behavior tests.

## Open Questions

None. All requirements are actionable within the current frontend scope.
