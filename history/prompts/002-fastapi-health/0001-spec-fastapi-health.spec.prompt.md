---
id: 0001
title: spec-fastapi-health
stage: spec
date: 2025-12-12
surface: cli
model: GPT-4.1 (Codex)
feature: 002-fastapi-health
branch: 002-fastapi-health
user: aie
command: Generate FastAPI health service spec and checklist
labels: [spec, requirements, backend]
links:
  spec: specs/002-fastapi-health/spec.md
  ticket: none
  adr: none
  pr: none
files:
  - specs/002-fastapi-health/spec.md
  - specs/002-fastapi-health/checklists/requirements.md
tests:
  - not run (spec-only)
---

## Prompt

```
## User Input

```text
Feature: Backend service bootstrap (FastAPI) User journeys 1.1 Start the backend service locally 1.2 Verify the service is running via a health endpoint Acceptance criteria 2.1 The backend is implemented using Python FastAPI 2.2 The service starts successfully using uvicorn 2.3 An HTTP endpoint GET /health is available 2.4 The /health endpoint returns HTTP 200 2.5 The response body is a simple JSON object (e.g. { status: ok }) 2.6 No authentication is required 2.7 No database connection is required 2.8 The endpoint is accessible via http://localhost:<port>/health 2.9 All code uses Python 3.13+ type hints and clear docstrings Success metrics 3.1 curl http://localhost:<port>/health returns HTTP 200 3.2 All pytest tests pass 3.3 Test coverage includes the /health endpoint 3.4 Code follows constitution rules
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

The text the user typed after `/sp.specify` in the triggering message **is** the feature description. Assume you always have it available in this conversation even if `Feature: Backend service bootstrap (FastAPI) User journeys 1.1 Start the backend service locally 1.2 Verify the service is running via a health endpoint Acceptance criteria 2.1 The backend is implemented using Python FastAPI 2.2 The service starts successfully using uvicorn 2.3 An HTTP endpoint GET /health is available 2.4 The /health endpoint returns HTTP 200 2.5 The response body is a simple JSON object (e.g. { status: ok }) 2.6 No authentication is required 2.7 No database connection is required 2.8 The endpoint is accessible via http://localhost:<port>/health 2.9 All code uses Python 3.13+ type hints and clear docstrings Success metrics 3.1 curl http://localhost:<port>/health returns HTTP 200 3.2 All pytest tests pass 3.3 Test coverage includes the /health endpoint 3.4 Code follows constitution rules` appears literally below. Do not ask the user to repeat it unless they provided an empty command.

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
   
   d. Run the script `.specify/scripts/bash/create-new-feature.sh --json "Feature: Backend service bootstrap (FastAPI) User journeys 1.1 Start the backend service locally 1.2 Verify the service is running via a health endpoint Acceptance criteria 2.1 The backend is implemented using Python FastAPI 2.2 The service starts successfully using uvicorn 2.3 An HTTP endpoint GET /health is available 2.4 The /health endpoint returns HTTP 200 2.5 The response body is a simple JSON object (e.g. { status: ok }) 2.6 No authentication is required 2.7 No database connection is required 2.8 The endpoint is accessible via http://localhost:<port>/health 2.9 All code uses Python 3.13+ type hints and clear docstrings Success metrics 3.1 curl http://localhost:<port>/health returns HTTP 200 3.2 All pytest tests pass 3.3 Test coverage includes the /health endpoint 3.4 Code follows constitution rules"` with the calculated number and short-name:
      - Pass `--number N+1` and `--short-name "your-short-name"` along with the feature description
      - Bash example: `.specify/scripts/bash/create-new-feature.sh --json "Feature: Backend service bootstrap (FastAPI) User journeys 1.1 Start the backend service locally 1.2 Verify the service is running via a health endpoint Acceptance criteria 2.1 The backend is implemented using Python FastAPI 2.2 The service starts successfully using uvicorn 2.3 An HTTP endpoint GET /health is available 2.4 The /health endpoint returns HTTP 200 2.5 The response body is a simple JSON object (e.g. { status: ok }) 2.6 No authentication is required 2.7 No database connection is required 2.8 The endpoint is accessible via http://localhost:<port>/health 2.9 All code uses Python 3.13+ type hints and clear docstrings Success metrics 3.1 curl http://localhost:<port>/health returns HTTP 200 3.2 All pytest tests pass 3.3 Test coverage includes the /health endpoint 3.4 Code follows constitution rules" --json --number 5 --short-name "user-auth" "Add user authentication"`
      - PowerShell example: `.specify/scripts/bash/create-new-feature.sh --json "Feature: Backend service bootstrap (FastAPI) User journeys 1.1 Start the backend service locally 1.2 Verify the service is running via a health endpoint Acceptance criteria 2.1 The backend is implemented using Python FastAPI 2.2 The service starts successfully using uvicorn 2.3 An HTTP endpoint GET /health is available 2.4 The /health endpoint returns HTTP 200 2.5 The response body is a simple JSON object (e.g. { status: ok }) 2.6 No authentication is required 2.7 No database connection is required 2.8 The endpoint is accessible via http://localhost:<port>/health 2.9 All code uses Python 3.13+ type hints and clear docstrings Success metrics 3.1 curl http://localhost:<port>/health returns HTTP 200 3.2 All pytest tests pass 3.3 Test coverage includes the /health endpoint 3.4 Code follows constitution rules" -Json -Number 5 -ShortName "user-auth" "Add user authentication"`

3. Load `.specify/templates/spec-template.md` to understand required sections.

4. Follow this execution flow:
    ...
```

## Response snapshot

- Created feature branch `002-fastapi-health`, produced spec with user stories (start service, check health), functional requirements, edge cases, measurable outcomes; added checklist marked complete.

## Outcome

- ✅ Impact: Spec ready for planning; checklist completed
- 🧪 Tests: Not run (specification work only)
- 📁 Files: specs/002-fastapi-health/spec.md; specs/002-fastapi-health/checklists/requirements.md
- 🔁 Next prompts: /sp.plan for this feature
- 🧠 Reflection: Simple scope; no clarifications needed; ensure plan aligns with FastAPI/uvicorn requirements.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): None
- Prompt variant (if applicable): n/a
- Next experiment (smallest change to try): n/a
