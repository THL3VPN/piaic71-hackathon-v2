---
id: 0003
title: generate-agent-behavior-tasks
stage: tasks
date: 2026-01-02T02:08:41+05:00
surface: cli
model: gpt-5
feature: 014-agent-behavior-validation
branch: 014-agent-behavior-validation
user: user
command: /sp.tasks
labels: [tasks, step5, agent-behavior]
links:
  spec: /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/aie/all_data/piaic71-hackathon-v2/specs/014-agent-behavior-validation/tasks.md
tests: []
---

## Prompt

## User Input

```text

```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/check-prerequisites.sh --json` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load design documents**: Read from FEATURE_DIR:
   - **Required**: plan.md (tech stack, libraries, structure), spec.md (user stories with priorities)
   - **Optional**: data-model.md (entities), contracts/ (API endpoints), research.md (decisions), quickstart.md (test scenarios)
   - Note: Not all projects have all documents. Generate tasks based on what's available.

3. **Execute task generation workflow**:
   - Load plan.md and extract tech stack, libraries, project structure
   - Load spec.md and extract user stories with their priorities (P1, P2, P3, etc.)
   - If data-model.md exists: Extract entities and map to user stories
   - If contracts/ exists: Map endpoints to user stories
   - If research.md exists: Extract decisions for setup tasks
   - Generate tasks organized by user story (see Task Generation Rules below)
   - Generate dependency graph showing user story completion order
   - Create parallel execution examples per user story
   - Validate task completeness (each user story has all needed tasks, independently testable)

4. **Generate tasks.md**: Use `.specify.specify/templates/tasks-template.md` as structure, fill with:
   - Correct feature name from plan.md
   - Phase 1: Setup tasks (project initialization)
   - Phase 2: Foundational tasks (blocking prerequisites for all user stories)
   - Phase 3+: One phase per user story (in priority order from spec.md)
   - Each phase includes: story goal, independent test criteria, tests (if requested), implementation tasks
   - Final Phase: Polish & cross-cutting concerns
   - All tasks must follow the strict checklist format (see Task Generation Rules below)
   - Clear file paths for each task
   - Dependencies section showing story completion order
   - Parallel execution examples per story
   - Implementation strategy section (MVP first, incremental delivery)

5. **Report**: Output path to generated tasks.md and summary:
   - Total task count
   - Task count per user story
   - Parallel opportunities identified
   - Independent test criteria for each story
   - Suggested MVP scope (typically just User Story 1)
   - Format validation: Confirm ALL tasks follow the checklist format (checkbox, ID, labels, file paths)

## Response snapshot

Generated the task breakdown for agent behavior validation with tests-first steps per user story.

## Outcome

- ✅ Impact: Tasks ready for execution with TDD and clear dependencies.
- 🧪 Tests: Not run (task generation only).
- 📁 Files: specs/014-agent-behavior-validation/tasks.md
- 🔁 Next prompts: Proceed to implementation (`/sp.execute`).
- 🧠 Reflection: Keep tasks small and aligned to behavior scenarios.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not run
- Prompt variant (if applicable): None
- Next experiment (smallest change to try): N/A
