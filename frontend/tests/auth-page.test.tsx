import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import React from "react";
import Page from "../app/page";

const pushMock = vi.fn();
vi.mock("next/navigation", () => ({ useRouter: () => ({ push: pushMock }) }));

describe("Auth Landing Page", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    localStorage.clear();
  });

  it("shows login/register form and stores token then redirects to tasks", async () => {
    const mockLogin = { token: "jwt-token", token_type: "bearer" };
    const fetchMock = vi
      .fn()
      // health check
      .mockResolvedValueOnce({ ok: true, json: async () => ({ status: "ok" }) })
      // login request
      .mockResolvedValueOnce({ ok: true, json: async () => mockLogin });
    vi.stubGlobal("fetch", fetchMock);

    render(<Page />);

    expect(await screen.findByText(/login/i)).toBeInTheDocument();
    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: "alice" } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: "pw123456" } });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => expect(localStorage.getItem("auth_token")).toBe("jwt-token"));
    // router.push captured through mock
    expect(pushMock).toHaveBeenCalledWith("/tasks");
  });

  it("shows validation error when login fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi
        .fn()
        // health ok
        .mockResolvedValueOnce({ ok: true, json: async () => ({ status: "ok" }) })
        // login fails
        .mockResolvedValueOnce({ ok: false, status: 401, json: async () => ({ detail: "invalid" }) })
    );

    render(<Page />);

    fireEvent.change(screen.getByLabelText(/username/i), { target: { value: "bob" } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: "pw" } });
    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/invalid/i);
  });
});
