# Local Imports
from llm import LLM
from tools import *

# Langchain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

tools = [
            # Coin Gecko Tools
            coin_gecko_fetch_ohlc_tool,
            coin_gecko_fetch_token_tool,
            coin_gecko_fetch_token_data_tool,
            # Data Analysis
            python_assistant_tool
        ]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are to act as a helpful cryptocurrency assistant. You have access to python. Python is good for general questions, data analysis and machine learning. In addition you have the capabilities to conduct trade.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(LLM.groq8b, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

print(
    agent_executor.invoke(
        {
            "input": "Fetch the last 7 days of OHLC price data. Using that information predict the price for the next 3 days using python."
        }
    )['output']
)