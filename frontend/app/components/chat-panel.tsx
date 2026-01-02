"use client";

// [Task]: T004, T010, T015, T021, T023 [From]: specs/017-add-chat-widget/spec.md
import React, { useEffect, useMemo, useRef, useState } from "react";
import { getConversationMessages, sendChatMessage } from "../../lib/chat";
import { clearActiveConversationId, setActiveConversationId } from "../../lib/chatStorage";
import { ChatMessage } from "../../lib/types";

type ChatPanelProps = {
  inputRef: React.RefObject<HTMLTextAreaElement>;
  isWidget?: boolean;
  messages: ChatMessage[];
  setMessages: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  conversationId: number | null;
  setConversationId: (id: number | null) => void;
  loadingHistory: boolean;
  setLoadingHistory: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
  onClose?: () => void;
};

const emptyHints = [
  "Add a task to buy groceries",
  "Show my pending tasks",
  "Mark task 3 as complete",
  "Delete the meeting task",
  "Change task 1 to 'Call mom tonight'",
];

function normalizeMessage(message: ChatMessage): ChatMessage {
  return {
    ...message,
    content: message.content ?? "",
  };
}

export default function ChatPanel({
  inputRef,
  isWidget = false,
  messages,
  setMessages,
  conversationId,
  setConversationId,
  loadingHistory,
  setLoadingHistory,
  error,
  setError,
  onClose = () => null,
}: ChatPanelProps) {
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [retryMessage, setRetryMessage] = useState<string | null>(null);
  const [expandedDetails, setExpandedDetails] = useState<Record<number, boolean>>({});
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, sending]);

  const orderedMessages = useMemo(() => messages.map(normalizeMessage), [messages]);

  useEffect(() => {
    async function loadHistory(activeId: number) {
      setLoadingHistory(true);
      setError(null);
      try {
        const history = await getConversationMessages(activeId, 50);
        setMessages(history);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load chat history");
      } finally {
        setLoadingHistory(false);
      }
    }

    if (conversationId != null && orderedMessages.length === 0) {
      void loadHistory(conversationId);
    }
  }, [conversationId, orderedMessages.length, setError, setLoadingHistory, setMessages]);

  async function handleSend(message: string, appendUser: boolean) {
    if (!message.trim()) {
      setError("Message cannot be empty");
      return;
    }

    setError(null);
    setRetryMessage(null);
    const trimmed = message.trim();
    if (appendUser) {
      setMessages((prev) => [...prev, { role: "user", content: trimmed }]);
      setInput("");
    }

    setSending(true);
    try {
      const response = await sendChatMessage(trimmed, conversationId);
      setConversationId(response.conversation_id);
      setActiveConversationId(response.conversation_id);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.response,
          tool_calls: response.tool_calls,
        },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Try again?");
      setRetryMessage(trimmed);
      setInput(trimmed);
    } finally {
      setSending(false);
    }
  }

  const showEmptyState = !loadingHistory && orderedMessages.length === 0;

  return (
    <section className="chat-widget-card">
      <header className="chat-widget-header">
        <div>
          <p className="page-header-subtitle">Assistant</p>
          <h2 className="page-header-title">Todo Assistant</h2>
        </div>
        {isWidget && (
          <div className="chat-widget-actions">
            <button
              type="button"
              className="form-button-secondary"
              onClick={() => {
                clearActiveConversationId();
                setConversationId(null);
                setMessages([]);
              }}
            >
              New chat
            </button>
            <button type="button" className="form-button-secondary" onClick={onClose}>
              Close
            </button>
          </div>
        )}
      </header>

      {error && (
        <div role="alert" aria-live="assertive" className="alert">
          {error}
          {retryMessage && (
            <button
              type="button"
              className="form-button-secondary"
              onClick={() => handleSend(retryMessage, false)}
            >
              Retry
            </button>
          )}
        </div>
      )}

      {loadingHistory && <p className="empty-state">Loading conversation…</p>}

      {showEmptyState && (
        <div className="empty-state">
          <p>Try one of these:</p>
          <ul>
            {emptyHints.map((hint) => (
              <li key={hint}>{hint}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="chat-widget-body">
        <ul className="task-list">
          {orderedMessages.map((message, index) => (
            <li
              key={`${message.role}-${index}`}
              className={`task-card ${message.role === "user" ? "chat-bubble-user" : "chat-bubble-assistant"}`}
            >
              <div className="task-card-header">
                <p className="task-card-title">
                  {message.role === "user" ? "You" : "Assistant"}
                </p>
                {message.created_at && (
                  <span className="task-status task-status-pending">
                    {new Date(message.created_at).toLocaleTimeString()}
                  </span>
                )}
              </div>
              <p className="task-card-description">{message.content}</p>
              {message.tool_calls && message.tool_calls.length > 0 && (
                <div className="card-actions">
                  <button
                    type="button"
                    className="action-button-ghost"
                    onClick={() =>
                      setExpandedDetails((prev) => ({
                        ...prev,
                        [index]: !prev[index],
                      }))
                    }
                  >
                    {expandedDetails[index] ? "Hide details" : "Show details"}
                  </button>
                  {expandedDetails[index] && (
                    <div className="form-error">
                      {message.tool_calls.map((call, callIndex) => (
                        <div key={`${call.name}-${callIndex}`}>
                          <strong>{call.name}</strong>
                          <pre>{JSON.stringify(call.arguments, null, 2)}</pre>
                          <pre>{JSON.stringify(call.result, null, 2)}</pre>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </li>
          ))}
        </ul>
        {sending && <p className="empty-state">Assistant is typing…</p>}
        <div ref={endRef} />
      </div>

      <form
        className="form"
        onSubmit={(event) => {
          event.preventDefault();
          void handleSend(input, true);
        }}
      >
        <label className="form-label" htmlFor="chat-message">
          Message
        </label>
        <textarea
          id="chat-message"
          className="form-input"
          placeholder="Ask the assistant to manage tasks…"
          rows={3}
          value={input}
          onChange={(event) => setInput(event.target.value)}
          ref={inputRef}
        />
        <button type="submit" className="form-button" disabled={sending}>
          {sending ? "Sending…" : "Send"}
        </button>
      </form>
    </section>
  );
}
