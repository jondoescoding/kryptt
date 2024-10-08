# Local
from config import GROQ_API_KEY, TAVILY_API_KEY
from traderjoe_tools import find_arbitrage_traderjoe
from sushiswap_tools import find_arbitrage_sushiswap
from validation import CoinGeckoFetchTokenInput, CoinGeckoFetchOHLCInput, CoinGeckoFetchTokenDataInput, MoneyInput, AIInput, CoinGeckoFetchTokensPriceInput, oneinchSearchTokensInput, oneinchGetManyTokensInput, GetOrderByIdInput, CancelOrderByIdInput, PostOrderInput, CloseAllPositionsInput, ClosePositionInput, FindArbitrageSushiswapInput, PredictProfitInput, BacktestTradingIndicatorsInput, GetAssetsInput, IsAssetTradableInput
from coin_gecko_tools import fetch_token, fetch_ohlc_by_id, fetch_coin_data, fetch_tokens_price
from forex_tools import convert_coin_price
from one_inch_tools import one_inch_search_tokens, oneinch_get_many_tokens
from alpaca_tools import get_accounts_details_alpaca, get_all_order_alpaca, get_order_by_id_alpaca, cancel_all_order_alpaca, cancel_order_by_id_alpaca, get_open_orders_alpaca, post_order_alpaca, get_positions_alpaca, close_all_positions, close_a_position, get_all_assets_alpaca, is_asset_tradable_alpaca
from traderjoe_sushiswap import find_arbitrage_sushiswap_traderjoe
from backtesting import predict_profit_from_the_past, backtest_with_trading_indicators
from utilities import tavily_invoke_func, e2b_code_interpreter_func
from validation import E2BCodeInterpreterInput

# Langchain
from langchain.tools import StructuredTool

# Phidata
from phi.assistant.python import PythonAssistant
from phi.llm.groq import Groq



tavily_tool = StructuredTool(
    name="web_search_tool",
    func=tavily_invoke_func,
    description="This tool is useful for when you need to answer questions about current events.",
    args_schema=AIInput
)

# 1inch Tools
oneinch_search_tokens_tool = StructuredTool.from_function(
    func=one_inch_search_tokens,
    name="oneinch_search_tokens_tool",
    description="This tool should be used to search for a single token contract addresses. It searches for a single token's contract address based on its name OR symbol. This tool should be used for finding out information on tokens from the Avalanche blockchain",
    args_schema=oneinchSearchTokensInput
)

oneinch_get_many_tokens_tool = StructuredTool.from_function(
    func=oneinch_get_many_tokens,
    name="oneinch_get_many_tokens_tool",
    description="This tool should be used to search for multiple token addresses on the Avalanche blockchain. It uses the contract address to find relevant information on the given token.",
    args_schema=oneinchGetManyTokensInput
)

# Python Tool
python_assistant = PythonAssistant(
    llm=Groq(model="llama3-70b-8192", api_key=GROQ_API_KEY),
    pip_install=True,
    show_function_calls=True,
    run_code=True,
    list_files=True,
    run_files=True,
    read_files=True
)

python_assistant_tool = StructuredTool.from_function(
    func=python_assistant.print_response,
    description="A Python shell for data analysis, predictions, converting natural language dates to UNIX timestamps and machine learning. Use this to execute python commands. Input should be a valid python command. Output will never contain images and should be text only. Do NOT run matplotlib GUI.",
    name="python_assistant_tool",
    args_schema=AIInput
)

# This tool converts the given USD coin price to the specified currency using a conversion API.
convert_coin_price_tool = StructuredTool.from_function(
    func=convert_coin_price,
    name="convert_coin_price_tool",
    description="This is a foreign exchange rate fiat currency convertion tool which is used to convert one currency into another. Example: A user asks to convert USD to JMD/JPY/EUR or any other type of country's currency",
    args_schema=MoneyInput
)

# Coingecko tools
coin_gecko_fetch_token_tool = StructuredTool.from_function(
    func=fetch_token,
    description="This is a tool which is for retrieval of a token's ID from the coin gecko platform. It should be used before any other coin gecko tool in order to get the token's ID for other tools which interact with the Coin Gecko Platform.",
    name="coin_gecko_fetch_token_tool",
    args_schema=CoinGeckoFetchTokenInput
)

coin_gecko_fetch_ohlc_tool = StructuredTool(
    func=fetch_ohlc_by_id,
    description="This tool retrieves the Open High Low and Close price data for a requested token from the Coin Gecko platform. It needs the token_id and days in order to work. The token_id is what you use to identify the cryptocurrency. The token_id can be name, id, or symbol. The name of a cryptocurrency would be a simple string, eg: Curve, Bitcoin. The ids many times have a hypen in them, eg: curve-dao-token. Symbols sometimes start with $, eg: $BTC or $ETH. The days for which can be requested are ONLY: 1, 7, 14, 30, 90, 180, 365.",
    name="coin_gecko_fetch_ohlc_tool",
    args_schema=CoinGeckoFetchOHLCInput
)

coin_gecko_fetch_token_data_tool = StructuredTool(
    func=fetch_coin_data,
    description="""This tool allows you to query ALL token data (name, price, market .... including exchange tickers) on CoinGecko based on a particular token_id. The query from the user does not have to be exact. If it is close to what is available then use that. Should not be used for token contract address retrieval.""",
    name="coin_gecko_fetch_token_data_tool",
    args_schema=CoinGeckoFetchTokenDataInput
)

coin_gecko_fetch_tokens_price_tool = StructuredTool(
    func=fetch_tokens_price,
    description="This tool fetches the current price (in USD) for one OR more tokens from the CoinGecko platform. This tool is not for any specific blockchain's price. It is only for USD. It can accept either a single token ID or a list of token IDs.",
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
    description="Posts an order to Alpaca. Supports market, limit, stop, and stop-limit orders.",
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

find_arbitrage_sushiswap_traderjoe_tool = StructuredTool.from_function(
    func=find_arbitrage_sushiswap_traderjoe,
    name="find_arbitrage_sushiswap_traderjoe_tool",
    description="Finds arbitrage opportunities between ONLY both TraderJoe AND SushiSwap for two given token addresses on ONLY the Avalanche network",
    args_schema=FindArbitrageSushiswapInput
)

find_arbitrage_sushiswap_tool = StructuredTool.from_function(
    func=find_arbitrage_sushiswap,
    name="find_arbitrage_sushiswap_tool",
    description="Finds arbitrage opportunities within ONLY SushiSwap for two given tokens on the Avalanche network",
    args_schema=FindArbitrageSushiswapInput
)

find_arbitrage_traderjoe_tool = StructuredTool.from_function(
    func=find_arbitrage_traderjoe,
    name="find_arbitrage_traderjoe_tool",
    description="Finds arbitrage opportunities within ONLY Traderjoe for two given tokens on the Avalanche network",
    args_schema=FindArbitrageSushiswapInput
)

predict_profit_tool = StructuredTool.from_function(
    func=predict_profit_from_the_past,
    name="predict_profit_tool",
    description="Predicts the percentage potential profit based on the amount invested in a cryptocurrency using historical data.",
    args_schema=PredictProfitInput
)

backtest_trading_indicators_tool = StructuredTool.from_function(
    func=backtest_with_trading_indicators,
    name="backtest_trading_indicators_tool",
    description="Applies a specific trading indicator to given OHLCV data and returns the profit.",
    args_schema=BacktestTradingIndicatorsInput
)

e2b_code_interpreter_tool = StructuredTool.from_function(
    func=e2b_code_interpreter_func,
    name="e2b_code_interpreter",
    description="Execute Python code in a Jupyter notebook cell and returns any rich data (e.g., charts), stdout, stderr, and error.",
    args_schema=E2BCodeInterpreterInput
)

get_all_assets_tool = StructuredTool.from_function(
    func=get_all_assets_alpaca,
    name="Get_All_Assets_Alpaca",
    description="Fetches a list of assets from Alpaca. Can be filtered by asset class.",
    args_schema=GetAssetsInput
)

is_asset_tradable_tool = StructuredTool.from_function(
    func=is_asset_tradable_alpaca,
    name="Is_Asset_Tradable_Alpaca",
    description="Checks if a particular asset is tradable on Alpaca.",
    args_schema=IsAssetTradableInput
)