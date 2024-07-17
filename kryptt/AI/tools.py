# Local
from config import GROQ_API_KEY
from validation import coinGeckoFetchTokenInput, coinGeckoFetchOHLCInput, coinGeckoFetchTokenDataInput, MoneyInput, AIInput
from coin_gecko_tools import fetch_token, fetch_ohlc_by_id, fetch_coin_data
from forex_tools import convert_coin_price

# Langchain
from langchain.tools import StructuredTool

# Phidata
from phi.assistant.python import PythonAssistant
from phi.llm.groq import Groq

# Python Tool
python_assistant = PythonAssistant(
    llm=Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY),
    pip_install=True,
    show_function_calls=True,
    run_code=True
)

python_assistant_tool = StructuredTool.from_function(
    func=python_assistant.print_response,
    description="A Python shell for data analysis, predictions, converting natural language dates to UNIX timestamps and machine learning. Use this to execute python commands. Input should be a valid python command.",
    name="python_assistant_tool",
    args_schema=AIInput
)

# This tool converts the given USD coin price to the specified currency using a conversion API.
convert_coin_price_tool = StructuredTool.from_function(
    func=convert_coin_price,
    name="Convert_Coin_Price",
    description="This converts the given USD coin price to the specified currency using a conversion API.",
    args_schema=MoneyInput
)

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