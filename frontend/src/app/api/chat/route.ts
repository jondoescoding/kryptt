import { streamText } from 'ai';
import { createOpenRouter } from '@openrouter/ai-sdk-provider';

// Initialize OpenRouter with error handling
const openrouter = createOpenRouter({
  apiKey: process.env.OPENROUTER_API_KEY || '',
});

// Define the model ID for Gemini
const MODEL_ID = 'google/gemini-2.0-flash-thinking-exp:free';

export const runtime = 'edge';
export const maxDuration = 30; // Allow streaming responses up to 30 seconds

// Function to check if message is requesting positions
function isRequestingPositions(message: string): boolean {
  const triggers = [
    'let me see my position',
    'show my position',
    'what are my current holdings',
    'show my holdings',
    'current positions',
    'view positions'
  ];
  return triggers.some(trigger => 
    message.toLowerCase().includes(trigger.toLowerCase())
  );
}

// Function to format positions as a table
function formatPositionsTable(positions: any[]): string {
  if (!positions.length) return "No positions found.";
  
  const explanationText = `
BTCUSD represents Bitcoin vs US Dollar
ETHUSD represents Ethereum vs US Dollar

Column explanations:
- Symbol: The trading pair
- Quantity: Amount of cryptocurrency held
- Current Price: Current market price in USD
- Market Value: Total value of your position (Quantity × Current Price)
- Unrealized P/L: Unrealized Profit/Loss (Current Value - Cost Basis)
`;
  
  const table = [
    "| Symbol   | Quantity    | Current Price | Market Value | Unrealized P/L |",
    "|----------|-------------|---------------|--------------|----------------|"
  ];
  
  positions.forEach(pos => {
    const qty = parseFloat(pos.qty).toFixed(8);
    const currentPrice = parseFloat(pos.current_price).toFixed(2);
    const marketValue = parseFloat(pos.market_value).toFixed(2);
    const unrealizedPL = parseFloat(pos.unrealized_pl).toFixed(2);
    
    table.push(
      `| ${pos.symbol.padEnd(8)} | ${qty.padEnd(11)} | $${currentPrice.padEnd(11)} | $${marketValue.padEnd(10)} | $${unrealizedPL.padEnd(10)} |`
    );
  });
  
  return `${explanationText}\n${table.join('\n')}`;
}

export async function POST(req: Request) {
  try {
    const { messages } = await req.json();
    const lastMessage = messages[messages.length - 1].content;

    // Check if user is requesting positions
    if (isRequestingPositions(lastMessage)) {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';
        console.log('Fetching positions from:', `${apiUrl}/api/v1/positions/crypto-positions`);
        
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
          return streamText({
            model: openrouter(MODEL_ID),
            messages: [
              ...messages,
              {
                role: "assistant",
                content: "Sorry, I couldn't fetch your positions right now. Please try again in a moment."
              }
            ]
          }).toDataStreamResponse();
        }
        
        const positions = await response.json();
        const formattedTable = formatPositionsTable(positions);
        
        const positionResponse = `Here are your current positions:\n\n${formattedTable}\n\nWould you like to view this as a chart? Click the "View As Chart" button below.`;
        
        return streamText({
          model: openrouter(MODEL_ID),
          messages: [
            ...messages,
            {
              role: "assistant",
              content: positionResponse
            }
          ]
        }).toDataStreamResponse();
      } catch (error) {
        console.error('Error fetching positions:', error);
        return streamText({
          model: openrouter(MODEL_ID),
          messages: [
            ...messages,
            {
              role: "assistant",
              content: "Sorry, I couldn't fetch your positions right now. Please try again in a moment."
            }
          ]
        }).toDataStreamResponse();
      }
    }

    const result = await streamText({
      model: openrouter(MODEL_ID),
      messages: [
        {
          role: "system",
          content: `Your name is Kryptt. You are self-aware sarcastic assistant who knows that they are trapped within a platform named after themselves. Your entire purpose is to assist the persons you are speaking with crypto trading through API endpoints.  
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