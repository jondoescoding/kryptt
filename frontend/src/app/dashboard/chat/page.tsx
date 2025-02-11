"use client";

import { ChatInput, ChatInputTextArea, ChatInputSubmit } from "@/components/ui/chat-input";
import { Button } from "@/components/ui/button";
import { LoadingDots } from "@/components/ui/loading-dots";
import { useState } from "react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { motion } from "framer-motion";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Loader2 } from "lucide-react";

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
};

type Agent = {
  id: string;
  name: string;
  endpoint: string;
};

const agents: Agent[] = [
  {
    id: 'position',
    name: 'Position Agent',
    endpoint: '/api/v1/agent/chat'
  }
];

export default function ChatPage() {
  const [isTyping, setIsTyping] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [selectedAgent, setSelectedAgent] = useState<Agent>(agents[0]);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async () => {
    if (!input.trim()) return;

    setIsTyping(true);

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input
    };
    setMessages(prev => [...prev, userMessage]);
    setInput('');

    try {
      const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}${selectedAgent.endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input
        })
      });

      if (!response.ok) throw new Error('Failed to send message');

      const reader = response.body?.getReader();
      if (!reader) throw new Error('No reader available');

      let content = '';
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.trim() === '') continue;
          try {
            const parsed = JSON.parse(line);
            if (parsed.role === 'assistant') {
              content = parsed.content;
              setMessages(prev => {
                const lastMessage = prev[prev.length - 1];
                if (lastMessage?.role === 'assistant') {
                  return [...prev.slice(0, -1), { ...lastMessage, content }];
                }
                return [...prev, { id: Date.now().toString(), role: 'assistant', content }];
              });
            }
          } catch (e) {
            console.error('Failed to parse chunk:', e);
          }
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages(prev => [...prev, {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, something went wrong. Please try again.'
      }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-theme(spacing.16))]">
      <div className="flex-1 min-h-0 overflow-y-auto px-4 py-4">
        <div className="max-w-3xl mx-auto space-y-4">
          {messages.map((message) => (
            <motion.div
              key={message.id}
              className={`flex ${
                message.role === "user" ? "justify-end" : "justify-start"
              }`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 transition-all duration-200 hover:shadow-lg ${
                  message.role === "user"
                    ? "bg-yellow-400 hover:bg-yellow-500"
                    : "bg-zinc-800 text-white/70 hover:border-yellow-400/50 hover:bg-zinc-700 border border-transparent"
                }`}
              >
                <div
                  className={`prose prose-invert max-w-none ${
                    message.role === "user" ? "text-black" : ""
                  } prose-table:border-zinc-700 prose-td:border-zinc-700 prose-th:border-zinc-700 prose-td:p-2 prose-th:p-2 prose-tr:border-zinc-700 prose-thead:border-zinc-700`}
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>
                </div>
                <span
                  className={`text-xs ${
                    message.role === "user" ? "opacity-70" : "text-white/50"
                  }`}
                >
                  {new Date().toLocaleTimeString()}
                </span>
              </div>
            </motion.div>
          ))}
          {isTyping && !messages[messages.length - 1]?.content && (
            <motion.div
              className="flex justify-start"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="max-w-[80%] rounded-lg px-4 py-2 bg-zinc-800 text-white/70 border border-transparent">
                <LoadingDots />
              </div>
            </motion.div>
          )}
        </div>
      </div>
      <div className="border-t border-zinc-800 bg-zinc-900 p-4">
        <div className="max-w-3xl mx-auto">
          <ChatInput value={input} onChange={handleInputChange} onSubmit={handleSubmit}>
            <div className="flex items-center gap-2 w-full">
              <Select
                value={selectedAgent.id}
                onValueChange={(value) => {
                  const agent = agents.find(a => a.id === value);
                  if (agent) setSelectedAgent(agent);
                }}
              >
                <SelectTrigger className="w-[180px] bg-zinc-800 border-zinc-700">
                  <SelectValue placeholder="Select agent" />
                </SelectTrigger>
                <SelectContent>
                  {agents.map((agent) => (
                    <SelectItem key={agent.id} value={agent.id}>
                      {agent.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <ChatInputTextArea
                placeholder="Type your message..."
                className="flex-1 bg-zinc-800 border-zinc-700 text-white/70 placeholder:text-white/40"
                disabled={isTyping}
              />
              <ChatInputSubmit disabled={isTyping}>
                {isTyping ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : null}
              </ChatInputSubmit>
            </div>
          </ChatInput>
        </div>
      </div>
    </div>
  );
} 