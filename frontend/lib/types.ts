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
