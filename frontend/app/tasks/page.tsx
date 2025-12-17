"use client";

import {
  deleteTask,
  fetchTasks,
  submitTask,
  TaskPayload,
  toggleTaskCompletion,
  updateTask,
  validateTaskPayload,
} from "../../lib/tasks";
import { Task } from "../../lib/types";
import { clearSession, getUsername } from "../../lib/auth";
import React, { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

const tabs = [
  { id: "view", label: "View tasks" },
  { id: "add", label: "Task form" },
];

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const [activeTab, setActiveTab] = useState(tabs[0].id);
  const [username] = useState(() => getUsername());
  const [formData, setFormData] = useState<TaskPayload>({ title: "", description: "" });
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [editingTaskId, setEditingTaskId] = useState<number | null>(null);

  useEffect(() => {
    refresh();
  }, []);

  async function refresh() {
    setLoading(true);
    try {
      const data = await fetchTasks();
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const validationMessage = validateTaskPayload(formData);
    if (validationMessage) {
      setFormError(validationMessage);
      return;
    }
    setFormError(null);
    setSubmitting(true);
    try {
      if (editingTaskId != null) {
        const updated = await updateTask(editingTaskId, formData);
        setTasks((prev) => prev.map((task) => (task.id === updated.id ? updated : task)));
      } else {
        const created = await submitTask(formData);
        setTasks((prev) => [created, ...prev]);
      }
      setFormData({ title: "", description: "" });
      setEditingTaskId(null);
      setActiveTab("view");
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Failed to save task");
    } finally {
      setSubmitting(false);
    }
  }

  const filteredTasks = useMemo(() => tasks, [tasks]);

  return (
    <main className="page-shell">
      <section className="page-card">
        <header className="page-header">
          <div>
            <p className="page-header-subtitle">Task operations</p>
            <h1 className="page-header-title">PIAIC-71</h1>
          </div>
        <div className="page-count-wrapper">
          <span className="page-count">{loading ? "Loading…" : `${tasks.length} tasks`}</span>
          <span className="page-count-secondary">Updated moments ago</span>
        </div>
        <div className="page-actions">
          {username && (
            <span className="form-button-secondary user-name-chip" aria-label={`Signed in as ${username}`}>
              {username}
            </span>
          )}
          <button
            type="button"
            className="form-button-secondary"
            onClick={() => {
              clearSession();
              router.push("/");
            }}
          >
            Logout
          </button>
        </div>
      </header>

        {error && (
          <div role="alert" aria-live="assertive" className="alert">
            Backend unavailable — {error}
          </div>
        )}

        <div className="tab-row">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              className={`tab ${activeTab === tab.id ? "tab-active" : "tab-inactive"}`}
              onClick={() => setActiveTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {activeTab === "view" && (
          <div className="page-grid">
            {!loading && filteredTasks.length === 0 && (
              <p className="empty-state">No tasks yet</p>
            )}
            {filteredTasks.map((task) => (
              <article key={task.id} className="task-card">
                <div className="task-card-header">
                  <p className="task-card-title">{task.title}</p>
                  <span className={`task-status ${task.completed ? "task-status-done" : "task-status-pending"}`}>
                    {task.completed ? "Done" : "Pending"}
                  </span>
                </div>
                {task.description && <p className="task-card-description">{task.description}</p>}
                <div className="card-actions">
                  <button
                    type="button"
                    className="action-button"
                    onClick={() =>
                      toggleTaskCompletion(task.id).then((updated) =>
                        setTasks((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
                      )
                    }
                  >
                    {task.completed ? "Mark Pending" : "Mark Done"}
                  </button>
                  <button
                    type="button"
                    className="action-button-ghost"
                    onClick={() => {
                      setEditingTaskId(task.id);
                      setFormData({ title: task.title, description: task.description ?? "" });
                      setActiveTab("add");
                    }}
                  >
                    Edit
                  </button>
                  <button
                    type="button"
                    className="action-button-danger"
                    onClick={() => deleteTask(task.id).then(() => setTasks((prev) => prev.filter((t) => t.id !== task.id)))}
                  >
                    Delete
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}

        {activeTab === "add" && (
          <form className="form" onSubmit={handleSubmit}>
            <div>
              <label className="form-label" htmlFor="title">
                Title
              </label>
              <input
                id="title"
                value={formData.title}
                onChange={(event) => setFormData((prev) => ({ ...prev, title: event.target.value }))}
                className="form-input"
                placeholder="Describe the task"
              />
            </div>
            <div>
              <label className="form-label" htmlFor="description">
                Description (optional)
              </label>
              <textarea
                id="description"
                value={formData.description}
                onChange={(event) => setFormData((prev) => ({ ...prev, description: event.target.value }))}
                className="form-input"
                placeholder="Add context or acceptance criteria"
                rows={3}
              />
            </div>
            {formError && <p className="form-error">{formError}</p>}
            <button type="submit" disabled={submitting} className="form-button">
              {submitting ? "Saving…" : editingTaskId ? "Update task" : "Add task"}
            </button>
            <button
              type="button"
              className="form-button-secondary"
              onClick={() => {
                setEditingTaskId(null);
                setFormData({ title: "", description: "" });
                setFormError(null);
              }}
            >
              Reset
            </button>
          </form>
        )}
      </section>
    </main>
  );
}
