export type HealthStatus = {
  status: string;
  message?: string;
  timestamp?: string;
};

export type Task = {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
};

export type ToolCall = {
  name: string;
  arguments: Record<string, unknown>;
  result: Record<string, unknown>;
};

export type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  created_at?: string;
  tool_calls?: ToolCall[];
};

export type ChatResponse = {
  conversation_id: number;
  response: string;
  tool_calls: ToolCall[];
};
