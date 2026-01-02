import { render, screen, fireEvent } from "@testing-library/react";
import { describe, expect, it, vi, afterEach, beforeAll } from "vitest";
import ChatPage from "../app/chat/page";

vi.mock("../lib/chat", () => ({
  sendChatMessage: vi.fn(),
  getConversationMessages: vi.fn(),
}));

// [Task]: T012, T013 [From]: specs/016-chat-ui-integration/spec.md
const { sendChatMessage, getConversationMessages } = await import("../lib/chat");
const sendChatMessageMock = vi.mocked(sendChatMessage);
const getConversationMessagesMock = vi.mocked(getConversationMessages);

describe("ChatPage history", () => {
  beforeAll(() => {
    if (!HTMLElement.prototype.scrollIntoView) {
      HTMLElement.prototype.scrollIntoView = vi.fn();
    }
  });

  afterEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it("loads history when a stored conversation id exists", async () => {
    localStorage.setItem("active_conversation_id", "5");
    getConversationMessagesMock.mockResolvedValue([
      { role: "user", content: "Previous task" },
      { role: "assistant", content: "Noted." },
    ]);

    render(<ChatPage />);

    expect(await screen.findByText("Previous task")).toBeInTheDocument();
    expect(await screen.findByText("Noted.")).toBeInTheDocument();
    expect(getConversationMessagesMock).toHaveBeenCalledWith(5, 50);
  });

  it("persists conversation_id after sending a message", async () => {
    getConversationMessagesMock.mockResolvedValue([]);
    sendChatMessageMock.mockResolvedValue({
      conversation_id: 2,
      response: "Saved.",
      tool_calls: [],
    });

    render(<ChatPage />);

    fireEvent.change(screen.getByLabelText(/message/i), {
      target: { value: "Add item" },
    });
    fireEvent.click(screen.getByRole("button", { name: /send/i }));

    expect(await screen.findByText("Saved.")).toBeInTheDocument();
    expect(localStorage.getItem("active_conversation_id")).toBe("2");
  });
});
