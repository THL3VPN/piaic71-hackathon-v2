# Data Model: MCP Server Extraction

No new data entities are introduced. MCP tools operate on existing task data.

Existing entities used:

- **Task**: Task records persisted in the database.
- **Conversation/Message**: Chat history used for stateless behavior.
- **Tool Call Record**: Response payload entries describing tool invocation.
