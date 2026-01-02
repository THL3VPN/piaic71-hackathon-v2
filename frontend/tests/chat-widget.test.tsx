import { render, screen, fireEvent, act } from "@testing-library/react";
import { describe, expect, it, vi, afterEach, beforeAll } from "vitest";
import ChatWidget from "../app/components/chat-widget";

vi.mock("../lib/chat", () => ({
  sendChatMessage: vi.fn(),
  getConversationMessages: vi.fn(),
}));

// [Task]: T007, T008, T017, T018, T019 [From]: specs/017-add-chat-widget/spec.md
const { sendChatMessage, getConversationMessages } = await import("../lib/chat");
const sendChatMessageMock = vi.mocked(sendChatMessage);
const getConversationMessagesMock = vi.mocked(getConversationMessages);

describe("ChatWidget", () => {
  beforeAll(() => {
    if (!HTMLElement.prototype.scrollIntoView) {
      HTMLElement.prototype.scrollIntoView = vi.fn();
    }
  });

  afterEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("opens and closes the widget panel", async () => {
    getConversationMessagesMock.mockResolvedValue([]);

    render(<ChatWidget isAuthenticated />);

    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));
    expect(await screen.findByRole("dialog")).toBeInTheDocument();

    fireEvent.click(screen.getByRole("button", { name: /^close$/i }));
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });

  it("sends a message and shows loading indicator", async () => {
    getConversationMessagesMock.mockResolvedValue([]);
    let resolveReply: (value: unknown) => void;
    const replyPromise = new Promise((resolve) => {
      resolveReply = resolve;
    });
    sendChatMessageMock.mockReturnValue(replyPromise);

    render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));
    fireEvent.change(await screen.findByLabelText(/message/i), {
      target: { value: "Add a task" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(await screen.findByText(/assistant is typing/i)).toBeInTheDocument();

    await act(async () => {
      resolveReply!({ conversation_id: 1, response: "Added.", tool_calls: [] });
    });

    expect(await screen.findByText("Added.")).toBeInTheDocument();
  });

  it("shows empty state prompts when no messages exist", async () => {
    getConversationMessagesMock.mockResolvedValue([]);

    render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));

    expect(await screen.findByText(/try one of these/i)).toBeInTheDocument();
  });

  it("shows error state and allows retry", async () => {
    getConversationMessagesMock.mockResolvedValue([]);
    sendChatMessageMock
      .mockRejectedValueOnce(new Error("Network down"))
      .mockResolvedValueOnce({
        conversation_id: 2,
        response: "Recovered.",
        tool_calls: [],
      });

    render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));
    fireEvent.change(await screen.findByLabelText(/message/i), {
      target: { value: "Retry me" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/network down/i);

    fireEvent.click(screen.getByRole("button", { name: /retry/i }));

    expect(await screen.findByText("Recovered.")).toBeInTheDocument();
  });

  it("focuses input on open and closes on escape", async () => {
    getConversationMessagesMock.mockResolvedValue([]);

    render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));
    const input = await screen.findByLabelText(/message/i);
    expect(document.activeElement).toBe(input);

    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
  });
});
