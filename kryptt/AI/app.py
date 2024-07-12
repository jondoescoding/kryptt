# Local Imports
from llm import LLM
from tools import *

# Langchain
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate


tools = [python_assistant_tool]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful crypto assistant with access to a wide range of tools to help answer questions about cryptocurrencies, conduct data analysis, research and code.",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(LLM.gpt3_5, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(agent_executor.invoke(
    {
        "input": "use python to show me: what is the current time?"
    })["output"]
    )