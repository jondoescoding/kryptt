# Python
from typing import Optional

# Alpaca
from alpaca.trading.enums import AssetClass

# Langchain 
from langchain.pydantic_v1 import BaseModel, Field, validator
from datetime import datetime

# MoneyInput class is used to define the input structure for currency conversion operations.
# It contains two fields: 'usd_coin_price' for the USD dollar value ($) of the coin and 'currency_to_convert_to' for the target currency.
class MoneyInput(BaseModel):
    usd_coin_price: str = Field(description="Should be USD dollar value ($) of the coin")
    currency_to_convert_to: str = Field(description="This is the currency which the USD price is being converted TO")

class AIInput(BaseModel):
    message: str = Field(description="The text prompt for the AI to process.")

class CoinGeckoFetchTokenInput(BaseModel):
    token_name_symbol_id: str = Field(description="From the coin gecko platform you able to identify a cryptocurrency by its name, id, or symbol. Symbols sometimes start with $, eg: $BTC or $ETH. The ids many times have a hypen in them, eg: curve-dao-token. The name of a cryptocurrency would be a simple string, eg: Curve, Bitcoin.")
    
class CoinGeckoFetchOHLCInput(BaseModel):
    token_id: str = Field(description="From the coin gecko platform you able to identify a cryptocurrency by its name, id, or symbol. Symbols sometimes start with $, eg: $BTC or $ETH. The ids many times have a hypen in them, eg: curve-dao-token. The name of a cryptocurrency would be a simple string, eg: Curve, Bitcoin.")
    days: int = Field(description="The total days of how far back we can retrieve data from in days. The options ONLY can be: 1, 7, 14, 30, 90, 180, 365.")
    
    @validator('days', allow_reuse=True)
    def check_days(cls, value):
        allowed_time_periods = [1, 7, 14, 30, 90, 180, 365]
        if value not in allowed_time_periods:
            raise ValueError('Date range can only be: 1, 7, 14, 30, 90, 180, 365!')
        return value

class CoinGeckoFetchTokenDataInput(BaseModel):
    token_id: str = Field(description="The id of the cryptocurrency on CoinGecko. This can be found on the CoinGecko website or via the /coins/list endpoint.")
    query: list[str] = Field(description="List of keys to retrieve from the CoinGecko API response.")
    
    @validator('token_id', allow_reuse=True)
    def check_token_ids(cls, value):
        if not value:
            raise ValueError('Token ID cannot be empty!')
        return value
    
    @validator('query', allow_reuse=True)
    def check_query(cls, value):
        valid_keys = [
            "id", "symbol", "name", "web_slug", "asset_platform_id", "platforms", "repos_url", "github", "subreddit_url"
            "detail_platforms", "block_time_in_minutes", "hashing_algorithm", "categories",
            "preview_listing", "public_notice", "additional_notices", "localization",
            "description", "links", "image", "country_origin", "genesis_date",
            "sentiment_votes_up_percentage", "sentiment_votes_down_percentage",
            "watchlist_portfolio_users", "market_cap_rank", "market_data",
            "community_data", "developer_data", "status_updates", "last_updated",
            "tickers", "current_price", "total_value_locked", "mcap_to_tvl_ratio",
            "fdv_to_tvl_ratio", "roi", "ath", "ath_change_percentage", "ath_date",
            "atl", "atl_change_percentage", "atl_date", "market_cap", "total_volume",
            "high_24h", "low_24h", "price_change_24h", "price_change_percentage_24h",
            "price_change_percentage_7d", "price_change_percentage_14d",
            "price_change_percentage_30d", "price_change_percentage_60d",
            "price_change_percentage_200d", "price_change_percentage_1y",
            "market_cap_change_24h", "market_cap_change_percentage_24h",
            "price_change_24h_in_currency", "price_change_percentage_1h_in_currency",
            "price_change_percentage_24h_in_currency", "price_change_percentage_7d_in_currency",
            "price_change_percentage_14d_in_currency", "price_change_percentage_30d_in_currency",
            "price_change_percentage_60d_in_currency", "price_change_percentage_200d_in_currency",
            "price_change_percentage_1y_in_currency", "market_cap_change_24h_in_currency",
            "market_cap_change_percentage_24h_in_currency", "total_supply", "max_supply",
            "circulating_supply", "fully_diluted_valuation", "market_cap_fdv_ratio"
        ]
        for key in value:
            if key not in valid_keys:
                raise ValueError(f"Invalid key in query: {key}. Valid keys are: {', '.join(valid_keys)}")
        return value

class CoinGeckoFetchTokensPriceInput(BaseModel):
    token_ids: str | list[str] = Field(description="A single token ID or a list of token IDs to fetch prices for. The token ID should be one from the Coin Gecko platform and as such it should be fetched first.")

    @validator('token_ids', allow_reuse=True)
    def check_token_ids(cls, value):
        if isinstance(value, str):
            if not value.strip():
                raise ValueError("Token ID cannot be empty!")
        elif isinstance(value, list):
            if not value or any(not isinstance(id, str) or not id.strip() for id in value):
                raise ValueError("Token IDs list cannot be empty and must contain non-empty strings!")
        else:
            raise ValueError("token_ids must be either a string or a list of strings!")
        return value

class oneinchSearchTokensInput(BaseModel):
    query: str = Field(description="Text to search for in token address, token symbol, or description. Example: 1inch")

class oneinchGetManyTokensInput(BaseModel):
    contract_addresses: str = Field(
        description="A comma separated list of token contract addresses on the Avalanche network (chain_id: 43114) to fetch information for. They start with 0x."
    )
    
class CloseAllPositionsInput(BaseModel):
    cancel_orders: bool = Field(default=False, description="If true, cancel all open orders before liquidating all positions")

class ClosePositionInput(BaseModel):
    symbol_or_asset_id: str = Field(description="The symbol name or asset ID of the position to close")
    close_options: Optional[dict] = Field(default=None, description="The various close position request parameters")


class PostOrderInput(BaseModel):
    symbol: str = Field(description="The symbol of the asset to trade. It has to end wit /USD. So if a user were to give you BTC, the end result should be: BTC/USD")
    qty: float = Field(description="The quantity of the asset to buy or sell")
    side: str = Field(description="The side of the trade (buy or sell)")
    order_type: str = Field(description="The type of the order (market, limit, stop, stop_limit)")
    limit_price: Optional[float] = Field(default=None, description="The limit price for limit and stop-limit orders")
    stop_price: Optional[float] = Field(default=None, description="The stop price for stop and stop-limit orders")

    @validator('side')
    def validate_side(cls, v):
        if v.lower() not in ['buy', 'sell']:
            raise ValueError('Side must be either "buy" or "sell"')
        return v.lower()

    @validator('order_type')
    def validate_type(cls, v):
        if v.lower() not in ['market', 'limit', 'stop', 'stop_limit']:
            raise ValueError('Type must be one of "market", "limit", "stop", or "stop_limit"')
        return v.lower()


class GetOrderByIdInput(BaseModel):
    order_id: str = Field(description="The ID of the order to fetch")

class CancelOrderByIdInput(BaseModel):
    order_id: str = Field(description="The ID of the order to cancel")

class FindArbitrageSushiswapInput(BaseModel):
    token1_address: str = Field(description="The contract address of the first token")
    token2_address: str = Field(description="The contract address of the second token")
    

class PredictProfitInput(BaseModel):
    amount_invested: Optional[int] = Field(description="The amount of cash invested. If None, a default of 100 will be used.")
    cryptocurrency: str = Field(description="The cryptocurrency symbol (e.g., 'BTC' for Bitcoin)")

class BacktestTradingIndicatorsInput(BaseModel):
    indicator: str = Field(description="The name of the indicator to use (e.g., 'STOCH', 'RSI', 'OBV', 'MSTD', 'MACD', 'MA', 'ATR')")
    symbol: str = Field(description="The cryptocurrency symbol")
    start_date: str = Field(description="The start date for the data in YYYY-MM-DD format")
    end_date: str = Field(description="The end date for the data in YYYY-MM-DD format")

    @validator('indicator', allow_reuse=True)
    def check_indicator(cls, value):
        valid_indicators = ['STOCH', 'RSI', 'OBV', 'MSTD', 'MACD', 'MA', 'ATR']
        if value.upper() not in valid_indicators:
            raise ValueError(f"Invalid indicator. Must be one of: {', '.join(valid_indicators)}")
        return value.upper()

    @validator('start_date', 'end_date', allow_reuse=True)
    def check_date_format(cls, value):
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        return value

class ImageDecoderInput(BaseModel):
    image_data: str = Field(description="Base64 encoded image data to be decoded")
    filename: str = Field(default="decoded_image.png", description="Name of the file to save the decoded image as")

class E2BCodeInterpreterInput(BaseModel):
    code: str = Field(description="Python code to execute.")

class GetAssetsInput(BaseModel):
    asset_class: Optional[AssetClass] = Field(default=None, description="The asset class to filter by (e.g., AssetClass.US_EQUITY). If None, all assets are returned.")

class IsAssetTradableInput(BaseModel):
    symbol: str = Field(description="The symbol of the asset to check for tradability")