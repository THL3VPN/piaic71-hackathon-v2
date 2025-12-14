# Feature Specification: Frontend bootstrap with backend connectivity

**Feature Branch**: `001-frontend-health`  
**Created**: 2024-05-08  
**Status**: Draft  
**Input**: User description: "Feature: Frontend bootstrap with backend connectivity User journeys 1.1 Start the frontend locally 1.2 Open the app in the browser via http://localhost:<port> 1.3 The homepage calls the backend /health endpoint and shows the result Acceptance criteria 2.1 Frontend is built using Next.js 16+ with App Router 2.2 The frontend starts successfully (e.g., http://localhost:3000) 2.3 The homepage loads without runtime errors 2.4 The frontend makes an HTTP request to the backend (e.g., GET http://localhost:8000/health) 2.5 The backend response is displayed clearly on the page (e.g., “Backend: OK”) 2.6 CORS or proxy configuration is set so the request succeeds locally 2.7 README includes how to run both apps locally (ports + commands) 2.8 No authentication is required 2.9 No task CRUD UI is required in this step Success metrics 3.1 Visiting http://localhost:<frontend_port> shows the UI and backend health status 3.2 Backend + frontend can run at the same time with no errors 3.3 (Optional) Frontend smoke test passes (or at least Next build succeeds)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Display backend health (Priority: P1)

Visitors open the Next.js App Router homepage, which immediately calls the backend `/health` endpoint and displays the result in a labeled card.

**Why this priority**: The health indicator proves the new frontend communicates with the backend before introducing any task-related UI, so it is the minimal meaningful deliverable.

**Independent Test**: Start the Next.js dev server and the backend, load `http://localhost:3000`, and verify the “Backend: OK” or error card renders without crash.

**Acceptance Scenarios**:

1. **Given** the backend is healthy and running on port 8000, **When** the homepage loads, **Then** the card shows the backend response text.
2. **Given** the backend is down or slow, **When** the homepage loads, **Then** the component displays a graceful error (e.g., “Backend: unavailable”) while the page remains interactive.

---

### User Story 2 - Document the dual-stack run (Priority: P2)

The README lists the commands and ports required to run both the Next.js frontend and the uvicorn backend simultaneously, including any environment variables such as `NEXT_PUBLIC_BACKEND_URL`.

**Why this priority**: Accurate documentation completes the bootstrap by making the integration repeatable for other developers or testers.

**Independent Test**: Follow the README instructions and confirm both apps start on their respective ports with the described commands.

**Acceptance Scenarios**:

1. **Given** a fresh repository clone, **When** a developer reads the README, **Then** they know the commands/ports (e.g., `npm run dev` for frontend, `uv run uvicorn src.main:app --reload --port 8000` for backend).

---

### User Story 3 - Resolve CORS/proxy during development (Priority: P3)

The frontend configures a Next.js proxy or documents CORS header expectations so the browser fetch to `http://localhost:8000/health` succeeds locally without manual tweaks.

**Why this priority**: Browser-based health checks will fail if cross-origin restrictions block the call, so fixing this is necessary for the UI to surface backend status.

**Independent Test**: Run both servers, load the homepage, and verify the browser console lists a successful request instead of a CORS error.

**Acceptance Scenarios**:

1. **Given** the frontend is on port 3000 and the backend on 8000, **When** the homepage tries to fetch `/health`, **Then** the request completes successfully.

---

### Edge Cases

- The backend returns 5xx or times out; the frontend should display “Backend: unavailable” plus the error message but must not throw runtime errors.
- The browser flags CORS issues during development; the UI should continue rendering and log instructions rather than breaking.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The homepage is a Next.js 16+ App Router page that renders without runtime errors.
- **FR-002**: The homepage issues a GET to the backend health endpoint (`http://localhost:8000/health` or configured URL) as soon as the page loads.
- **FR-003**: The backend response (success or failure) is displayed in a labeled component such as “Backend: OK” or “Backend: unavailable”.
- **FR-004**: Development configuration includes a proxy rewrites table or clearly spelled out CORS headers so the browser request succeeds locally.
- **FR-005**: README instructions describe how to start both frontend and backend, mention ports, and call out any necessary environment variables (e.g., `NEXT_PUBLIC_BACKEND_URL`).

### Key Entities *(include if feature involves data)*

- **HealthStatus**: Represents the backend response payload (status string + optional message); the frontend only needs the string to display success or failure.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Visiting `http://localhost:3000` completes the backend health request within 5 seconds and presents the returned string or a user-friendly error.
- **SC-002**: Running both servers simultaneously produces no runtime errors in the frontend console and the health card updates accordingly.
- **SC-003**: README documents the commands/ports needed for both apps so a teammate can reproduce the local deployment without additional guidance.
- **SC-004**: Next.js dev server passes `npm run dev` (or `next dev`), demonstrating the project builds successfully during this bootstrap.
