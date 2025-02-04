from fastapi import APIRouter, HTTPException
from app.core.logging import logging
from alpaca.trading.client import TradingClient
from .models.alpaca_user_data import TradeAccountResponse
from .settings import api_keys_store

router = APIRouter(prefix="/alpaca", tags=["alpaca"])

@router.post("/account", response_model=TradeAccountResponse)
async def get_account_details():
    """
    Retrieve Alpaca trading account details.
    
    Returns:
        TradeAccountResponse: Account information including:
        - Account status and numbers
        - Buying power and cash balances
        - Portfolio values and margins
        - Trading permissions and restrictions
        
    Raises:
        HTTPException: 
            - 500: Internal server error if Alpaca API call fails
            - 404: If API keys are not configured
    """
    try:
        if "current" not in api_keys_store:
            raise HTTPException(
                status_code=404,
                detail="Alpaca API keys not configured"
            )
            
        keys = api_keys_store["current"]
        trading_client = TradingClient(
            api_key=keys["alpaca_api_key"],
            secret_key=keys["alpaca_secret_key"], 
            paper=True
        )

        client_information = trading_client.get_account()
        
        logging.info_with_emoji(
            "Client Information retrieved Successfully"
        )
        return client_information
        
    except Exception as e:
        logging.error_with_emoji(f"Failed to get account details: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
