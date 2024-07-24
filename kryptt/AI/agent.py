# Local Imports
from llm import LLM
from tools import *

# Langchain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory

tools = [

            # Coin Gecko
            coin_gecko_fetch_token_tool, # gets the token from the large list
            coin_gecko_fetch_ohlc_tool, # gets OHLC price data from the token
            coin_gecko_fetch_tokens_price_tool, # gets the price of a token
            coin_gecko_fetch_token_data_tool, # gets the misc data from the token
            # Forex
            convert_coin_price_tool, # convert currency
            # 1inch
            oneinch_search_tokens_tool, # search for the token details on avalanche
            oneinch_get_many_tokens_tool, # searches for a list of tokens details on avalanche 
            # Web search
            tavily_tool, # web search
            # Data Analysis
            python_assistant_tool, # python shell
            # Alpaca
            get_accounts_details_tool, 
            get_all_order_tool,
            get_order_by_id_tool,
            cancel_all_order_tool,
            cancel_order_by_id_tool,
            get_open_orders_tool,
            post_order_tool,
            get_positions_tool,
            close_all_positions_tool,
            close_a_position_tool,
            # Traderjoe <-> Sushiswap
            find_arbitrage_sushiswap_traderjoe_tool,
            find_arbitrage_sushiswap_tool,
            find_arbitrage_traderjoe_tool,
            # Vectorbt Tools
            predict_profit_tool,
            backtest_trading_indicators_tool
        ]

memory = ConversationBufferMemory(return_messages=True)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a cryptocurrency social monitor and trading assistant. You have access to the python programming language. Python should be used for: data analysis, data exploration and machine learning. If you don't know the answer to a question, apologize and say you don't know the answer to the question.",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

agent = create_tool_calling_agent(LLM.gpt4o, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    memory=memory
)