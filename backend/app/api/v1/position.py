from fastapi import APIRouter, HTTPException
from app.core.logging import logging
from app.core.config import get_trading_client
from alpaca.trading.enums import AssetClass
from .settings import api_keys_store
from typing import List
from .models.position import CryptoPosition

router = APIRouter(prefix="/positions", tags=["alpaca"])

@router.get("/crypto-positions", response_model=List[CryptoPosition])
async def get_crypto_positions() -> List[CryptoPosition]:
    """
    Retrieves all crypto positions (open or closed) sorted by current price.
    Filters out null values and converts numeric nulls to "0".
    
    Returns:
        List[CryptoPosition]: Sorted list of crypto positions with standardized values
    
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
        
        logging.info_with_emoji("🧹 Cleaning position data and removing null values")
        cleaned_positions = []
        null_field_count = 0
        
        for position in crypto_positions:
            position_dict = position.dict()
            # Remove asset_id
            position_dict.pop('asset_id', None)
            
            # Convert numeric nulls to "0"
            numeric_fields = [
                'market_value', 'unrealized_pl', 'unrealized_plpc',
                'unrealized_intraday_pl', 'unrealized_intraday_plpc',
                'current_price', 'lastday_price', 'change_today',
                'swap_rate', 'avg_entry_swap_rate', 'qty_available'
            ]
            
            for field in numeric_fields:
                if position_dict.get(field) is None:
                    position_dict[field] = "0"
                    null_field_count += 1
            
            cleaned_positions.append(CryptoPosition(**position_dict))
            
        logging.info_with_emoji(f"🔄 Converted {null_field_count} null numeric values to '0'")
        
        logging.info_with_emoji("📈 Sorting positions by current price")
        sorted_positions = sorted(
            cleaned_positions,
            key=lambda x: float(x.current_price),
            reverse=True
        )
        
        logging.info_with_emoji(f"✅ Successfully retrieved and cleaned {len(sorted_positions)} crypto positions")
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