from fastapi import APIRouter, HTTPException
import logging
from .models.settings import APIKeys

router = APIRouter(prefix="/settings", tags=["settings"])

# In-memory storage (this will be lost when server restarts)
api_keys_store = {}

def mask_key(key: str, visible_chars: int = 4) -> str:
    """Mask sensitive key data, showing only the last few characters."""
    if not key:
        return ""
    return f"{'*' * (len(key) - visible_chars)}{key[-visible_chars:]}"

@router.post("/keys")
async def save_api_keys(keys: APIKeys):
    try:
        # Store keys in memory
        api_keys_store["current"] = keys.model_dump()
        
        # Log masked versions of the keys
        logging.info(
            "API keys saved: %s",
            {
                "groq": f"gsk_...{keys.groq[-4:] if keys.groq else ''}",
                "alpaca_api_key": mask_key(keys.alpaca_api_key),
                "alpaca_secret_key": mask_key(keys.alpaca_secret_key),
                "alpaca_endpoint": keys.alpaca_endpoint
            }
        )
        return {"message": "API keys saved successfully"}
    except Exception as e:
        logging.error(f"Failed to save API keys: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/keys")
async def get_api_keys():
    try:
        if "current" not in api_keys_store:
            return {"message": "No API keys found"}
        return api_keys_store["current"]
    except Exception as e:
        logging.error(f"Failed to retrieve API keys: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 