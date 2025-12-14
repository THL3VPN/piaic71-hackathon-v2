import { render, screen, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi, afterEach } from "vitest";
import TasksPage from "../app/tasks/page";

describe("TasksPage", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("tries to fetch tasks and renders a list entry", async () => {
    const sampleTasks = [
      { id: 1, title: "Sample task", description: "Explain it", completed: false },
    ];

    vi.stubGlobal("fetch", vi.fn(() =>
      Promise.resolve({ ok: true, json: async () => sampleTasks })
    ));

    render(<TasksPage />);

    expect(fetch).toHaveBeenCalledWith("http://localhost:8000/api/tasks", expect.any(Object));
    expect(await screen.findByText("Sample task")).toBeInTheDocument();
    expect(screen.getByText("Team backlog")).toBeInTheDocument();
  });

  it("validates and submits the add-task form", async () => {
    const newTask = { id: 5, title: "New task", description: "Fresh", completed: false };

    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: async () => [] })
      .mockResolvedValueOnce({ ok: true, json: async () => newTask })
      .mockResolvedValueOnce({ ok: true, json: async () => [newTask] });

    vi.stubGlobal("fetch", fetchMock);

    render(<TasksPage />);

    await screen.findByText(/No tasks yet/i);

    fireEvent.click(screen.getByRole("button", { name: /Add task/i }));
    expect(await screen.findByText(/title is required/i)).toBeInTheDocument();

    fireEvent.change(screen.getByLabelText(/title/i), { target: { value: "New task" } });
    fireEvent.change(screen.getByLabelText(/description/i), { target: { value: "Fresh" } });
    fireEvent.click(screen.getByRole("button", { name: /Add task/i }));

    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/api/tasks",
      expect.objectContaining({
        method: "POST",
        body: JSON.stringify({ title: "New task", description: "Fresh" }),
      })
    );

    expect(await screen.findByText("New task")).toBeInTheDocument();
  });

  it("shows a backend error message and retains responsive layout when fetching fails", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.reject(new Error("network down"))));

    render(<TasksPage />);

    expect(await screen.findByRole("alert")).toHaveTextContent(/Backend unavailable/i);
    expect(document.querySelector(".page-grid")).toBeInTheDocument();
  });
});
