# Built in imports
import os

# Python dotenv imports
from dotenv import load_dotenv

# Loading the environmental variables from the containing folder
load_dotenv()

# GLOBAL VARIABLES
OPENROUTER_TOKEN = os.getenv("OPENROUTER_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
COIN_MARKET_CAP_TOKEN = os.getenv("COIN_MARKET_CAP_TOKEN")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
