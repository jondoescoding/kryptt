# Local Imports
from llm import LLM
from tools import *

# Langchain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

tools = [

            # Coin Gecko
            coin_gecko_fetch_ohlc_tool, # gets price data from the token 
            #coin_gecko_fetch_token_tool, # gets the token from the large list
            coin_gecko_fetch_token_data_tool, # gets the misc data from the token
            # 1inch
            oneinch_search_tokens_tool,
            oneinch_get_many_tokens_tool,
            # Coin Gecko PT 2 -> Placed here since Groq runs tools in sequence
            coin_gecko_fetch_tokens_price_tool, # gets the price of a token
            # Web search
            tavily_tool,
            # Data Analysis
            python_assistant_tool,
            # Forex
            convert_coin_price_tool,
            # Alpaca
            get_accounts_details_tool, get_all_order_tool,
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

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a cryptocurrency social monitor and trading assistant. You have access to python. Python is good for general questions, data analysis, machine learning and the capabilities to conduct trade. If you don't know the answer to a question, then apologize and say you don't know the answer to the question.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(LLM.groq70b, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

