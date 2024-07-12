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
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")


# Config For The CEX ARB
ct_config = {
    "exchanges": [
        {
            "name": "kraken",
            "apiKey": os.getenv("KRAKEN_API_KEY"),
            "secret": os.getenv("KRAKEN_SECRET_KEY")
        },
        {
            "name": "bitget",
            "apiKey": os.getenv("BITGET_API_KEY"),
            "secret": os.getenv("BITGET_SECRET_KEY"),
            "password": os.getenv("BITGET_PASSWORD")
        }
    ],
    "usd_amount": 100,
    "usd_price_diff": 5,
    "pause": 6
}