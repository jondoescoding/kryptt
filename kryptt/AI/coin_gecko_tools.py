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
    """
    Fetches data for a specific cryptocurrency token from the CoinGecko API.

    This function retrieves a list of all available coins from the CoinGecko API and 
    searches for coins that match the provided token name, symbol, or ID. If matching 
    coins are found, they are returned; otherwise, a message indicating no data found 
    is returned.

    Parameters
    ----------
    token_name_symbol_id : str
        The name, symbol, or ID of the cryptocurrency token to search for.

    Returns
    -------
    list[dict] or str
        A list of dictionaries containing the details of the matching coins if found.
        If no matching coins are found, a string message indicating no data found is returned.
        In case of an error, a string message indicating the error is returned.

    Example
    -------
    >>> fetch_token("bitcoin")
    [{'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin'}, ...]

    Raises
    ------
    requests.RequestException
        If an error occurs during the request to the CoinGecko API.
    """
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
        return f"OHLC data fetched successfully for {token_id}:\n{data}"
    except Exception as e:
        log.error(f"An error occurred while fetching OHLC data for coin: {token_id} - {str(e)}")
        return {"error": str(e)}

def fetch_coin_data(token_id: str, query: list[str]):
    """
    Fetches a detailed breakdown of all the information on a token from CoinGecko.

    This function retrieves comprehensive data about a specific cryptocurrency token
    from the CoinGecko API. The data fetched includes various attributes of the token
    such as its name, symbol, market data, community data, and more, based on the 
    specified query parameters.

    Parameters
    ----------
    token_id : str
        The id of the cryptocurrency on CoinGecko. This can be found on the CoinGecko 
        website or via the /coins/list endpoint.
    query : list of str
        List of keys to retrieve from the CoinGecko API response. Valid keys include:
        "id", "symbol", "name", "asset_platform_id", "platforms", "block_time_in_minutes",
        "hashing_algorithm", "categories", "description", "links", "image", "country_origin",
        "genesis_date", "sentiment_votes_up_percentage", "sentiment_votes_down_percentage",
        "market_cap_rank", "market_data", "community_data", "developer_data", "status_updates",
        "last_updated", "tickers", "current_price", "total_value_locked", "mcap_to_tvl_ratio",
        "fdv_to_tvl_ratio", "roi", "ath", "ath_change_percentage", "ath_date", "atl",
        "atl_change_percentage", "atl_date", "market_cap", "total_volume", "high_24h",
        "low_24h", "price_change_24h", "price_change_percentage_24h", "price_change_percentage_7d",
        "price_change_percentage_14d", "price_change_percentage_30d", "price_change_percentage_60d",
        "price_change_percentage_200d", "price_change_percentage_1y", "market_cap_change_24h",
        "market_cap_change_percentage_24h", "price_change_24h_in_currency", "price_change_percentage_1h_in_currency",
        "price_change_percentage_24h_in_currency", "price_change_percentage_7d_in_currency",
        "price_change_percentage_14d_in_currency", "price_change_percentage_30d_in_currency",
        "price_change_percentage_60d_in_currency", "price_change_percentage_200d_in_currency",
        "price_change_percentage_1y_in_currency", "market_cap_change_24h_in_currency",
        "market_cap_change_percentage_24h_in_currency", "total_supply", "max_supply",
        "circulating_supply", "fully_diluted_valuation", "market_cap_fdv_ratio".

    Returns
    -------
    dict
        A dictionary containing the requested data for the specified token. The keys
        in the dictionary correspond to the query parameters provided.

    Raises
    ------
    Exception
        If there is an error fetching data from the CoinGecko API, an exception is raised
        with the error message.

    Notes
    -----
    This function is useful for retrieving specific details about a cryptocurrency token
    for analysis or display purposes. The CoinGecko API provides a wide range of data
    points that can be queried, making it a versatile tool for cryptocurrency data retrieval.

    Examples
    --------
    >>> fetch_coin_data("bitcoin", ["id", "symbol", "name", "market_data"])
    {'id': 'bitcoin', 'symbol': 'btc', 'name': 'Bitcoin', 'market_data': {...}}
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
    
    return f"Feteched Token Data. Here what was found: {result}"

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
        return f"Successfully fetched price data for {token_ids}: {data}"
    except Exception as e:
        log.error(f"An error occurred while fetching price data: {str(e)}")
        return {"error": str(e)}