"use client";

// [Task]: T001, T009, T014, T022 [From]: specs/017-add-chat-widget/spec.md
// [Task]: T003, T016 [From]: specs/018-chat-widget-polish/spec.md
import React, { useEffect, useRef, useState } from "react";
import ChatPanel from "./chat-panel";
import { getActiveConversationId } from "../../lib/chatStorage";
import { ChatMessage } from "../../lib/types";
import { getLauncherIcon, getLauncherLabel } from "../../lib/chatWidget";

type ChatWidgetProps = {
  isAuthenticated: boolean;
};

export default function ChatWidget({ isAuthenticated }: ChatWidgetProps) {
  const [open, setOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);

  useEffect(() => {
    if (!isAuthenticated) {
      setOpen(false);
      setMessages([]);
      setConversationId(null);
      setError(null);
      return;
    }
    const stored = getActiveConversationId();
    if (stored && conversationId == null) {
      setConversationId(stored);
    }
  }, [isAuthenticated, conversationId]);

  useEffect(() => {
    if (open && inputRef.current) {
      inputRef.current.focus();
    }
  }, [open]);

  useEffect(() => {
    function handleKey(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setOpen(false);
      }
    }
    if (open) {
      window.addEventListener("keydown", handleKey);
      return () => window.removeEventListener("keydown", handleKey);
    }
    return undefined;
  }, [open]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="chat-widget-shell fixed right-6 bottom-6 z-[60] flex flex-col items-end gap-3">
      {open && (
        <div
          className="chat-widget-panel w-[min(420px,calc(100vw-2rem))] h-[min(70vh,620px)] min-w-0 overflow-hidden text-sm"
          role="dialog"
          aria-label="Todo Assistant chat"
        >
          <ChatPanel
            inputRef={inputRef}
            messages={messages}
            setMessages={setMessages}
            conversationId={conversationId}
            setConversationId={setConversationId}
            loadingHistory={loadingHistory}
            setLoadingHistory={setLoadingHistory}
            error={error}
            setError={setError}
            onClose={() => setOpen(false)}
            isWidget
          />
        </div>
      )}
      <button
        type="button"
        className="chat-widget-launcher"
        aria-label={getLauncherLabel(open)}
        onClick={() => setOpen((prev) => !prev)}
      >
        {getLauncherIcon(open)}
      </button>
    </div>
  );
}
