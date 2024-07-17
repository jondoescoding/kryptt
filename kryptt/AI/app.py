# Local Imports
from llm import LLM
from tools import *

# Langchain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

tools = [
            python_assistant_tool, 
            coin_gecko_fetch_ohlc_tool,
            coin_gecko_fetch_token_tool
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

agent = create_tool_calling_agent(LLM.gorilla, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

print(
    agent_executor.invoke(
        {
            "input": "Fetch the OHLC data of the curve token data from the last 7 days. Use machine learning to predict the price for the next 2 days using the fetched data."
        }
    )['output']
)