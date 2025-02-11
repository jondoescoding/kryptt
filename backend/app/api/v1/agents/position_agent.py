from langgraph.prebuilt import create_react_agent
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from ..position import get_crypto_positions
from ..settings import api_keys_store
from langchain_groq import ChatGroq
from typing import AsyncGenerator, Dict, Optional, List
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, AIMessage
import json

router = APIRouter(prefix="/agent", tags=["agent"])

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
    try:
        if "current" not in api_keys_store:
            print("BRUH")
            raise HTTPException(
                status_code=404,
                detail="Alpaca API keys not configured"
            )
            
        keys = api_keys_store["current"]
        
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            api_key=keys["groq"],
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        
        return create_react_agent(
            model=llm,
            tools=[get_crypto_positions],
            name="Alpaca Trading Position Agent",
            prompt="You are a world class data representer with access to a given user's trading positions."
        )
        
    except HTTPException as he:
        raise he

def get_agent():
    """
    Get or create the position agent instance.
    
    Returns:
        The position agent instance
        
    Raises:
        HTTPException: If agent setup fails
    """
    global _position_agent
    if _position_agent is None:
        _position_agent = setup_position_agent()
    return _position_agent

async def stream_agent_response(message: str) -> AsyncGenerator[str, None]:
    """Stream the agent's response."""
    try:
        # Get or initialize agent
        agent = get_agent()
        
        # Create the agent state with messages
        agent_state = {
            "messages": [HumanMessage(content=message)],
            "structured_response": None
        }
        
        # Initialize agent with message
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
        yield json.dumps(response_chunk.model_dump()) + "\n"
        
    except Exception as e:
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
    return StreamingResponse(
        stream_agent_response(request.message),
        media_type="text/event-stream"
    )