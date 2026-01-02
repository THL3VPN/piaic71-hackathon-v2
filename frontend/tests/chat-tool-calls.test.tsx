import { render, screen, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi, afterEach, beforeAll } from "vitest";
import ChatWidget from "../app/components/chat-widget";

vi.mock("../lib/chat", () => ({
  sendChatMessage: vi.fn(),
  getConversationMessages: vi.fn(),
}));

// [Task]: T020 [From]: specs/017-add-chat-widget/spec.md
const { sendChatMessage, getConversationMessages } = await import("../lib/chat");
const sendChatMessageMock = vi.mocked(sendChatMessage);
const getConversationMessagesMock = vi.mocked(getConversationMessages);

describe("Chat tool call details", () => {
  beforeAll(() => {
    if (!HTMLElement.prototype.scrollIntoView) {
      HTMLElement.prototype.scrollIntoView = vi.fn();
    }
  });

  afterEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("toggles tool call details", async () => {
    getConversationMessagesMock.mockResolvedValue([]);
    sendChatMessageMock.mockResolvedValue({
      conversation_id: 3,
      response: "Done.",
      tool_calls: [
        {
          name: "add_task",
          arguments: { title: "buy milk" },
          result: { task_id: 1, status: "created", title: "buy milk" },
        },
      ],
    });

    render(<ChatWidget isAuthenticated />);

    fireEvent.click(screen.getByRole("button", { name: /open chat/i }));

    fireEvent.change(screen.getByLabelText(/message/i), {
      target: { value: "Add buy milk" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    const toggle = await screen.findByRole("button", { name: /show details/i });
    fireEvent.click(toggle);

    expect(await screen.findByText("add_task")).toBeInTheDocument();
    const mentions = await screen.findAllByText(/buy milk/i);
    expect(mentions.length).toBeGreaterThanOrEqual(2);
  });
});
