# Quickstart: Task Tools Layer

## Goal

Validate that task tools can be invoked directly with a user identifier and return structured results with correct ownership and validation behavior.

## Suggested Tests

1. **Create a task via tool**
   - Call add_task with a valid user_id and title
   - Assert returned status is "created" and task_id is present

2. **List tasks via tool**
   - Call list_tasks with status = "all"
   - Assert only user-owned tasks are returned

3. **Complete a task via tool**
   - Call complete_task with a user-owned task_id
   - Assert status is "completed" and title matches

4. **Update a task via tool**
   - Call update_task with a title or description
   - Assert status is "updated" and title matches

5. **Delete a task via tool**
   - Call delete_task with a user-owned task_id
   - Assert status is "deleted"

6. **Ownership enforcement**
   - Attempt to complete/delete/update a task owned by another user
   - Expect UnauthorizedAccess

7. **Validation errors**
   - add_task with empty title -> InvalidInput
   - update_task with no fields -> InvalidInput
   - list_tasks with unsupported status -> InvalidInput

## Validation Notes (2025-12-31)

The quickstart scenarios are covered by unit tests in `tests/unit/test_task_tools.py`:
- add_task: test_add_task_creates_task_and_returns_result
- list_tasks: test_list_tasks_defaults_to_all_and_filters_owner, test_list_tasks_supports_status_filters
- complete_task: test_complete_task_marks_task_completed
- update_task: test_update_task_updates_title_and_description
- delete_task: test_delete_task_removes_task
- ownership enforcement: test_cross_user_access_raises_unauthorized
- validation errors: test_add_task_rejects_empty_title, test_update_task_rejects_empty_payload, test_list_tasks_rejects_invalid_status
