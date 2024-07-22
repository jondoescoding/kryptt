from time import sleep
from coin_gecko_tools import fetch_data
from config import log

def one_inch_search_tokens(query: str):
    log.info(f"Starting 1inch token search for query: {query}")
    url = "https://api.1inch.dev/token/v1.2/43114/search"
    
    params = {
        "query": query,
        "ignore_listed": "false",
        "only_positive_rating": "true",
        "limit": 10
    }
    log.debug(f"Search parameters: {params}")
    
    headers = {
        "Authorization": "Bearer GyI1FUwHQn9bAIpyg2Eugzq1NmXbY20G"
    }
    log.debug("Headers prepared")
    
    # Construct the full URL with query parameters
    full_url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    log.debug(f"Full URL constructed: {full_url}")
    
    log.info("Sending request to 1inch API")
    response = fetch_data(full_url, headers)
    sleep(5)
    
    if "error" not in response:
        log.success("Successfully retrieved token search results from 1inch API")
        return response
    else:
        error_message = f"Error: {response['error']}"
        log.error(f"Failed to retrieve token search results: {error_message}")
        return error_message

def oneinch_get_many_tokens(contract_addresses: str):
    """
    Retrieve information for multiple tokens on the Avalanche network using their contract addresses.

    This function fetches token data from the 1inch API for a comma-separated string of contract addresses
    on the Avalanche network (chain_id: 43114). It returns detailed information about each token,
    including its address, symbol, name, decimals, and logoURI.

    Args:
        contract_addresses (str): A comma-separated string of token contract addresses to fetch information for.

    Returns:
        dict: A dictionary containing token information, with contract addresses as keys.

    Raises:
        Exception: If there's an error in the API request or response processing.
    """
    addresses_list = [addr.strip() for addr in contract_addresses.split(',')]
    log.info(f"Starting 1inch get many tokens for {len(addresses_list)} addresses")
    url = "https://api.1inch.dev/token/v1.2/43114/custom"
    
    params = {
        "addresses": contract_addresses
    }
    log.debug(f"Request parameters: {params}")
    
    headers = {
        "Authorization": "Bearer GyI1FUwHQn9bAIpyg2Eugzq1NmXbY20G"
    }
    log.debug("Headers prepared")
    
    # Construct the full URL with query parameters
    full_url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    print(f"Full URL constructed: {full_url}")
    
    log.info("Sending request to 1inch API")
    response = fetch_data(full_url, headers)
    
    if response:
        log.success(f"Successfully retrieved data for tokens from 1inch API")
        print("Here is the response: ", response)
        return response
    else:
        error_message = f"Error: Unexpected response format or error in response"
        log.error(f"Failed to retrieve token data: {error_message}")
        return error_message