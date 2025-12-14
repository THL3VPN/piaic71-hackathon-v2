"use client";

import { fetchTasks, submitTask, validateTaskPayload } from "../../lib/tasks";
import { Task } from "../../lib/types";
import React, { useEffect, useState } from "react";

const statusClasses = {
  true: "text-emerald-500",
  false: "text-orange-500"
};

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [formData, setFormData] = useState({ title: "", description: "" });
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchTasks()
      .then((data) => setTasks(data))
      .catch((err) => setError(err instanceof Error ? err.message : "Failed to load tasks"))
      .finally(() => setLoading(false));
  }, []);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const validationMessage = validateTaskPayload({
      title: formData.title,
      description: formData.description,
    });

    if (validationMessage) {
      setFormError(validationMessage);
      return;
    }

    setFormError(null);
    setSubmitting(true);

    try {
      const created = await submitTask(
        {
          title: formData.title,
          description: formData.description,
        },
        { retry: true }
      );
      setTasks((previous) => [created, ...previous]);
      setFormData({ title: "", description: "" });
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Failed to create task");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 p-6 text-white">
      <section className="mx-auto max-w-5xl space-y-6 rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl">
        <header className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Tasks</p>
            <h1 className="text-4xl font-semibold">Team backlog</h1>
          </div>
          <span className="text-sm text-slate-300">
            {loading ? "Loading…" : `${tasks.length} task${tasks.length === 1 ? "" : "s"}`}
          </span>
        </header>

        {error && (
          <div
            role="alert"
            aria-live="assertive"
            className="rounded-2xl border border-red-400/60 bg-red-500/10 p-4 text-sm text-red-200"
          >
            Backend unavailable — {error}
          </div>
        )}

        <div className="grid gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
          {tasks.map((task) => (
            <article
              key={task.id}
              className="rounded-2xl border border-white/10 bg-slate-900/60 p-5 backdrop-blur"
            >
              <div className="flex items-center justify-between">
                <p className="text-2xl font-bold tracking-tight">{task.title}</p>
                <span className={statusClasses[task.completed]}>{task.completed ? "Done" : "Pending"}</span>
              </div>
              {task.description && (
                <p className="mt-3 text-sm text-slate-300">{task.description}</p>
              )}
            </article>
          ))}
        </div>

        {!loading && tasks.length === 0 && !error && (
          <p className="rounded-2xl border border-dashed border-slate-600/60 p-4 text-center text-slate-400">
            No tasks yet. Create one to get started.
          </p>
        )}
        <form className="space-y-4 rounded-2xl border border-white/10 bg-slate-950/30 p-6" onSubmit={handleSubmit}>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-200" htmlFor="title">
              Title
            </label>
            <input
              id="title"
              value={formData.title}
              onChange={(event) => setFormData((prev) => ({ ...prev, title: event.target.value }))}
              className="w-full rounded-2xl border border-white/20 bg-slate-900/80 p-3 text-white placeholder:text-slate-500 focus:border-emerald-400 focus:outline-none"
              placeholder="Describe the task"
            />
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-slate-200" htmlFor="description">
              Description (optional)
            </label>
            <textarea
              id="description"
              value={formData.description}
              onChange={(event) => setFormData((prev) => ({ ...prev, description: event.target.value }))}
              className="w-full rounded-2xl border border-white/20 bg-slate-900/80 p-3 text-white placeholder:text-slate-500 focus:border-emerald-400 focus:outline-none"
              placeholder="Add context or acceptance criteria"
              rows={3}
            />
          </div>
          {formError && <p className="text-sm text-red-300">{formError}</p>}
          <button
            type="submit"
            disabled={submitting}
            className="rounded-2xl bg-emerald-500 px-6 py-3 font-semibold text-slate-900 transition hover:bg-emerald-400 disabled:opacity-60"
          >
            {submitting ? "Adding…" : "Add task"}
          </button>
        </form>
      </section>
    </main>
  );
}
