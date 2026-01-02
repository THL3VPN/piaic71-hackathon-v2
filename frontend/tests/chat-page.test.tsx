import { render, screen, fireEvent, act } from "@testing-library/react";
import { describe, expect, it, vi, afterEach, beforeAll } from "vitest";
import ChatPage from "../app/chat/page";

vi.mock("../lib/chat", () => ({
  sendChatMessage: vi.fn(),
  getConversationMessages: vi.fn(),
}));

// [Task]: T005 [From]: specs/017-add-chat-widget/spec.md
const { sendChatMessage, getConversationMessages } = await import("../lib/chat");
const sendChatMessageMock = vi.mocked(sendChatMessage);
const getConversationMessagesMock = vi.mocked(getConversationMessages);

describe("ChatPage", () => {
  beforeAll(() => {
    if (!HTMLElement.prototype.scrollIntoView) {
      HTMLElement.prototype.scrollIntoView = vi.fn();
    }
  });

  afterEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("sends a message and renders the assistant reply", async () => {
    getConversationMessagesMock.mockResolvedValue([]);
    sendChatMessageMock.mockResolvedValue({
      conversation_id: 1,
      response: "Added.",
      tool_calls: [],
    });

    render(<ChatPage />);

    fireEvent.change(screen.getByLabelText(/message/i), {
      target: { value: "Add a task" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(await screen.findByText("Add a task")).toBeInTheDocument();
    expect(await screen.findByText("Added.")).toBeInTheDocument();
  });

  it("shows a loading indicator while waiting for the reply", async () => {
    getConversationMessagesMock.mockResolvedValue([]);
    let resolveReply: (value: unknown) => void;
    const replyPromise = new Promise((resolve) => {
      resolveReply = resolve;
    });

    sendChatMessageMock.mockReturnValue(replyPromise);

    render(<ChatPage />);

    fireEvent.change(screen.getByLabelText(/message/i), {
      target: { value: "List tasks" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(await screen.findByText(/assistant is typing/i)).toBeInTheDocument();

    await act(async () => {
      resolveReply!({ conversation_id: 2, response: "Here you go.", tool_calls: [] });
    });

    expect(await screen.findByText("Here you go.")).toBeInTheDocument();
  });

  it("renders empty state hints before any messages", () => {
    getConversationMessagesMock.mockResolvedValue([]);

    render(<ChatPage />);

    expect(screen.getByText(/try one of these/i)).toBeInTheDocument();
  });

  it("shows an error and allows retry", async () => {
    getConversationMessagesMock.mockResolvedValue([]);
    sendChatMessageMock
      .mockRejectedValueOnce(new Error("Network down"))
      .mockResolvedValueOnce({
        conversation_id: 4,
        response: "Recovered.",
        tool_calls: [],
      });

    render(<ChatPage />);

    fireEvent.change(screen.getByLabelText(/message/i), {
      target: { value: "Retry me" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(await screen.findByRole("alert")).toHaveTextContent(/network down/i);

    fireEvent.click(screen.getByRole("button", { name: /retry/i }));

    expect(await screen.findByText("Recovered.")).toBeInTheDocument();
  });
});
