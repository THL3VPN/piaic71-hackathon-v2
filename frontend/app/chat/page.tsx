"use client";

// [Task]: T005 [From]: specs/017-add-chat-widget/spec.md
import React from "react";
import ChatPanel from "../components/chat-panel";
import { ChatMessage } from "../../lib/types";

export default function ChatPage() {
  const [messages, setMessages] = React.useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = React.useState<number | null>(null);
  const [loadingHistory, setLoadingHistory] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const inputRef = React.useRef<HTMLTextAreaElement | null>(null);

  return (
    <main className="page-shell">
      <section className="page-card">
        <header className="page-header">
          <div>
            <p className="page-header-subtitle">Chat assistant</p>
            <h1 className="page-header-title">Task Chat</h1>
          </div>
        </header>

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
          onClose={() => null}
        />
      </section>
    </main>
  );
}
