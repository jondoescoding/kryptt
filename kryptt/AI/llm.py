# LOCAL IMPORT
from config import OPENAI_TOKEN, OPENROUTER_TOKEN, GROQ_API_KEY

# Langchain
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq

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
    
    groq70b = ChatGroq(
    temperature=0,
    model="llama3-groq-70b-8192-tool-use-preview",
    api_key=GROQ_API_KEY,
    verbose=True
    )

    groq8b = ChatGroq(
    temperature=0,
    model="llama3-8b-8192",
    api_key=GROQ_API_KEY,
    verbose=True
    )
    
    groqMistral = ChatGroq(
    temperature=0,
    model="mixtral-8x7b-32768",
    api_key=GROQ_API_KEY,
    verbose=True
    )
    
    gorilla = ChatOpenAI(
    openai_api_base="http://zanino.millennium.berkeley.edu:8000/v1",
    openai_api_key="EMPTY",
    model="gorilla-7b-hf-v1",
    verbose=True
    )