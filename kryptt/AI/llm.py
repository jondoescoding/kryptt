# LOCAL IMPORT
from config import OPENAI_TOKEN, OPENROUTER_TOKEN

# Langchain
from langchain_openai import ChatOpenAI

def ChatOpenRouter(model: str, temperature: int) -> ChatOpenAI:
    """
    Creates a ChatOpenAI object with the specified model and temperature.

    Parameters:
        model (str): The name of the model to be used.
        temperature (int): The temperature parameter for generating responses.

    Returns:
        ChatOpenAI: A ChatOpenAI object with the specified model, API key, API base, temperature, and verbose set to True.
    """
    return ChatOpenAI(
            model=model,
            openai_api_key = OPENROUTER_TOKEN,
            openai_api_base = 'https://openrouter.ai/api/v1',
            temperature=temperature,
            verbose=True
    )


class LLM():
    """Class of LLMs"""
    
    # Free AI Models we will be using 
    mistral = ChatOpenRouter(
        model="mistralai/mistral-7b-instruct:free",
        temperature=0
    )

    mythomist = ChatOpenRouter(
        model="gryphe/mythomist-7b:free",
        temperature=0
    )
    
    llama3 = ChatOpenRouter(
        model="meta-llama/llama-3-8b-instruct:free",
        temperature=0
    )
    
    phi3 = ChatOpenRouter(
        model="microsoft/phi-3-medium-128k-instruct:free",
        temperature=0
    )
    
    gpt3_5 = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0,
        api_key=OPENAI_TOKEN,
        verbose=True
    )
    
    gpt4o = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        api_key=OPENAI_TOKEN,
        verbose=True
    )

