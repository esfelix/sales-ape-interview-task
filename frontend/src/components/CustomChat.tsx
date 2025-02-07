import { useState, useEffect } from "react";
import { Message } from "@ai-sdk/ui-utils";
import { nanoid } from "nanoid";
import { ChatContainer, ChatForm, ChatMessages } from "@/components/ui/chat";
import { MessageInput } from "@/components/ui/message-input";
import { MessageList } from "@/components/ui/message-list";

export function CustomChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetch("http://localhost:8000/auth/clear-chat", {
          method: "GET",
          credentials: "include",
        });
        if (res.ok) {
          console.log("Chat session refreshed");
        } else {
          console.error("Failed to refresh chat session");
        }
      } catch (error) {
        console.error("Error refreshing chat session:", error);
      }
    })();
  }, []);

  const handleSubmit = (event?: { preventDefault?: () => void }) => {
    event?.preventDefault?.();
    if (!input.trim()) return;

    (async () => {
      setIsLoading(true);
      const userMsg: Message = { id: nanoid(), role: "user", content: input };
      setMessages((prev) => [...prev, userMsg]);
      setInput("");

      try {
        const res = await fetch("http://localhost:8000/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          credentials: "include",
          body: JSON.stringify({ prompt: userMsg.content }),
        });

        const data = await res.json();

        if (data.type === "recommendation") {
          const recommendation = data.recommendation;
          const assistantMsg: Message = {
            id: nanoid(),
            role: "assistant",
            content: `${recommendation.message}\n\n**Track:** ${recommendation.track_name}\n**Artist:** ${recommendation.artists}`,
          };
          setMessages((prev) => [...prev, assistantMsg]);
        } else if (data.type === "play_track") {
          const trackUrl = data.track.external_urls.spotify;
          window.location.href = trackUrl;
        }
      } catch (err) {
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    })().catch(console.error);
  };

  return (
    <div className="flex h-screen w-full items-center justify-center bg-gray-50 p-4">
      <div className="max-w-2xl w-full h-[600px] bg-white rounded shadow p-6 flex flex-col">
        <ChatContainer className="flex-1 flex flex-col">
          {messages.length > 0 && (
            <ChatMessages messages={messages}>
              <MessageList messages={messages} isTyping={isLoading} />
            </ChatMessages>
          )}
          <ChatForm
            className="mt-auto"
            isPending={isLoading}
            handleSubmit={handleSubmit}
          >
            {() => (
              <MessageInput
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Tell us how you're feeling or what you want to listen to..."
                isGenerating={isLoading}
              />
            )}
          </ChatForm>
        </ChatContainer>
      </div>
    </div>
  );
}
