import { render, screen, fireEvent, act } from "@testing-library/react";
import { describe, expect, it, vi, afterEach, beforeAll } from "vitest";
import ChatWidget from "../app/components/chat-widget";

vi.mock("../lib/chat", () => ({
  sendChatMessage: vi.fn(),
  getConversationMessages: vi.fn(),
}));

// [Task]: T007, T008, T017, T018, T019 [From]: specs/017-add-chat-widget/spec.md
// [Task]: T006, T010, T014 [From]: specs/018-chat-widget-polish/spec.md
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

  it("renders aligned bubbles and prevents horizontal overflow", async () => {
    getConversationMessagesMock.mockResolvedValue([
      { role: "user", content: "Hello" },
      { role: "assistant", content: "Hi there" },
    ]);
    localStorage.setItem("active_conversation_id", "1");

    const { container } = render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));

    const body = container.querySelector(".chat-widget-body");
    expect(body).toBeTruthy();
    expect(body).toHaveClass("overflow-x-hidden");

    const userBubble = (await screen.findByText("Hello")).closest("li");
    const assistantBubble = (await screen.findByText("Hi there")).closest("li");

    expect(userBubble).toHaveClass("chat-bubble-user");
    expect(assistantBubble).toHaveClass("chat-bubble-assistant");
  });

  it("keeps the composer visible and uses a circular send button", async () => {
    getConversationMessagesMock.mockResolvedValue([]);

    render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));

    const input = await screen.findByLabelText(/message/i);
    const form = screen.getByTestId("chat-composer");
    expect(form).toHaveClass("mt-3");

    const sendButton = screen.getByRole("button", { name: /send/i });
    expect(sendButton).toHaveClass("rounded-full");
  });

  it("renders compact message labels for concise replies", async () => {
    getConversationMessagesMock.mockResolvedValue([
      { role: "assistant", content: "Added." },
    ]);
    localStorage.setItem("active_conversation_id", "2");

    const { container } = render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));

    await screen.findByText("Added.");

    const labels = container.querySelectorAll(".task-card-title");
    expect(labels.length).toBeGreaterThan(0);
    labels.forEach((label) => {
      expect(label).toHaveClass("text-xs");
    });
  });
});
