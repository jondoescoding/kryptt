"use client";

import { ChatMessageList } from "@/components/ui/chat-message-list";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send, BarChart, Loader2 } from "lucide-react";
import { motion } from "framer-motion";
import { useChat } from 'ai/react';
import { LoadingDots } from "@/components/ui/loading-dots";
import { useState } from "react";
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import dynamic from 'next/dynamic';

const Chart = dynamic(() => import('@/components/ui/chart'), { ssr: false });

export default function ChatPage() {
  const [isTyping, setIsTyping] = useState(false);
  const [showChart, setShowChart] = useState(false);
  const [chartData, setChartData] = useState<any>(null);
  
  const { messages, input, handleInputChange, handleSubmit: originalHandleSubmit } = useChat({
    api: '/api/chat',
    onFinish: () => setIsTyping(false),
  });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    setIsTyping(true);
    setShowChart(false);
    await originalHandleSubmit(e);
  };

  const handleViewChart = async () => {
    try {
      const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/v1/positions/crypto-positions`, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        cache: 'no-store'
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Position fetch failed:', {
          status: response.status,
          statusText: response.statusText,
          error: errorText
        });
        throw new Error('Failed to fetch positions');
      }
      
      const data = await response.json();
      const positions = Array.isArray(data) ? data : [];
      
      if (positions.length === 0) {
        console.warn('No positions data available');
        return;
      }
      
      const chartData = {
        labels: positions.map((p: any) => p.symbol),
        datasets: [
          {
            label: 'Market Value ($)',
            data: positions.map((p: any) => parseFloat(p.market_value) || 0),
            backgroundColor: '#EAB308',
          },
          {
            label: 'Unrealized P/L ($)',
            data: positions.map((p: any) => parseFloat(p.unrealized_pl) || 0),
            backgroundColor: '#22C55E',
          }
        ]
      };
      
      setChartData(chartData);
      setShowChart(true);
    } catch (error) {
      console.error('Failed to load chart data:', error);
      setShowChart(false);
    }
  };

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
                className={`prose prose-invert max-w-none ${message.role === "user" ? "text-black" : ""} 
                prose-table:border-zinc-700 
                prose-td:border-zinc-700 
                prose-th:border-zinc-700 
                prose-td:p-2 
                prose-th:p-2
                prose-tr:border-zinc-700
                prose-thead:border-zinc-700`}>
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>
                  {message.role === "assistant" && message.content.includes("View As Chart") && (
                    <Button
                      onClick={handleViewChart}
                      className="mt-2 bg-yellow-400 hover:bg-yellow-500 text-black"
                    >
                      <BarChart className="h-4 w-4 mr-2" />
                      View As Chart
                    </Button>
                  )}
                </div>
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
          {showChart && chartData && (
            <motion.div
              className="w-full p-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <div className="bg-zinc-800 p-4 rounded-lg">
                <Chart data={chartData} />
              </div>
            </motion.div>
          )}
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
        </ChatMessageList>
      </div>
      <div className="h-8" />
      <form onSubmit={handleSubmit} className="flex gap-2 p-4 bg-zinc-900 border-t border-zinc-800 rounded-b-lg">
        <Input
          value={input}
          onChange={handleInputChange}
          placeholder="Type your message..."
          className="flex-1 bg-zinc-800 border-zinc-700 text-white/70 placeholder:text-white/40"
          disabled={isTyping}
        />
        <Button 
          type="submit"
          size="icon"
          className="bg-yellow-400 hover:bg-yellow-500 text-black transition-all duration-200"
          disabled={isTyping}
        >
          {isTyping ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Send className="h-4 w-4" />
          )}
        </Button>
      </form>
    </div>
  );
} 