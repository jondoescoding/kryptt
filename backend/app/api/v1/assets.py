from fastapi import APIRouter, HTTPException
from app.core.logging import logging
from app.core.config import get_trading_client
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus
from .models.alpaca_user_data import TradeAccountResponse
from .settings import api_keys_store

router = APIRouter(prefix="/assets", tags=["alpaca"])

@router.get("/crypto")
async def get_all_available_crypto_assets():
    """
    Retrieves ALL Alpaca trading crypto assets which are available to be traded.
    
    Returns:
        List[Asset]: List of available crypto assets including:
        - Symbol
        - Name
        - Status
        - Tradable flag
        - Asset class details
        
    Raises:
        HTTPException: 
            - 500: Internal server error if Alpaca API call fails
            - 404: If API keys are not configured
    """
    logging.info_with_emoji("Crypto Asset Retrieval has begun...")
    
    try:
        if "current" not in api_keys_store:
            logging.error_with_emoji("API keys not found in store")
            raise HTTPException(
                status_code=404,
                detail="Alpaca API keys not configured"
            )
            
        keys = api_keys_store["current"]
        logging.info_with_emoji("Getting Alpaca Trading Client instance")
        
        trading_client = get_trading_client(keys)
        
        # Search specifically for crypto assets
        search_params = GetAssetsRequest(status=AssetStatus.ACTIVE, asset_class=AssetClass.CRYPTO)
        
        logging.info_with_emoji("Fetching all crypto assets from Alpaca")
        assets = trading_client.get_all_assets(search_params)
        
        logging.info_with_emoji(f"Successfully retrieved {len(assets)} crypto assets")
        return assets
        
    except HTTPException as he:
        logging.error_with_emoji(f"HTTP Exception: {str(he)}")
        raise he
    except Exception as e:
        logging.error_with_emoji(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get crypto assets: {str(e)}"
        )

    