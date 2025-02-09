"use client";

import { ChatMessageList } from "@/components/ui/chat-message-list";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";
import { motion } from "framer-motion";
import { useChat } from 'ai/react';

export default function ChatPage() {
  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: '/api/chat',
  });

  return (
    <div className="flex flex-col h-[calc(100vh-theme(spacing.16))]">
      <div className="flex-1 min-h-0">
        <ChatMessageList className="h-full bg-zinc-900 rounded-lg shadow-lg border border-zinc-800">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
              whileHover={{ scale: 1.02 }}
              transition={{ duration: 0.2 }}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 transition-all duration-200 hover:shadow-lg ${
                  message.role === "user"
                    ? "bg-yellow-400 text-black hover:bg-yellow-500"
                    : "bg-zinc-800 text-white/70 hover:border-yellow-400/50 hover:bg-zinc-700 border border-transparent"
                }`}
              >
                <p>{message.content}</p>
                <span className={`text-xs ${
                  message.role === "user" 
                    ? "opacity-70" 
                    : "text-white/50"
                }`}>
                  {new Date().toLocaleTimeString()}
                </span>
              </div>
            </motion.div>
          ))}
        </ChatMessageList>
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2 p-4 bg-zinc-900 border-t border-zinc-800 rounded-b-lg">
        <Input
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
          className="flex-1 bg-zinc-800 border-zinc-700 text-white/70 placeholder:text-white/40"
        />
        <Button 
          type="submit"
          size="icon"
          className="bg-yellow-400 hover:bg-yellow-500 text-black"
        >
          <Send className="h-4 w-4" />
        </Button>
      </form>
    </div>
  );
} 