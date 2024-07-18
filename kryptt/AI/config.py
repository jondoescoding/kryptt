# Built in imports
import os
from loguru import logger
import uuid
from datetime import datetime

# Python dotenv imports
from dotenv import load_dotenv

# Loading the environmental variables from the containing folder
load_dotenv()

# Get the current file's name without the extension
current_file = os.path.splitext(os.path.basename(__file__))[0]

# Configure logging
logger.remove()  # Remove default handler
logger.add(f'{current_file}.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

# Add a run identifier and separator
run_id = uuid.uuid4()
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info(f"{'='*50}")
logger.info(f"New Run Started - ID: {run_id} - Time: {current_time}")
logger.info(f"{'='*50}")

# Create a named logger
log = logger.bind(name="config_logger")

# GLOBAL VARIABLES
OPENROUTER_TOKEN = os.getenv("OPENROUTER_TOKEN")
OPENAI_TOKEN = os.getenv("OPENAI_TOKEN")
COIN_MARKET_CAP_TOKEN = os.getenv("COIN_MARKET_CAP_TOKEN")
COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
E2B_API_KEY = os.getenv("E2B_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY= os.getenv("ALPACA_SECRET_KEY")
# Export the logger
__all__ = ['log']