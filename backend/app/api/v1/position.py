from fastapi import APIRouter, HTTPException
from app.core.logging import logging
from app.core.config import get_trading_client
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.models import Position
from .settings import api_keys_store
from typing import Union, Any, List, Dict

router = APIRouter(prefix="/positions", tags=["alpaca"])

@router.get("/all-positions")
async def get_all_available_crypto_assets() -> Union[List[Position], Dict[str, Any]]:
    """
    Retrieves ALL of the users positions (open or closed).
    
    Returns:
        List[Position]

    Raises:
        HTTPException: 
            - 500: Internal server error if Alpaca API call fails
            - 404: If API keys are not configured
    """
    logging.info_with_emoji("Crypto Asset Retrieval has begun...")