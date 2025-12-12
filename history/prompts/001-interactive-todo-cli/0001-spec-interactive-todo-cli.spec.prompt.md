---
id: 0001
title: spec-interactive-todo-cli
stage: spec
date: 2025-12-12
surface: cli
model: GPT-4.1 (Codex)
feature: 001-interactive-todo-cli
branch: 001-interactive-todo-cli
user: aie
command: Generate feature spec and checklist for interactive CLI todo app
labels: [spec, requirements, todo]
links:
  spec: specs/001-interactive-todo-cli/spec.md
  ticket: none
  adr: none
  pr: none
files:
  - specs/001-interactive-todo-cli/spec.md
  - specs/001-interactive-todo-cli/checklists/requirements.md
tests:
  - not run (specification-only change)
---

## Prompt

```
## User Input

```text
Feature: Interactive command-line todo application (single-file entry, in-memory) 1 User journeys: 1.1 Run the app using `python main.py` 1.2 See all available options in a main menu (View, Add, Update, Delete, Mark Complete, Exit) 1.3 Select actions interactively and return to the main menu after each action 1.4 Manage tasks without restarting the app 2 Acceptance criteria: 2.1 The entire app runs from a single entry file: `main.py` 2.2 Tasks are stored in memory only (no file system, no database) 2.3 The app is menu-driven (not one command per action) 2.4 All five basic features are implemented: 2.4.1 Add task (non-empty title required) 2.4.2 View task list (ID/index, title, completion status) 2.4.3 Update task (by ID/index) 2.4.4 Delete task (by ID/index) 2.4.5 Mark task complete/incomplete (toggle) 2.5 Invalid task selections are handled gracefully without crashing 2.6 Core logic is separated from the UI for testability 2.7 All core logic has full test coverage with pytest 2.8 Code uses Python 3.12+ type hints and clear docstrings 3 Success metrics: 3.1 ≥80% overall test coverage (100% for core task logic) 3.2 All tests pass 3.3 Code follows our constitution rules
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/sp.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `Feature: Interactive command-line todo application (single-file entry, in-memory) 1 User journeys: 1.1 Run the app using `python main.py` 1.2 See all available options in a main menu (View, Add, Update, Delete, Mark Complete, Exit) 1.3 Select actions interactively and return to the main menu after each action 1.4 Manage tasks without restarting the app 2 Acceptance criteria: 2.1 The entire app runs from a single entry file: `main.py` 2.2 Tasks are stored in memory only (no file system, no database) 2.3 The app is menu-driven (not one command per action) 2.4 All five basic features are implemented: 2.4.1 Add task (non-empty title required) 2.4.2 View task list (ID/index, title, completion status) 2.4.3 Update task (by ID/index) 2.4.4 Delete task (by ID/index) 2.4.5 Mark task complete/incomplete (toggle) 2.5 Invalid task selections are handled gracefully without crashing 2.6 Core logic is separated from the UI for testability 2.7 All core logic has full test coverage with pytest 2.8 Code uses Python 3.12+ type hints and clear docstrings 3 Success metrics: 3.1 ≥80% overall test coverage (100% for core task logic) 3.2 All tests pass 3.3 Code follows our constitution rules` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

Given that feature description, do this:

1. **Generate a concise short name** (2-4 words) for the branch:
   - Analyze the feature description and extract the most meaningful keywords
   - Create a 2-4 word short name that captures the essence of the feature
   - Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
   - Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)
   - Keep it concise but descriptive enough to understand the feature at a glance
   - Examples:
     - "I want to add user authentication" → "user-auth"
     - "Implement OAuth2 integration for the API" → "oauth2-api-integration"
     - "Create a dashboard for analytics" → "analytics-dashboard"
     - "Fix payment processing timeout bug" → "fix-payment-timeout"

2. **Check for existing branches before creating new one**:
   
   a. First, fetch all remote branches to ensure we have the latest information:
      ```bash
      git fetch --all --prune
      ```
   
   b. Find the highest feature number across all sources for the short-name:
      - Remote branches: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - Local branches: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - Specs directories: Check for directories matching `specs/[0-9]+-<short-name>`
   
   c. Determine the next available number:
      - Extract all numbers from all three sources
      - Find the highest number N
      - Use N+1 for the new branch number
   
   d. Run the script `.specify/scripts/bash/create-new-feature.sh --json "Feature: Interactive command-line todo application (single-file entry, in-memory) 1 User journeys: 1.1 Run the app using `python main.py` 1.2 See all available options in a main menu (View, Add, Update, Delete, Mark Complete, Exit) 1.3 Select actions interactively and return to the main menu after each action 1.4 Manage tasks without restarting the app 2 Acceptance criteria: 2.1 The entire app runs from a single entry file: `main.py` 2.2 Tasks are stored in memory only (no file system, no database) 2.3 The app is menu-driven (not one command per action) 2.4 All five basic features are implemented: 2.4.1 Add task (non-empty title required) 2.4.2 View task list (ID/index, title, completion status) 2.4.3 Update task (by ID/index) 2.4.4 Delete task (by ID/index) 2.4.5 Mark task complete/incomplete (toggle) 2.5 Invalid task selections are handled gracefully without crashing 2.6 Core logic is separated from the UI for testability 2.7 All core logic has full test coverage with pytest 2.8 Code uses Python 3.12+ type hints and clear docstrings 3 Success metrics: 3.1 ≥80% overall test coverage (100% for core task logic) 3.2 All tests pass 3.3 Code follows our constitution rules"` with the calculated number and short-name:
      - Pass `--number N+1` and `--short-name "your-short-name"` along with the feature description
      - Bash example: `.specify/scripts/bash/create-new-feature.sh --json "Feature: Interactive command-line todo application (single-file entry, in-memory) 1 User journeys: 1.1 Run the app using `python main.py` 1.2 See all available options in a main menu (View, Add, Update, Delete, Mark Complete, Exit) 1.3 Select actions interactively and return to the main menu after each action 1.4 Manage tasks without restarting the app 2 Acceptance criteria: 2.1 The entire app runs from a single entry file: `main.py` 2.2 Tasks are stored in memory only (no file system, no database) 2.3 The app is menu-driven (not one command per action) 2.4 All five basic features are implemented: 2.4.1 Add task (non-empty title required) 2.4.2 View task list (ID/index, title, completion status) 2.4.3 Update task (by ID/index) 2.4.4 Delete task (by ID/index) 2.4.5 Mark task complete/incomplete (toggle) 2.5 Invalid task selections are handled gracefully without crashing 2.6 Core logic is separated from the UI for testability 2.7 All core logic has full test coverage with pytest 2.8 Code uses Python 3.12+ type hints and clear docstrings 3 Success metrics: 3.1 ≥80% overall test coverage (100% for core task logic) 3.2 All tests pass 3.3 Code follows our constitution rules" --json --number 5 --short-name "user-auth" "Add user authentication"`
      - PowerShell example: `.specify/scripts/bash/create-new-feature.sh --json "Feature: Interactive command-line todo application (single-file entry, in-memory) 1 User journeys: 1.1 Run the app using `python main.py` 1.2 See all available options in a main menu (View, Add, Update, Delete, Mark Complete, Exit) 1.3 Select actions interactively and return to the main menu after each action 1.4 Manage tasks without restarting the app 2 Acceptance criteria: 2.1 The entire app runs from a single entry file: `main.py` 2.2 Tasks are stored in memory only (no file system, no database) 2.3 The app is menu-driven (not one command per action) 2.4 All five basic features are implemented: 2.4.1 Add task (non-empty title required) 2.4.2 View task list (ID/index, title, completion status) 2.4.3 Update task (by ID/index) 2.4.4 Delete task (by ID/index) 2.4.5 Mark task complete/incomplete (toggle) 2.5 Invalid task selections are handled gracefully without crashing 2.6 Core logic is separated from the UI for testability 2.7 All core logic has full test coverage with pytest 2.8 Code uses Python 3.12+ type hints and clear docstrings 3 Success metrics: 3.1 ≥80% overall test coverage (100% for core task logic) 3.2 All tests pass 3.3 Code follows our constitution rules" -Json -Number 5 -ShortName "user-auth" "Add user authentication"`
   
   **IMPORTANT**:
   - Check all three sources (remote branches, local branches, specs directories) to find the highest number
   - Only match branches/directories with the exact short-name pattern
   - If no existing branches/directories found with this short-name, start with number 1
   - You must only ever run this script once per feature
   - The JSON is provided in the terminal as output - always refer to it to get the actual content you're looking for
   - The JSON output will contain BRANCH_NAME and SPEC_FILE paths
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot")

3. Load `.specify/templates/spec-template.md` to understand required sections.

4. Follow this execution flow:

    1. Parse user description from Input
       If empty: ERROR "No feature description provided"
    2. Extract key concepts from description
       Identify: actors, actions, data, constraints
    3. For unclear aspects:
       - Make informed guesses based on context and industry standards
       - Only mark with [NEEDS CLARIFICATION: specific question] if:
         - The choice significantly impacts feature scope or user experience
         - Multiple reasonable interpretations exist with different implications
         - No reasonable default exists
       - **LIMIT: Maximum 3 [NEEDS CLARIFICATION] markers total**
       - Prioritize clarifications by impact: scope > security/privacy > user experience > technical details
    4. Fill User Scenarios & Testing section
       If no clear user flow: ERROR "Cannot determine user scenarios"
    5. Generate Functional Requirements
       Each requirement must be testable
       Use reasonable defaults for unspecified details (document assumptions in Assumptions section)
    6. Define Success Criteria
       Create measurable, technology-agnostic outcomes
       Include both quantitative metrics (time, performance, volume) and qualitative measures (user satisfaction, task completion)
       Each criterion must be verifiable without implementation details
    7. Identify Key Entities (if data involved)
    8. Return: SUCCESS (spec ready for planning)

5. Write the specification to SPEC_FILE using the template structure, replacing placeholders with concrete details derived from the feature description (arguments) while preserving section order and headings.

6. **Specification Quality Validation**: After writing the initial spec, validate it against quality criteria:

   a. **Create Spec Quality Checklist**: Generate a checklist file at `FEATURE_DIR/checklists/requirements.md` using the checklist template structure with these validation items:

      ```markdown
      # Specification Quality Checklist: [FEATURE NAME]
      
      **Purpose**: Validate specification completeness and quality before proceeding to planning
      **Created**: [DATE]
      **Feature**: [Link to spec.md]
      
      ## Content Quality
      
      - [ ] No implementation details (languages, frameworks, APIs)
      - [ ] Focused on user value and business needs
      - [ ] Written for non-technical stakeholders
      - [ ] All mandatory sections completed
      
      ## Requirement Completeness
      
      - [ ] No [NEEDS CLARIFICATION] markers remain
      - [ ] Requirements are testable and unambiguous
      - [ ] Success criteria are measurable
      - [ ] Success criteria are technology-agnostic (no implementation details)
      - [ ] All acceptance scenarios are defined
      - [ ] Edge cases are identified
      - [ ] Scope is clearly bounded
      - [ ] Dependencies and assumptions identified
      
      ## Feature Readiness
      
      - [ ] All functional requirements have clear acceptance criteria
      - [ ] User scenarios cover primary flows
      - [ ] Feature meets measurable outcomes defined in Success Criteria
      - [ ] No implementation details leak into specification
      
      ## Notes
      
      - Items marked incomplete require spec updates before `/sp.clarify` or `/sp.plan`
      ```

   b. **Run Validation Check**: Review the spec against each checklist item:
      - For each item, determine if it passes or fails
      - Document specific issues found (quote relevant spec sections)

   c. **Handle Validation Results**:

      - **If all items pass**: Mark checklist complete and proceed to step 6

      - **If items fail (excluding [NEEDS CLARIFICATION])**:
        1. List the failing items and specific issues
        2. Update the spec to address each issue
        3. Re-run validation until all items pass (max 3 iterations)
        4. If still failing after 3 iterations, document remaining issues in checklist notes and warn user

      - **If [NEEDS CLARIFICATION] markers remain**:
        1. Extract all [NEEDS CLARIFICATION: ...] markers from the spec
        2. **LIMIT CHECK**: If more than 3 markers exist, keep only the 3 most critical (by scope/security/UX impact) and make informed guesses for the rest
        3. For each clarification needed (max 3), present options to user in this format:

           ```markdown
           ## Question [N]: [Topic]
           
           **Context**: [Quote relevant spec section]
           
           **What we need to know**: [Specific question from NEEDS CLARIFICATION marker]
           
           **Suggested Answers**:
           
           | Option | Answer | Implications |
           |--------|--------|--------------|
           | A      | [First suggested answer] | [What this means for the feature] |
           | B      | [Second suggested answer] | [What this means for the feature] |
           | C      | [Third suggested answer] | [What this means for the feature] |
           | Custom | Provide your own answer | [Explain how to provide custom input] |
           
           **Your choice**: _[Wait for user response]_
           ```

        4. **CRITICAL - Table Formatting**: Ensure markdown tables are properly formatted:
           - Use consistent spacing with pipes aligned
           - Each cell should have spaces around content: `| Content |` not `|Content|`
           - Header separator must have at least 3 dashes: `|--------|`
           - Test that the table renders correctly in markdown preview
        5. Number questions sequentially (Q1, Q2, Q3 - max 3 total)
        6. Present all questions together before waiting for responses
        7. Wait for user to respond with their choices for all questions (e.g., "Q1: A, Q2: Custom - [details], Q3: B")
        8. Update the spec by replacing each [NEEDS CLARIFICATION] marker with the user's selected or provided answer
        9. Re-run validation after all clarifications are resolved

   d. **Update Checklist**: After each validation iteration, update the checklist file with current pass/fail status

7. Report completion with branch name, spec file path, checklist results, and readiness for the next phase (`/sp.clarify` or `/sp.plan`).

**NOTE:** The script creates and checks out the new branch and initializes the spec file before writing.
```

## Response snapshot

- Created feature branch `001-interactive-todo-cli`, filled spec with user stories, functional requirements, edge cases, and measurable outcomes for an interactive menu-driven in-memory todo app; removed placeholders and aligned with constitution gates; generated quality checklist with all items passing.

## Outcome

- ✅ Impact: Spec ready for planning with validation checklist completed
- 🧪 Tests: Not run (specification-only)
- 📁 Files: specs/001-interactive-todo-cli/spec.md; specs/001-interactive-todo-cli/checklists/requirements.md
- 🔁 Next prompts: /sp.plan (implementation plan) if no clarifications needed
- 🧠 Reflection: Kept tech/tool mentions out of spec while preserving entrypoint and menu requirements from user acceptance criteria.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
