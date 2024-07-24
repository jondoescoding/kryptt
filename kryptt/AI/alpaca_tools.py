# Python Imports
from typing import Optional

# Alpaca Imports
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Local Imports
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, log

# Configure loguru log
log.add('alpaca_tools.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")

TRADING_CLIENT = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

# ACCOUNT
def get_accounts_details_alpaca():
    """
    Fetches account details from Alpaca.

    This function retrieves the account details from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the account details if the request is successful.
        None: If an error occurs during the request.
    """
    log.info("Fetching account details from Alpaca")
    try:
        account = TRADING_CLIENT.get_account()
        log.info(f"Account details: {account}")
        return f"Here are your account details: {account}"
    except Exception as e:
        log.error(f"Error fetching account details: {e}")
        return None

# ORDERS
def get_all_order_alpaca():
    """
    Fetches all orders from Alpaca.

    This function retrieves all orders from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with all orders if the request is successful.
        None: If an error occurs during the request.
    """
    log.info("Fetching all orders from Alpaca")
    try:
        orders = TRADING_CLIENT.get_orders()
        log.info(f"All orders: {orders}")
        return f"Here are all your orders: {orders}"
    except Exception as e:
        log.error(f"Error fetching all orders: {e}")
        return None

def get_order_by_id_alpaca(order_id: str):
    """
    Fetches an order by ID from Alpaca.

    Args:
        order_id (str): The ID of the order to fetch.

    Returns:
        str: A message with the order details if the request is successful.
        None: If an error occurs during the request.
    """
    log.info(f"Fetching order by ID from Alpaca: {order_id}")
    try:
        order = TRADING_CLIENT.get_order_by_id(order_id)
        log.info(f"Order details: {order}")
        return f"Here are the details for order {order_id}: {order}"
    except Exception as e:
        log.error(f"Error fetching order by ID: {e}")
        return None

def cancel_all_order_alpaca():
    """
    Cancels all orders on Alpaca.

    This function cancels all orders on the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the cancel responses if the request is successful.
        None: If an error occurs during the request.
    """
    log.info("Cancelling all orders on Alpaca")
    try:
        cancel_responses = TRADING_CLIENT.cancel_orders()
        log.info(f"Cancel responses: {cancel_responses}")
        return f"All orders have been cancelled: {cancel_responses}"
    except Exception as e:
        log.error(f"Error cancelling all orders: {e}")
        return None

def cancel_order_by_id_alpaca(order_id: str):
    """
    Cancels an order by ID on Alpaca.

    Args:
        order_id (str): The ID of the order to cancel.

    Returns:
        str: A message with the cancel response if the request is successful.
        None: If an error occurs during the request.
    """
    log.info(f"Cancelling order by ID on Alpaca: {order_id}")
    try:
        cancel_response = TRADING_CLIENT.cancel_order_by_id(order_id)
        log.info(f"Cancel response: {cancel_response}")
        return f"Order {order_id} has been cancelled: {cancel_response}"
    except Exception as e:
        log.error(f"Error cancelling order by ID: {e}")
        return None

def get_open_orders_alpaca():
    """
    Fetches open orders from Alpaca.

    This function retrieves all open orders from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the open orders if the request is successful.
        None: If an error occurs during the request.
    """
    log.info("Fetching open orders from Alpaca")
    try:
        open_orders = TRADING_CLIENT.get_orders(status='open')
        log.info(f"Open orders: {open_orders}")
        return f"Here are your open orders: {open_orders}"
    except Exception as e:
        log.error(f"Error fetching open orders: {e}")
        return None

def post_order_alpaca(symbol: str, qty: int, order_side: str, time_in_force: str):
    """
    Posts an order to Alpaca.

    Args:
        symbol (str): The symbol of the stock or asset to trade.
        qty (int): The quantity of the asset to buy or sell.
        order_side (str): The side of the trade (BUY or SELL).
        time_in_force (str): The duration for which the order is valid.

    Returns:
        str: A message with the order details if the request is successful.
        None: If an error occurs during the request.
    """
    log.info("Posting order to Alpaca")
    try:
        account = TRADING_CLIENT.get_account()
        log.info(f"Account details: {account}")

        # Creating a MarketOrderRequest object to prepare the order details
        order_data = MarketOrderRequest(
            symbol=symbol,  # The symbol of the stock or asset to trade
            qty=qty,  # The quantity of the asset to buy or sell
            side=OrderSide(order_side),  # The side of the trade (BUY or SELL)
            time_in_force=TimeInForce(time_in_force)  # The duration for which the order is valid
        )

        order = TRADING_CLIENT.submit_order(order_data=order_data)
        log.info(f"Order submitted: {order}")
        return f"Order has been submitted: {order}"
    except Exception as e:
        log.error(f"Error posting order: {e}")
        return None

# POSITIONS
def get_positions_alpaca():
    """
    Fetches positions from Alpaca.

    This function retrieves all positions from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the positions if the request is successful.
        None: If an error occurs during the request.
    """
    log.info("Fetching positions from Alpaca")
    try:
        account_id = TRADING_CLIENT.get_account().id
        positions = TRADING_CLIENT.get_all_positions_for_account(account_id=account_id)
        log.info(f"Positions: {positions}")
        return f"Here are your positions: {positions}"
    except Exception as e:
        log.error(f"Error fetching positions: {e}")
        return None

def close_all_positions(cancel_orders: bool = False):
    """
    Closes all positions on Alpaca.

    Args:
        cancel_orders (bool): If true, cancel all open orders before liquidating all positions.

    Returns:
        str: A message with the close responses if the request is successful.
        None: If an error occurs during the request.
    """
    log.info("Closing all positions on Alpaca")
    try:
        close_responses = TRADING_CLIENT.close_all_positions(cancel_orders=cancel_orders)
        log.info(f"Close responses: {close_responses}")
        return f"All positions have been closed: {close_responses}"
    except Exception as e:
        log.error(f"Error closing all positions: {e}")
        return None

def close_a_position(symbol_or_asset_id: str, close_options: Optional[dict] = None):
    """
    Closes a position for a specific asset on Alpaca.

    Args:
        symbol_or_asset_id (str): The symbol name or asset ID of the position to close.
        close_options (Optional[dict]): The various close position request parameters.

    Returns:
        str: A message with the close response if the request is successful.
        None: If an error occurs during the request.
    """
    log.info(f"Closing position for asset: {symbol_or_asset_id}")
    try:
        close_response = TRADING_CLIENT.close_position(symbol_or_asset_id, close_options=close_options)
        log.info(f"Close response: {close_response}")
        return f"Position for asset {symbol_or_asset_id} has been closed: {close_response}"
    except Exception as e:
        log.error(f"Error closing position for asset {symbol_or_asset_id}: {e}")
        return None