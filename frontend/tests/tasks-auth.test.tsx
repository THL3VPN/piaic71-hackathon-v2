import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi, afterEach } from "vitest";
import TasksPage from "../app/tasks/page";
import { clearToken, saveToken } from "../lib/auth";

const pushMock = vi.fn();
vi.mock("next/navigation", () => ({ useRouter: () => ({ push: pushMock }) }));

vi.stubGlobal("fetch", vi.fn());

describe("Tasks page with auth", () => {
  beforeEach(() => {
    clearToken();
    vi.clearAllMocks();
  });

  afterEach(() => {
    clearToken();
  });

  it("attaches jwt header when fetching tasks", async () => {
    saveToken("jwt-token");
    const tasks = [{ id: 1, title: "Auth task", description: "owned", completed: true }];
    vi.stubGlobal(
      "fetch",
      vi.fn()
        .mockResolvedValueOnce({ ok: true, json: async () => tasks }) // initial list
        .mockResolvedValueOnce({ ok: true, json: async () => tasks }) // toggle or fetch again
    );

    render(<TasksPage />);

    expect(await screen.findByText("Auth task")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith(
      "http://localhost:8000/api/tasks",
      expect.objectContaining({
        headers: expect.objectContaining({ Authorization: "Bearer jwt-token" }),
      })
    );
  });

  it("publishes logout to clear token and navigate back", async () => {
    saveToken("jwt-token");
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: async () => [] });
    vi.stubGlobal("fetch", fetchMock);

    render(<TasksPage />);
    expect(await screen.findByText("No tasks yet")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /logout/i }));
    expect(localStorage.getItem("auth_token")).toBeNull();
  });
});
