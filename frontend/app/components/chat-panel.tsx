"use client";

// [Task]: T004, T010, T015, T021, T023 [From]: specs/017-add-chat-widget/spec.md
// [Task]: T004, T005, T008, T009, T011, T012, T013, T015, T017 [From]: specs/018-chat-widget-polish/spec.md
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

function formatMessageContent(content: string): string {
  const trimmed = content.trim();
  if (!trimmed) {
    return content;
  }

  const withNumberedBreaks = trimmed.replace(/\s+(?=\d+\.\s)/g, "\n");
  const withBoldBreaks = withNumberedBreaks.replace(/\s+(?=\*\*[^*]+\*\*\s*-)/g, "\n");
  return withBoldBreaks.replace(/\*\*/g, "");
}

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

  function handleComposerKeyDown(event: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      void handleSend(input, true);
    }
  }

  const showEmptyState = !loadingHistory && orderedMessages.length === 0;

  return (
    <section className="chat-widget-card flex h-full min-w-0 flex-col overflow-hidden">
      <header className="chat-widget-header flex flex-wrap items-center justify-between gap-3">
        <div className="min-w-0">
          <p className="text-[0.6rem] font-semibold uppercase tracking-[0.3em] text-slate-400">
            Assistant
          </p>
          <h2 className="text-base font-semibold leading-tight text-slate-100">
            Todo Assistant
          </h2>
        </div>
        {isWidget && (
          <div className="chat-widget-actions flex items-center gap-2">
            <button
              type="button"
              className="h-8 rounded-full border border-slate-600 px-3 text-[0.6rem] font-semibold uppercase tracking-[0.2em] text-slate-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400"
              onClick={() => {
                clearActiveConversationId();
                setConversationId(null);
                setMessages([]);
              }}
            >
              New chat
            </button>
            <button
              type="button"
              className="h-8 rounded-full border border-slate-600 px-3 text-[0.6rem] font-semibold uppercase tracking-[0.2em] text-slate-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-sky-400"
              onClick={onClose}
            >
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
              className="form-button-secondary focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-amber-400"
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

      <div className="chat-widget-body flex-1 min-w-0 overflow-x-hidden overflow-y-auto pr-2">
        <ul className="flex flex-col gap-3">
          {orderedMessages.map((message, index) => {
            const displayContent =
              message.role === "assistant" ? formatMessageContent(message.content) : message.content;
            return (
              <li
                key={`${message.role}-${index}`}
                className={`rounded-2xl border border-slate-700/60 bg-slate-900/80 px-4 py-3 text-slate-200 shadow-[0_12px_30px_rgba(2,6,23,0.45)] max-w-[85%] break-words ${
                  message.role === "user"
                    ? "ml-auto text-left chat-bubble-user"
                    : "mr-auto text-left chat-bubble-assistant"
                }`}
              >
              <div className="flex items-center justify-between gap-2">
                <p
                  className="text-[0.65rem] font-semibold uppercase tracking-[0.25em] text-slate-300"
                  data-testid="message-role"
                >
                  {message.role === "user" ? "You" : "Assistant"}
                </p>
                {message.created_at && (
                  <span className="task-status task-status-pending">
                    {new Date(message.created_at).toLocaleTimeString()}
                  </span>
                )}
              </div>
              <p className="mt-2 whitespace-pre-line break-words text-sm leading-relaxed text-slate-200">
                {displayContent}
              </p>
              {message.tool_calls && message.tool_calls.length > 0 && (
                <div className="card-actions">
                  <button
                    type="button"
                    className="action-button-ghost focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-400"
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
                    <div className="mt-2 rounded-lg bg-slate-950/60 p-2 text-xs text-slate-200 max-w-full break-words">
                      {message.tool_calls.map((call, callIndex) => (
                        <div key={`${call.name}-${callIndex}`}>
                          <strong>{call.name}</strong>
                          <pre className="whitespace-pre-wrap break-words">
                            {JSON.stringify(call.arguments, null, 2)}
                          </pre>
                          <pre className="whitespace-pre-wrap break-words">
                            {JSON.stringify(call.result, null, 2)}
                          </pre>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
              </li>
            );
          })}
        </ul>
        {sending && <p className="empty-state">Assistant is typing…</p>}
        <div ref={endRef} />
      </div>

      <form
        data-testid="chat-composer"
        className="mt-3 flex items-center gap-3 rounded-2xl border border-slate-800 bg-slate-900/90 p-3"
        onSubmit={(event) => {
          event.preventDefault();
          void handleSend(input, true);
        }}
      >
        <label className="form-label sr-only" htmlFor="chat-message">
          Message
        </label>
        <textarea
          id="chat-message"
          className="flex-1 resize-none rounded-xl border border-slate-700 bg-slate-950/60 px-3 py-2 text-sm text-slate-100 placeholder:text-slate-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-300"
          placeholder="Ask the assistant to manage tasks…"
          rows={1}
          value={input}
          onChange={(event) => setInput(event.target.value)}
          onKeyDown={handleComposerKeyDown}
          ref={inputRef}
        />
        <button
          type="submit"
          className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-400 text-slate-900 shadow-[0_10px_25px_rgba(16,185,129,0.35)] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-emerald-300"
          disabled={sending}
          aria-label="Send"
        >
          <span className="sr-only">{sending ? "Sending" : "Send"}</span>
          <span aria-hidden="true">➤</span>
        </button>
      </form>
    </section>
  );
}
