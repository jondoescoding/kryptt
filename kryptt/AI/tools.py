# Local 
from config import OPENAI_TOKEN, OPENROUTER_TOKEN, GROQ_API_KEY
from validation import coinGeckoFetchTokenInput, coinGeckoFetchOHLCInput, coinGeckoFetchTokenDataInput
from coin_gecko_tools import fetch_token, fetch_ohlc_by_id, fetch_coin_data

# Langchain
from langchain.tools import StructuredTool

# Coingecko tools
coin_gecko_fetch_token_tool = StructuredTool.from_function(
    func=fetch_token,
    description="Useful for finding token. Pulls data from coin gecko. This is a tool which is for retrieval of a token's ID from the coin gecko platform. It should be used before any other coin gecko tool in order to get the token's ID for other tools.",
    name="coin_gecko_fetch_token_tool",
    args_schema=coinGeckoFetchTokenInput
)

coin_gecko_fetch_ohlc_tool = StructuredTool(
    func=fetch_ohlc_by_id,
    description="This is a tool which is used to fetch the price data for a specific cryptocurrency",
    name="coin_gecko_fetch_ohlc_tool",
    args_schema=coinGeckoFetchOHLCInput
)

coin_gecko_fetch_token_data_tool = StructuredTool(
    func=fetch_coin_data,
    description="This tool fetches specific data for a cryptocurrency based on the provided query keys.",
    name="coin_gecko_fetch_token_data_tool",
    args_schema=coinGeckoFetchTokenDataInput
)