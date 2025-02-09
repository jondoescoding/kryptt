from fastapi import APIRouter, HTTPException
from app.core.logging import logging
from app.core.config import get_trading_client
from alpaca.trading.models import Position
from alpaca.trading.enums import AssetClass
from .settings import api_keys_store
from typing import Union, Any, List, Dict
from operator import attrgetter

router = APIRouter(prefix="/positions", tags=["alpaca"])

@router.get("/crypto-positions")
async def get_crypto_positions() -> Union[List[Position], Dict[str, Any]]:
    """
    Retrieves all crypto positions (open or closed) sorted by current price.
    
    Returns:
        List[Position]: Sorted list of crypto positions including:
        - symbol: Asset symbol
        - exchange: Exchange name
        - asset_class: Asset class type
        - asset_marginable: Marginability flag
        - avg_entry_price: Average entry price
        - qty: Position quantity
        - side: Position side (long/short)
        - market_value: Total position value
        - cost_basis: Total cost basis
        - unrealized_pl: Unrealized P/L
        - unrealized_plpc: Unrealized P/L percent
        - unrealized_intraday_pl: Today's unrealized P/L
        - unrealized_intraday_plpc: Today's unrealized P/L percent
        - current_price: Current price per share
        - lastday_price: Previous day's closing price
        - change_today: Today's price change percentage
        - swap_rate: Current exchange rate
        - avg_entry_swap_rate: Entry exchange rate
        - usd: USD position values
        - qty_available: Available quantity

    Raises:
        HTTPException: 
            - 500: Internal server error if Alpaca API call fails
            - 404: If API keys are not configured
    """
    logging.info_with_emoji("🔍 Starting crypto positions retrieval...")
    
    try:
        if "current" not in api_keys_store:
            logging.error_with_emoji("🚫 API keys not found in store")
            raise HTTPException(
                status_code=404,
                detail="Alpaca API keys not configured"
            )
            
        keys = api_keys_store["current"]
        logging.info_with_emoji("🔑 Initializing Alpaca Trading Client")
        
        trading_client = get_trading_client(keys)
        
        logging.info_with_emoji("📊 Fetching all positions from Alpaca")
        all_positions = trading_client.get_all_positions()
        
        logging.info_with_emoji("🔎 Filtering for crypto positions")
        crypto_positions = [
            position for position in all_positions 
            if position.asset_class == AssetClass.CRYPTO
        ]
        
        logging.info_with_emoji("📈 Sorting positions by current price")
        sorted_positions = sorted(
            crypto_positions,
            key=lambda x: float(x.current_price or 0),
            reverse=True
        )
        
        logging.info_with_emoji(f"✅ Successfully retrieved {len(sorted_positions)} crypto positions")
        return sorted_positions
        
    except HTTPException as he:
        logging.error_with_emoji(f"❌ HTTP Exception: {str(he)}")
        raise he
    except Exception as e:
        logging.error_with_emoji(f"❌ Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get crypto positions: {str(e)}"
        )