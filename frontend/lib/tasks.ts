import { Task } from "./types";

const BASE_URL = "http://localhost:8000/api/tasks";

export type TaskPayload = { title: string; description?: string };

export function validateTaskPayload(payload: TaskPayload): string | null {
  if (!payload.title.trim()) {
    return "Title is required";
  }
  return null;
}

async function parsedResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

export async function fetchTasks(): Promise<Task[]> {
  const res = await fetch(BASE_URL, {
    headers: { Accept: "application/json" },
    cache: "no-store",
  });

  return parsedResponse(res);
}

export async function submitTask(payload: TaskPayload, options?: { retry?: boolean }): Promise<Task> {
  const attempt = async () => {
    const res = await fetch(BASE_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload),
    });
    return parsedResponse<Task>(res);
  };

  try {
    return await attempt();
  } catch (err) {
    if (options?.retry) {
      return attempt();
    }
    throw err;
  }
}

export async function updateTask(id: number, payload: TaskPayload): Promise<Task> {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
  });
  return parsedResponse<Task>(res);
}

export async function deleteTask(id: number): Promise<void> {
  const res = await fetch(`${BASE_URL}/${id}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    throw new Error(`Failed to delete task: ${res.status} ${res.statusText}`);
  }
}

export async function toggleTaskCompletion(id: number): Promise<Task> {
  const res = await fetch(`${BASE_URL}/${id}/complete`, {
    method: "PATCH",
    headers: { Accept: "application/json" },
  });
  return parsedResponse<Task>(res);
}
