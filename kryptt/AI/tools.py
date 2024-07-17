# Local 
from config import OPENAI_TOKEN, OPENROUTER_TOKEN, GROQ_API_KEY
from validation import coinGeckoFetchTokenInput, coinGeckoFetchOHLCInput, AIInput
from e2b2_tool import CodeInterpreterFunctionTool
from coin_gecko_tools import fetch_token, fetch_ohlc_by_id
from phi.assistant.python import PythonAssistant
from phi.llm.groq import Groq

# Langchain
from langchain.tools import StructuredTool

# Python Shell From E2B
e2b_code_interpreter_tool = CodeInterpreterFunctionTool().to_langchain_tool()



# Phi Data
python_assistant = PythonAssistant(
    llm=Groq(model="llama3-8b-8192", api_key=GROQ_API_KEY),
    pip_install=True,
    run_code=True,
    read_files=True,
    list_files=True,
    debug_mode=True
)
python_assistant_tool = StructuredTool.from_function(
    func=python_assistant.print_response,
    name="python_assistant_tool",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command.",
    args_schema=AIInput
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