import { HealthStatus } from "./types";

const explicitBackendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
const FALLBACK_ENDPOINT = "/api/health";
const HEALTH_URL = explicitBackendUrl ? `${explicitBackendUrl}/health` : FALLBACK_ENDPOINT;

export async function fetchBackendHealth(): Promise<HealthStatus> {
  const response = await fetch(HEALTH_URL, {
    cache: "no-store",
    headers: {
      "Accept": "application/json"
    }
  });

  if (!response.ok) {
    throw new Error(`Health request failed: ${response.status} ${response.statusText}`);
  }

  return response.json();
}
