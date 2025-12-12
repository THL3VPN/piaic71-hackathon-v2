# Feature Specification: Interactive CLI Todo App

**Feature Branch**: `001-interactive-todo-cli`  
**Created**: 2025-12-12  
**Status**: Draft  
**Input**: Interactive command-line todo application with single entry (`python main.py`), menu-driven flows (view, add, update, delete, toggle complete, exit), in-memory tasks, graceful error handling, and fully tested core logic.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently

  Testing is written first (pytest) to drive implementation; capture expected coverage impact so the 80% project floor is preserved.
-->

### User Story 1 - Start and view tasks (Priority: P1)

New or returning user launches the app, sees the main menu, and can view the current task list (including empty state) without restarting the app.

**Why this priority**: Establishes entrypoint and visibility of work; all other actions depend on a stable menu and view flow.

**Independent Test**: Launch the app, navigate to “View tasks,” observe empty list message or existing tasks table, return automatically to the main menu.

**Acceptance Scenarios**:

1. **Given** the app is started, **When** the user chooses “View tasks,” **Then** a list/table shows each task’s ID/index, title, and completion status (or a clear empty-state message).
2. **Given** no tasks exist, **When** the user views tasks, **Then** the app shows an empty-state message and returns to the main menu without exiting.

---

### User Story 2 - Add tasks via menu (Priority: P1)

User adds tasks from the main menu, providing a non-empty title, sees confirmation, and can view the new task in the list during the same session.

**Why this priority**: Task creation is the core value; it must be quick, validated, and reflected immediately.

**Independent Test**: From the main menu, choose “Add task,” enter a title, see a success message, and verify the task appears in “View tasks” with a unique identifier.

**Acceptance Scenarios**:

1. **Given** the app is running, **When** the user selects “Add task” and enters a non-empty title, **Then** the task is created with a unique ID/index, defaults to incomplete, and the app returns to the main menu.
2. **Given** the user enters an empty title, **When** they submit, **Then** the app shows a validation message, does not create a task, and returns to the main menu without crashing.

---

### User Story 3 - Manage existing tasks (Priority: P2)

User updates, deletes, or toggles completion for a task by ID/index, with clear feedback and resilience to invalid selections.

**Why this priority**: Keeps tasks accurate and useful; users must correct or complete items without restarting.

**Independent Test**: Add a task, then update its title, toggle completion, delete it, and confirm each action reflects in the list while the app continues running.

**Acceptance Scenarios**:

1. **Given** a task exists, **When** the user selects “Update task” and provides its ID/index with a new non-empty title, **Then** the task title changes, a confirmation displays, and the app returns to the main menu.
2. **Given** a task exists, **When** the user selects “Mark complete/incomplete” with its ID/index, **Then** the status toggles, the list reflects the change, and the app remains running.
3. **Given** a task exists, **When** the user selects “Delete task” with its ID/index, **Then** the task is removed, the list updates, and the app returns to the main menu.
4. **Given** a user provides an invalid ID/index for update/delete/toggle, **When** the action is attempted, **Then** the app shows a “task not found” message and stays on the main menu.

### Edge Cases

- Viewing tasks when none exist shows a clear empty-state message and keeps the menu available.
- Adding a task with an empty or whitespace-only title is rejected with a friendly prompt; no task is created.
- Update/Delete/Toggle with an out-of-range or non-numeric ID/index returns a “task not found” message without exiting.
- Repeated toggles flip completion status reliably within the same session.
- Rapid consecutive actions (e.g., add then delete) leave the in-memory list consistent and the menu responsive.
- Exit choice cleanly stops the loop without leaving partial actions.

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
  Align with project standards: Python 3.12+, type hints everywhere, dataclasses for structured data, pytest for testing (TDD), and coverage ≥80%.
-->

### Functional Requirements

- **FR-001**: The app MUST launch from a single entrypoint (`main.py`) into an interactive main menu that remains available until the user chooses Exit.
- **FR-002**: The system MUST maintain an in-memory list of tasks for the current session; no file system or database persistence is used.
- **FR-003**: The system MUST create a task with a non-empty title, assign it a unique ID/index, and default status to incomplete.
- **FR-004**: The system MUST display tasks in a clear list showing ID/index, title, and completion status, and handle empty lists gracefully.
- **FR-005**: The system MUST update a task’s title when provided a valid ID/index and non-empty new title; it MUST report “task not found” otherwise.
- **FR-006**: The system MUST delete a task when provided a valid ID/index and report “task not found” otherwise.
- **FR-007**: The system MUST toggle a task’s completion status when provided a valid ID/index and report “task not found” otherwise.
- **FR-008**: After every action (view, add, update, delete, toggle), the user MUST be returned to the main menu without restarting the app.
- **FR-009**: Core task operations (create, read, update, delete, toggle) MUST be separated from the interactive UI to enable isolated testing.
- **FR-010**: The system MUST handle invalid inputs (empty titles, malformed IDs) without crashing and provide user-friendly messages.

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item with fields: unique ID/index (stable within session), title (non-empty string), completion status (complete/incomplete).
- **Session Task List**: In-memory collection of tasks for the active run; supports lookup by ID/index and reflects updates, deletions, and toggles immediately.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
  Include verification signals for TDD (tests written first), type correctness, and maintaining ≥80% coverage alongside feature-specific outcomes.
-->

### Measurable Outcomes

- **SC-001**: Users can launch the app and perform any main-menu action (view, add, update, delete, toggle) without restarting, returning to the menu after each action within one step.
- **SC-002**: Task lists consistently show ID/index, title, and completion status with clear empty-state messaging when no tasks exist.
- **SC-003**: Invalid inputs (empty title, bad ID/index) result in user-friendly messages and the app remains operational in 100% of tested cases.
- **SC-004**: Overall test coverage is ≥80%, with 100% coverage for core task operations; all tests pass.
- **SC-005**: After any single-session sequence of add/update/toggle/delete actions, the in-memory task list reflects the correct state without data loss during that session.
