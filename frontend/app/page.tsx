 "use client";
import React, { useEffect, useState } from "react";
import { fetchBackendHealth } from "../lib/health";
import { HealthStatus } from "../lib/types";

export default function Page() {
  const [status, setStatus] = useState<HealthStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBackendHealth()
      .then((data) => {
        setStatus(data);
        setError(null);
      })
      .catch((err) => {
        console.error("Health check failed", err);
        setStatus(null);
        setError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center p-6">
      <section className="space-y-4 border border-white/20 rounded-2xl p-8 bg-white/5 shadow-2xl">
        <h1 className="text-3xl font-semibold tracking-tight">Backend Health</h1>
        {status && (
          <p className="text-lg">
            Backend: <strong>{status.status}</strong>
          </p>
        )}
        {error && (
          <p className="text-red-400">
            Backend: unavailable
            <span className="block text-sm text-red-200">{error}</span>
          </p>
        )}
        {loading && !status && !error && (
          <p className="text-sm text-slate-300">Checking backend status...</p>
        )}
      </section>
    </main>
  );
}
