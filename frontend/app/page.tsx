"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { fetchBackendHealth } from "../lib/health";
import { login, register, saveToken } from "../lib/auth";
import { HealthStatus } from "../lib/types";

type FormMode = "login" | "register";

export default function Page() {
  const router = useRouter();
  const [status, setStatus] = useState<HealthStatus | null>(null);
  const [healthError, setHealthError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState<FormMode>("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    fetchBackendHealth()
      .then((data) => {
        setStatus(data);
        setHealthError(null);
      })
      .catch((err) => {
        console.error("Health check failed", err);
        setStatus(null);
        setHealthError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (evt: React.FormEvent) => {
    evt.preventDefault();
    setFormError(null);
    try {
      if (mode === "login") {
        const result = await login(username, password);
        saveToken(result.token);
      } else {
        await register(username, password);
        const result = await login(username, password);
        saveToken(result.token);
      }
      router.push("/tasks");
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Authentication failed";
      setFormError(message);
    }
  };

  return (
    <main className="landing-shell">
      <section className="landing-card">
        <div className="landing-hero">
          <p className="landing-kicker">TaskBoard</p>
          <h1 className="landing-title">Welcome</h1>
          <p className="landing-subtitle">Sign in or create an account to manage your tasks.</p>
        </div>

        <div className="landing-health">
          <p className="landing-health-row">
            <span className="landing-dot" />
            Backend: {status ? status.status : healthError ? "unavailable" : "checking..."}
          </p>
          {healthError && (
            <p className="landing-health-alert" role="alert">
              {healthError}
            </p>
          )}
          {loading && !status && !healthError && (
            <p className="landing-health-muted">Checking backend status...</p>
          )}
        </div>

        <div className="landing-modes">
          <button
            className={`landing-pill ${mode === "login" ? "landing-pill-active" : ""}`}
            onClick={() => setMode("login")}
            type="button"
          >
            Sign in
          </button>
          <button
            className={`landing-pill ${mode === "register" ? "landing-pill-active" : ""}`}
            onClick={() => setMode("register")}
            type="button"
          >
            Create account
          </button>
        </div>

        <form className="landing-form" onSubmit={handleSubmit}>
          <label className="landing-label">
            Username
            <input
              aria-label="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="landing-input"
              autoComplete="username"
            />
          </label>
          <label className="landing-label">
            Password
            <input
              aria-label="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="landing-input"
              autoComplete={mode === "login" ? "current-password" : "new-password"}
            />
          </label>

          {formError && (
            <p className="landing-error" role="alert">
              {formError}
            </p>
          )}

          <button type="submit" className="landing-submit">
            {mode === "login" ? "Login" : "Register"}
          </button>
        </form>
      </section>
    </main>
  );
}
