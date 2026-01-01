# Implementation Plan: Frontend Chat UI Integration

**Branch**: `016-chat-ui-integration` | **Date**: 2026-01-01 | **Spec**: /home/aie/all_data/piaic71-hackathon-v2/specs/016-chat-ui-integration/spec.md
**Input**: Feature specification from `/home/aie/all_data/piaic71-hackathon-v2/specs/016-chat-ui-integration/spec.md`

**Note**: This plan follows the Spec-Driven Development workflow and the project constitution.

## Summary

Add a chat UI to the frontend using OpenAI ChatKit so authenticated users can send messages to `/api/chat`, persist and reuse `conversation_id`, render history, and optionally view tool call metadata without altering backend behavior.

## Technical Context

**Language/Version**: TypeScript 5.3 + React 18.3 (Next.js App Router)  
**Primary Dependencies**: next (App Router), react, OpenAI ChatKit, testing-library, vitest  
**Storage**: Browser local storage for `active_conversation_id`; backend remains source of truth for chat history  
**Testing**: vitest + @testing-library/react (frontend), pytest coverage remains ≥80%  
**Target Platform**: Modern browsers (desktop + mobile)  
**Project Type**: Web application (Next.js frontend + existing FastAPI backend)  
**Performance Goals**: Visible loading state within 250 ms; UI remains responsive during network waits  
**Constraints**: No backend changes; keep auth flow intact; no streaming; no new chat listing UI; maintain coverage ≥80%  
**Scale/Scope**: Single chat surface with one active conversation per user session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Tests are defined first (vitest for frontend), executed to red, then implemented to green; plan documents TDD for UI flows.
- Python 3.12+ with type hints is unchanged for backend; frontend uses TypeScript types.
- UV remains for backend dependency management; frontend uses npm per existing setup.
- Quality bars: all planned changes must maintain ≥80% coverage and preserve existing behavior.

## Project Structure

### Documentation (this feature)

```text
/home/aie/all_data/piaic71-hackathon-v2/specs/016-chat-ui-integration/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
└── tasks.md
```

### Source Code (repository root)

```text
/home/aie/all_data/piaic71-hackathon-v2/src/
├── api/
├── services/
└── models/

/home/aie/all_data/piaic71-hackathon-v2/frontend/
├── app/
├── lib/
└── tests/
```

**Structure Decision**: Web application with existing FastAPI backend and Next.js frontend. Chat UI lives under `frontend/app/` with shared utilities in `frontend/lib/` and tests under `frontend/tests/`.

## Complexity Tracking

No constitution violations anticipated for this feature.

## Phase 0: Outline & Research

### Research Tasks

- Confirm OpenAI ChatKit integration patterns for Next.js App Router.
- Validate conversation_id persistence and history load expectations for UX.

### Research Output

See `/home/aie/all_data/piaic71-hackathon-v2/specs/016-chat-ui-integration/research.md`.

## Phase 1: Design & Contracts

### Architecture Sketch

- Chat UI renders message list, composer, loading/error states.
- Conversation state stored in React state and local storage.
- History fetched on open via `/api/conversations/{conversation_id}/messages`.
- `/api/chat` used for message send and tool call capture.

### API Contracts

See `/home/aie/all_data/piaic71-hackathon-v2/specs/016-chat-ui-integration/contracts/chat-ui.openapi.yaml`.

### Data Model

See `/home/aie/all_data/piaic71-hackathon-v2/specs/016-chat-ui-integration/data-model.md`.

### Quickstart

See `/home/aie/all_data/piaic71-hackathon-v2/specs/016-chat-ui-integration/quickstart.md`.

## Phase 1: Agent Context Update

Run `/home/aie/all_data/piaic71-hackathon-v2/.specify/scripts/bash/update-agent-context.sh codex` after the plan is finalized.
