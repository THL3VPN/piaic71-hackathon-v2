const API_BASE = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export type AuthResponse = { token: string; token_type?: string };

export function saveToken(token: string): void {
  localStorage.setItem("auth_token", token);
}

export function saveUsername(username: string): void {
  localStorage.setItem("auth_username", username);
}

export function getToken(): string | null {
  return typeof window === "undefined" ? null : localStorage.getItem("auth_token");
}

export function getUsername(): string | null {
  return typeof window === "undefined" ? null : localStorage.getItem("auth_username");
}

export function clearToken(): void {
  localStorage.removeItem("auth_token");
}

export function clearSession(): void {
  clearToken();
  localStorage.removeItem("auth_username");
}

export async function fetchWithAuth(input: string | URL, init: RequestInit = {}): Promise<Response> {
  const headers = new Headers(init.headers || {});
  const token = getToken();
  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  return fetch(input, { ...init, headers });
}

async function sendAuth(path: string, body: { username: string; password: string }): Promise<AuthResponse> {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = (await res.json().catch(() => ({}))).detail || res.statusText;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return res.json();
}

export function login(username: string, password: string): Promise<AuthResponse> {
  return sendAuth("/api/login", { username, password });
}

export function register(username: string, password: string): Promise<AuthResponse> {
  return sendAuth("/api/register", { username, password });
}

export function authHeaders(): Record<string, string> {
  const token = getToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}
