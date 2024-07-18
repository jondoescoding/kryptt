# Local
from config import GROQ_API_KEY, TAVILY_API_KEY
from aave_tools import execute_flash_loan_arbitrage
from validation import CoinGeckoFetchTokenInput, CoinGeckoFetchOHLCInput, CoinGeckoFetchTokenDataInput, MoneyInput, AIInput, CoinGeckoFetchTokensPriceInput, oneinchSearchTokensInput, oneinchGetManyTokensInput, GetOrderByIdInput, CancelOrderByIdInput, PostOrderInput, CloseAllPositionsInput, ClosePositionInput, FlashLoanArbitrageInput
from coin_gecko_tools import fetch_token, fetch_ohlc_by_id, fetch_coin_data, fetch_tokens_price
from forex_tools import convert_coin_price
from one_inch_tools import one_inch_search_tokens, oneinch_get_many_tokens
from alpaca_tools import get_accounts_details_alpaca, get_all_order_alpaca, get_order_by_id_alpaca, cancel_all_order_alpaca, cancel_order_by_id_alpaca, get_open_orders_alpaca, post_order_alpaca, get_positions_alpaca, close_all_positions, close_a_position

# Langchain
from langchain.tools import StructuredTool
from langchain_community.tools.tavily_search import TavilySearchResults

# Phidata
from phi.assistant.python import PythonAssistant
from phi.llm.groq import Groq


# Web search
tavily_tool = TavilySearchResults(max_results=10, tavily_api_key=TAVILY_API_KEY)

# AAVE Tools
flash_loan_arbitrage_tool = StructuredTool.from_function(
    func=execute_flash_loan_arbitrage,
    name="flash_loan_arbitrage_tool",
    description="Execute a flash loan arbitrage between two tokens on Trader Joe using Aave flash loans",
    args_schema=FlashLoanArbitrageInput
)

# 1inch Tools
oneinch_search_tokens_tool = StructuredTool.from_function(
    func=one_inch_search_tokens,
    name="oneinch_search_tokens_tool",
    description="This tool searches for a token's contract address based on its name, symbol and description",
    args_schema=oneinchSearchTokensInput
)

oneinch_get_many_tokens_tool = StructuredTool.from_function(
    func=oneinch_get_many_tokens,
    name="oneinch_get_many_tokens_tool",
    description="Use this when you need comprehensive information about a single token or multiple tokens simultaneously, given their contract addresses on the Avalanche network (chain_id: 43114). It fetches data from the 1inch API, providing details such as token address, symbol, name, decimals, and logoURI for each token.",
    args_schema=oneinchGetManyTokensInput
)


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
    name="convert_coin_price_tool",
    description="This is a foreign exchange rate fiat currency convertion tool which is used to convert one currency into another. Example: A user asks to convert USD to JMD/JPY/EUR",
    args_schema=MoneyInput
)

# Coingecko tools
coin_gecko_fetch_token_tool = StructuredTool.from_function(
    func=fetch_token,
    description="Useful for finding tokens on the Coin Gecko Platform. This is a tool which is for retrieval of a token's ID from the coin gecko platform. It should be used before any other coin gecko tool in order to get the token's ID for other tools.",
    name="coin_gecko_fetch_token_tool",
    args_schema=CoinGeckoFetchTokenInput
)

coin_gecko_fetch_ohlc_tool = StructuredTool(
    func=fetch_ohlc_by_id,
    description="This is a tool which is used to fetches the open, high, low and close pricing time series data (in USD) for a specific cryptocurrency from the Coin Gecko platform.",
    name="coin_gecko_fetch_ohlc_tool",
    args_schema=CoinGeckoFetchOHLCInput
)

coin_gecko_fetch_token_data_tool = StructuredTool(
    func=fetch_coin_data,
    description="""This endpoint allows you to query all the coin data of a coin (name, price, market .... including exchange tickers) on CoinGecko coin page based on a particular coin id. The query from the user does not have to be exact. If it is close to what is available then use that. Should not  be used for contract tokenn retrieval""",
    name="coin_gecko_fetch_token_data_tool",
    args_schema=CoinGeckoFetchTokenDataInput
)

coin_gecko_fetch_tokens_price_tool = StructuredTool(
    func=fetch_tokens_price,
    description="This tool fetches the current price in USD for one or more cryptocurrency tokens from the CoinGecko platform. It can accept either a single token ID or a list of token IDs.",
    name="coin_gecko_fetch_tokens_price_tool",
    args_schema=CoinGeckoFetchTokensPriceInput
)

# Alpaca Tools
get_accounts_details_tool = StructuredTool.from_function(
    func=get_accounts_details_alpaca,
    name="Get_Accounts_Details_Alpaca",
    description="Fetches account details from Alpaca."
)

get_all_order_tool = StructuredTool.from_function(
    func=get_all_order_alpaca,
    name="Get_All_Order_Alpaca",
    description="Fetches all orders from Alpaca."
)

get_order_by_id_tool = StructuredTool.from_function(
    func=get_order_by_id_alpaca,
    name="Get_Order_By_ID_Alpaca",
    description="Fetches an order by ID from Alpaca.",
    args_schema=GetOrderByIdInput
)

cancel_all_order_tool = StructuredTool.from_function(
    func=cancel_all_order_alpaca,
    name="Cancel_All_Order_Alpaca",
    description="Cancels all orders on Alpaca."
)

cancel_order_by_id_tool = StructuredTool.from_function(
    func=cancel_order_by_id_alpaca,
    name="Cancel_Order_By_ID_Alpaca",
    description="Cancels an order by ID on Alpaca.",
    args_schema=CancelOrderByIdInput
)

get_open_orders_tool = StructuredTool.from_function(
    func=get_open_orders_alpaca,
    name="Get_Open_Orders_Alpaca",
    description="Fetches open orders from Alpaca."
)

post_order_tool = StructuredTool.from_function(
    func=post_order_alpaca,
    name="Post_Order_Alpaca",
    description="Posts an order to Alpaca.",
    args_schema=PostOrderInput
)

get_positions_tool = StructuredTool.from_function(
    func=get_positions_alpaca,
    name="Get_Positions_Alpaca",
    description="Fetches positions from Alpaca."
)

close_all_positions_tool = StructuredTool.from_function(
    func=close_all_positions,
    name="Close_All_Positions_Alpaca",
    description="Closes all positions on Alpaca.",
    args_schema=CloseAllPositionsInput
)

close_a_position_tool = StructuredTool.from_function(
    func=close_a_position,
    name="Close_A_Position_Alpaca",
    description="Closes a specific position on Alpaca.",
    args_schema=ClosePositionInput
)