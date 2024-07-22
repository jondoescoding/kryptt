# Local
from config import COINGECKO_API_KEY, log

# HTTP
import requests

def fetch_data(url, headers):
    """
    Fetches data from a given URL using the provided headers.

    Args:
        url (str): The URL to fetch data from.
        headers (dict): The headers to include in the request.

    Returns:
        dict or None: The JSON response from the server if the request is successful.
        If an error occurs, a dictionary with the error message is returned.

    Raises:
        requests.RequestException: If an error occurs during the request.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        log.success("Response successful")
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def fetch_token(token_name_symbol_id: str):
    url = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"

    headers = {
        "accept": "application/json",
        "X-CMC_PRO_API_KEY": COINGECKO_API_KEY
    }
    
    log.info(f"Fetching data for coin: {token_name_symbol_id}")
    try:
        coins = fetch_data(url, headers)
        matching_coins = []
        for coin in coins:
            if token_name_symbol_id.lower() in [coin["name"].lower(), coin["symbol"].lower(), coin["id"].lower()]:
                matching_coins.append(coin)
        
        if matching_coins:
            log.success(f"Tokens/Coins found for: {token_name_symbol_id}")
            return matching_coins
        else:
            log.warning(f"No data found for the provided coin: {token_name_symbol_id}")
            return f"No data found for the provided coin: {token_name_symbol_id}"
    except Exception as e:
        log.error(f"An error occurred while fetching data for coin: {token_name_symbol_id} - {str(e)}")
        return f"An error occurred: {str(e)}"

def fetch_ohlc_by_id(token_id: str, days: int | None):
    """
    Fetches the OHLC (Open, High, Low, Close) data for a specific cryptocurrency coin based on the coin name and number of days provided.

    Args:
        token_id (str): The name of the cryptocurrency coin for which to retrieve OHLC data.
        days (int): The number of days of OHLC data to fetch.

    Returns:
        The OHLC data for the specified coin over the specified number of days.
    """
    if days is None:
        days = 100  # Default to 100 days if not provided

    url = f"https://api.coingecko.com/api/v3/coins/{token_id}/ohlc?vs_currency=usd&days={days}&precision=full"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }
    
    log.info(f"Fetching OHLC data for coin: {token_id} for {days} days")
    try:
        data = fetch_data(url, headers)
        log.info(f"OHLC data fetched successfully for coin: {token_id}")
        return data
    except Exception as e:
        log.error(f"An error occurred while fetching OHLC data for coin: {token_id} - {str(e)}")
        return {"error": str(e)}

def fetch_coin_data(token_id: str, query: list[str]):
    """
    Fetches a detail breakdown of all the information on a token.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{token_id}"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }
    
    data = fetch_data(url, headers)
    
    if "error" in data:
        raise Exception(f"Error fetching data: {data['error']}")
    
    # Extract relevant data based on query
    result = {key: data.get(key) for key in query}
    
    return result

def fetch_tokens_price(token_ids: str | list[str]):
    """
    Fetches the current price in USD for one or more tokens from CoinGecko.

    Args:
        token_ids (str | list[str]): A single token ID or a list of token IDs.

    Returns:
        dict: A dictionary with token IDs as keys and their USD prices as values.
    """
    log.info(f"Fetching price data for token(s): {token_ids}")
    
    if isinstance(token_ids, str):
        token_ids = [token_ids]
    
    ids_param = ",".join(token_ids)
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids_param}&vs_currencies=usd"
    
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": COINGECKO_API_KEY
    }
    
    try:
        data = fetch_data(url, headers)
        if "error" in data:
            log.error(f"Error fetching price data: {data['error']}")
            return {"error": data['error']}
        
        log.success(f"Successfully fetched price data for token(s): {token_ids}")
        return data
    except Exception as e:
        log.error(f"An error occurred while fetching price data: {str(e)}")
        return {"error": str(e)}