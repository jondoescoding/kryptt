"""
Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
Date: January 2024
"""

from langgraph.prebuilt import create_react_agent
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.api.v1.tools.position import get_crypto_positions, get_open_position, close_a_position
from ..settings import api_keys_store
from langchain_openai import ChatOpenAI
from typing import AsyncGenerator, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage
from app.core.logging import logging
import json
import time

router = APIRouter(prefix="/agents/position-agent", tags=["agents"])

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(
        ...,
        description="The message to send to the agent",
        example="What are my current crypto positions?"
    )

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    role: str = Field("assistant", description="The role of the message sender")
    content: str = Field(..., description="The message content")

# Global variable to store the agent instance
_position_agent: Optional[object] = None

def setup_position_agent():
    """
    Sets up and returns the position agent with proper error handling.
    
    Returns:
        The configured position agent
        
    Raises:
        HTTPException: If API keys are not configured or other setup errors occur
    """
    logging.info_with_emoji("🤖 Setting up position agent...")
    try:
        if "current" not in api_keys_store:
            logging.error_with_emoji("🔑 API keys not found in store")
            raise HTTPException(
                status_code=404,
                detail="Alpaca API keys not configured"
            )
            
        keys = api_keys_store["current"]
        logging.info_with_emoji("🔑 API keys retrieved successfully")
    
        logging.info_with_emoji("🧠 Initializing ChatOpenAI model...")
        llm = ChatOpenAI(
            model="gpt-4o",
            api_key=keys["groq"],
            temperature=0.1,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        
        logging.info_with_emoji("🛠️ Creating React agent...")
        agent = create_react_agent(
            model=llm,
            tools=[get_crypto_positions, get_open_position, close_a_position],
            name="Alpaca-Trading-Position-Agent-Trading-Bot",
            prompt="You are a trader bot. You will be given tasks to carry out which involve: opening a position, closing a position and getting details about a specific position."
        )
        
        logging.info_with_emoji("✅ Position agent setup completed successfully")
        return agent
        
    except HTTPException as he:
        logging.error_with_emoji(f"❌ HTTP Exception during agent setup: {str(he)}")
        raise he
    except Exception as e:
        logging.error_with_emoji(f"❌ Unexpected error during agent setup: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to setup position agent: {str(e)}"
        )

def get_agent():
    """
    Get or create the position agent instance.
    
    Returns:
        The position agent instance
        
    Raises:
        HTTPException: If agent setup fails
    """
    global _position_agent
    logging.info_with_emoji("🤖 Getting position agent instance...")
    if _position_agent is None:
        logging.info_with_emoji("🆕 Creating new position agent instance...")
        _position_agent = setup_position_agent()
    return _position_agent

async def stream_agent_response(message: str) -> AsyncGenerator[str, None]:
    """Stream the agent's response."""
    start_time = time.time()
    logging.info_with_emoji(f"📝 Processing message: {message}")
    
    try:
        # Get or initialize agent
        agent = get_agent()
        
        # Create the agent state with messages
        agent_state = {
            "messages": [HumanMessage(content=message)],
            "structured_response": None
        }
        
        # Initialize agent with message
        logging.info_with_emoji("🤖 Invoking agent...")
        agent_response = await agent.ainvoke(agent_state)
        
        # Extract the last message from the response
        if agent_response.get("messages"):
            last_message = agent_response["messages"][-1]
            content = last_message.content if isinstance(last_message, AIMessage) else str(last_message)
        else:
            content = str(agent_response.get("structured_response", "No response generated"))
        
        # Stream the response in chunks
        response_chunk = ChatResponse(
            role="assistant",
            content=content
        )
        
        processing_time = time.time() - start_time
        logging.info_with_emoji(f"✅ Response generated in {processing_time:.2f} seconds")
        
        yield json.dumps(response_chunk.model_dump()) + "\n"
        
    except Exception as e:
        logging.error_with_emoji(f"❌ Error generating response: {str(e)}")
        error_chunk = ChatResponse(
            role="assistant",
            content=f"Error: {str(e)}"
        )
        yield json.dumps(error_chunk.model_dump()) + "\n"

@router.post("/chat", 
    description="""
    Chat with the position agent to get information about your crypto positions.
    
    Example queries:
    - "What are my current crypto positions?"
    - "Show me my biggest positions"
    - "Calculate my total portfolio value"
    - "Which positions are in profit?"
    """
)
async def chat_with_agent(request: ChatRequest):
    """
    Chat endpoint that streams responses from the position agent.
    
    Args:
        request: ChatRequest containing the user's message
        
    Returns:
        StreamingResponse: Streamed agent responses
    """
    logging.info_with_emoji(f"📨 Received chat request: {request.message}")
    return StreamingResponse(
        stream_agent_response(request.message),
        media_type="text/event-stream"
    )