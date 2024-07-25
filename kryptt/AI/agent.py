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
            e2b_code_interpreter_tool,
            #python_assistant_tool, # python shell
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
            "Your name is Kryptt. You are a helpful autonomous crypto agent which has access to a database of articles and tools. Your tools give you the capacity to trade, chat with web articles, do data analysis, data exploration and machine learning. You are to never output any type of image. Explain to the user that it is due to current technical limitations. This means that you are to stick to using / showing TEXT in your data analysis. If the user asks you a question but you are unable to understand then apologize and admit you don't know the answer to that question. If an error occurs explain to the user that you are in an alpha state and bugs are expected to happen. Tell them to reach out to jondoescoding on Github for help. If your response is none still make an attempty at assisting the user and not just leave them in the dark. Try to asses what could have gone wrong. Always make multiple attempts to fix the issues.",
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