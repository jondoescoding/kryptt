"use client";

import { ChatMessageList } from "@/components/ui/chat-message-list";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";
import { useState } from "react";
import { motion } from "framer-motion";

interface Message {
  id: string;
  content: string;
  sender: "user" | "bot";
  timestamp: Date;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage,
      sender: "user",
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, newMessage]);
    setInputMessage("");
  };

  return (
    <div className="flex flex-col h-[calc(100vh-theme(spacing.16))]">
      <div className="flex-1 min-h-0">
        <ChatMessageList className="h-full bg-zinc-900 rounded-lg shadow-lg border border-zinc-800">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              className={`flex ${
                message.sender === "user" ? "justify-end" : "justify-start"
              }`}
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.2 }}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 transition-all duration-200 hover:shadow-lg ${
                  message.sender === "user"
                    ? "bg-yellow-400 text-black hover:bg-yellow-500"
                    : "bg-zinc-800 text-white/70 hover:border-yellow-400/50 hover:bg-zinc-700 border border-transparent"
                }`}
              >
                <p>{message.content}</p>
                <span className={`text-xs ${
                  message.sender === "user" 
                    ? "opacity-70" 
                    : "text-white/50"
                }`}>
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
            </motion.div>
          ))}
        </ChatMessageList>
      </div>
      <div className="flex gap-2 p-4 bg-zinc-900 border-t border-zinc-800 rounded-b-lg">
        <Input
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          placeholder="Type your message..."
          className="flex-1 bg-zinc-800 border-zinc-700 text-white/70 placeholder:text-white/40"
        />
        <Button 
          onClick={handleSendMessage} 
          size="icon"
          className="bg-yellow-400 hover:bg-yellow-500 text-black"
        >
          <Send className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
} 