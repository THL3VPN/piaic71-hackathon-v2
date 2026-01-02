# Implementation Plan: Chat Widget Polish

**Branch**: `018-chat-widget-polish` | **Date**: 2026-01-02 | **Spec**: specs/018-chat-widget-polish/spec.md
**Input**: Feature specification from `/specs/018-chat-widget-polish/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Polish the existing chat widget UI to match a ChatGPT-style experience: clean layout, consistent typography, message bubble alignment, always-visible composer with a circular send button, no horizontal scrolling, and concise assistant replies (handled by existing backend behavior).

## Technical Context

**Language/Version**: TypeScript 5.3 (Next.js App Router)  
**Primary Dependencies**: React 18.3, Next.js (canary), Vitest, Testing Library; add Tailwind CSS for styling utilities  
**Storage**: Browser localStorage (conversation id); backend remains source of truth  
**Testing**: Vitest + Testing Library (frontend)  
**Target Platform**: Modern desktop browsers (Chrome, Edge, Firefox, Safari)  
**Project Type**: Web application (frontend-only changes)  
**Performance Goals**: Smooth scrolling and UI responsiveness on standard laptops  
**Constraints**: No backend changes, no new endpoints, no horizontal scrolling, maintain existing auth flow, preserve existing tests and coverage  
**Scale/Scope**: Single widget UI polish, no new screens

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first and run in the frontend test suite (Vitest); no Python changes in this step.
- Python 3.12+ with type hints is not impacted; this step is frontend-only.
- UV/pytest gates are not applicable to frontend-only changes; existing frontend quality gates remain in effect.
- ADR required for material decisions: adopting Tailwind CSS is a new dependency and should be tracked before implementation.

## Project Structure

### Documentation (this feature)

```text
specs/018-chat-widget-polish/
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
│   ├── components/
│   ├── chat/
│   └── tasks/
├── lib/
└── tests/
```

**Structure Decision**: Web application layout under `frontend/` with React components in `frontend/app/components` and tests in `frontend/tests`.

## Phase 0: Outline & Research

### Unknowns & Decisions

- **Decision**: Adopt Tailwind CSS for widget styling.
  - **Rationale**: Utility classes allow rapid, consistent UI polish and easy control of spacing, sizing, and overflow constraints.
  - **Alternatives considered**: Extend existing CSS in `globals.css` only; use CSS modules per component.

- **Decision**: Concise responses requirement will be satisfied by existing backend behavior (no frontend truncation or summarization).
  - **Rationale**: Backend behavior is out of scope; avoid altering message content in the UI.
  - **Alternatives considered**: Client-side truncation (rejected due to content loss).

### Output

- `specs/018-chat-widget-polish/research.md`

## Phase 1: Design & Contracts

### Data Model

Document the UI-facing shape for chat messages and conversation identifiers (no new backend entities).

### API Contracts

Document existing chat endpoints used by the UI in a lightweight OpenAPI file (no changes to backend contracts).

### Quickstart

Provide steps to run the frontend and validate the widget layout and behavior.

### Output

- `specs/018-chat-widget-polish/data-model.md`
- `specs/018-chat-widget-polish/contracts/chat-widget-polish.openapi.yaml`
- `specs/018-chat-widget-polish/quickstart.md`

### Agent Context Update

Run: `/home/aie/all_data/piaic71-hackathon-v2/.specify/scripts/bash/update-agent-context.sh codex`

## Phase 1 Re-Check: Constitution Check

- Frontend-only change remains compliant with project constraints.
- ADR required for Tailwind adoption remains outstanding before implementation.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Tailwind dependency | Required to meet UI polish goals quickly and consistently | Custom CSS only would be slower and more error-prone for rapid iteration |
