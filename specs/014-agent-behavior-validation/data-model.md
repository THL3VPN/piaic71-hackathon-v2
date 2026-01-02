# Data Model: Agent Behavior Validation

No new data entities are introduced in this step.

Existing entities used for validation:

- **Conversation**: Stores chat sessions per user.
- **Message**: Stores user and assistant messages used for stateless history.
- **Task**: Stores user tasks mutated by tool calls.
- **Tool Call**: Response payload entries reflecting tool name, inputs, and outputs.
