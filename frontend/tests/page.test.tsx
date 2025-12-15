import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, it, vi } from "vitest";
import React from "react";
import Page from "../app/page";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
}));

describe("Page", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("displays backend status after the health check succeeds", async () => {
    const mockResponse = {
      ok: true,
      json: vi.fn().mockResolvedValue({ status: "ok" })
    } satisfies Response;

    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(mockResponse));

    render(<Page />);

    await waitFor(() => expect(screen.getByText(/Backend:/i)).toBeInTheDocument());
    expect(screen.getByText(/Backend:/i)).toHaveTextContent("Backend: ok");
  });

  it("shows an error message when the health check fails", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network failure")));

    render(<Page />);

    await waitFor(() => expect(screen.getByText(/Backend: unavailable/i)).toBeInTheDocument());
    expect(screen.getByText(/network failure/i)).toBeInTheDocument();
  });
});
