# Local
from config import log

# Python
from datetime import datetime

# HTTP
import requests

def convert_coin_price(usd_coin_price: str, currency_to_convert_to: str):
    """
    Converts the given USD coin price to the specified currency using a conversion API.
    """
    log.info(f"Starting conversion: {usd_coin_price} USD to {currency_to_convert_to}")

    # Get today's date in the format YYYY-MM-DD
    today_date = datetime.today().strftime('%Y-%m-%d')
    log.debug(f"Today's date: {today_date}")
    
    # Construct the URL for the API request
    url = f"https://api.fxratesapi.com/convert?from=USD&to={currency_to_convert_to}&date={today_date}&amount={usd_coin_price}&format=json"
    log.debug(f"Constructed URL: {url}")
    
    try:
        # Send a GET request to the conversion API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        log.debug(f"API response data: {data}")

        # Extract the converted amount from the response
        converted_amount = data.get('result')

        if converted_amount is not None:
            log.info(f"Conversion successful: {usd_coin_price} USD = {converted_amount} {currency_to_convert_to}")
            return converted_amount
        else:
            log.error(f"Conversion result not found for the provided data: {usd_coin_price} to {currency_to_convert_to}")
            return f"Conversion result not found for the provided data: {usd_coin_price} to {currency_to_convert_to}"
    except requests.RequestException as e:
        log.error(f"Request failed: {e}")
        return f"Request failed: {e}"