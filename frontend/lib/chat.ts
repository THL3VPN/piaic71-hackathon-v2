import { fetchWithAuth } from "./auth";
import { ChatMessage, ChatResponse } from "./types";

const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const CHAT_URL = `${backendUrl.replace(/\/$/, "")}/api/chat`;

function buildHistoryUrl(conversationId: number, limit: number): string {
  const base = `${backendUrl.replace(/\/$/, "")}/api/conversations/${conversationId}/messages`;
  const params = new URLSearchParams();
  params.set("limit", String(limit));
  return `${base}?${params.toString()}`;
}

async function parseResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    const detail = (await res.json().catch(() => ({}))).detail || res.statusText;
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return res.json();
}

export async function sendChatMessage(
  message: string,
  conversationId?: number | null,
): Promise<ChatResponse> {
  const payload: Record<string, unknown> = { message };
  if (conversationId) {
    payload.conversation_id = conversationId;
  }
  const res = await fetchWithAuth(CHAT_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse<ChatResponse>(res);
}

export async function getConversationMessages(
  conversationId: number,
  limit = 50,
): Promise<ChatMessage[]> {
  const res = await fetchWithAuth(buildHistoryUrl(conversationId, limit), {
    headers: { Accept: "application/json" },
    cache: "no-store",
  });
  return parseResponse<ChatMessage[]>(res);
}
