import { render, screen, fireEvent, act } from "@testing-library/react";
import { describe, expect, it, vi, afterEach } from "vitest";
import ChatPage from "../app/chat/page";

vi.mock("../lib/chat", () => ({
  sendChatMessage: vi.fn(),
  getConversationMessages: vi.fn(),
}));

const { sendChatMessage } = await import("../lib/chat");
const sendChatMessageMock = vi.mocked(sendChatMessage);

describe("ChatPage", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("sends a message and renders the assistant reply", async () => {
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

    expect(await screen.findByText(/waiting for response/i)).toBeInTheDocument();

    await act(async () => {
      resolveReply!({ conversation_id: 2, response: "Here you go.", tool_calls: [] });
    });

    expect(await screen.findByText("Here you go.")).toBeInTheDocument();
  });
});
