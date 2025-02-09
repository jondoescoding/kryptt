import { streamText } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';

// Initialize OpenRouter with error handling
const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY || '',
});

export const runtime = 'edge';
export const maxDuration = 30; // Allow streaming responses up to 30 seconds

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();

    // Define the model ID for Gemini
    const MODEL_ID = 'google/gemini-2.0-flash-thinking-exp:free';

    const result = await streamText({
      model: openrouter(MODEL_ID),
      messages: [
        {
          role: "system",
          content: `You are a helpful crypto trading assistant with access to real-time crypto asset data through API endpoints. 
          You can:
          1. Fetch current crypto asset information
          2. Provide trading insights and analysis
          3. Explain crypto concepts
          4. Access real-time market data through the Alpaca API
          
          Always provide clear, concise responses and indicate when you're using external data.`
        },
        ...messages
      ],
      onError: ({ error }) => {
        console.error('Streaming Error:', error);
      }
    });

    // Return a streaming response
    return result.toDataStreamResponse({
      getErrorMessage: (error) => {
        if (error instanceof Error) return error.message;
        if (typeof error === 'string') return error;
        return 'An unexpected error occurred';
      }
    });
  } catch (error: any) {
    console.error('Chat API Error:', error);
    return new Response(
      JSON.stringify({
        error: 'Failed to generate response',
        details: error.message
      }),
      {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );
  }
} 