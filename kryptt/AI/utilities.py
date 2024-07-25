# Python
import os

# Local
from config import TAVILY_API_KEY, E2B_API_KEY

# Langchain
from langchain_community.retrievers import TavilySearchAPIRetriever

# Code Interpreter
from e2b_code_interpreter import CodeInterpreter

# Web search
tavily = TavilySearchAPIRetriever(k=5, tavily_api_key=TAVILY_API_KEY)

def tavily_invoke_func(message: str):
    """
    Search the web using LLMs via the Tavily API.

    Args:
    message (str): The search query or message to be processed by the Tavily API.

    Returns:
    The response from the Tavily API based on the provided message.
    """
    return tavily.invoke(message)

def e2b_code_interpreter_func(code: str):
    """
    Execute Python code using E2B Code Interpreter.

    Args:
    code (str): The Python code to be executed.

    Returns:
    dict: A dictionary containing the execution results, stdout, stderr, and any errors.
    """
    if not E2B_API_KEY:
        raise ValueError("E2B_API_KEY is not set in the environment variables.")
    
    code_interpreter = CodeInterpreter()
    try:
        execution = code_interpreter.notebook.exec_cell(code)
        return {
            "results": execution.results,
            "stdout": execution.logs.stdout,
            "stderr": execution.logs.stderr,
            "error": execution.error,
        }
    finally:
        code_interpreter.close()