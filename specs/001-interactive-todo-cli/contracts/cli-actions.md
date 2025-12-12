# CLI Interaction Contract: Interactive CLI Todo App

| Action | Inputs | Success Outcome | Error/Validation | Returns to Menu |
|--------|--------|-----------------|------------------|-----------------|
| View tasks | None | Shows table with ID/index, title, completion status; shows empty-state message when none | n/a | Yes |
| Add task | Title (non-empty) | Creates task with unique ID/index, status = incomplete, confirms creation | Empty/whitespace title → friendly validation message; no task created | Yes |
| Update task | ID/index, new title (non-empty) | Updates task title and confirms change | Invalid ID/index → "task not found"; empty/whitespace title → validation message; no change | Yes |
| Delete task | ID/index | Removes task and confirms deletion | Invalid ID/index → "task not found"; no deletion | Yes |
| Mark complete/incomplete | ID/index | Toggles completion status and confirms result | Invalid ID/index → "task not found"; no change | Yes |
| Exit | None | Cleanly terminates loop | n/a | n/a |
