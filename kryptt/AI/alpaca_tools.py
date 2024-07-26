# Python Imports
from typing import Optional

# Alpaca Imports
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType, AssetClass, QueryOrderStatus
from alpaca.trading.requests import GetOrdersRequest, GetAssetsRequest, MarketOrderRequest, LimitOrderRequest, StopOrderRequest, StopLimitOrderRequest


# Local Imports
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY

TRADING_CLIENT = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)

# ACCOUNT
def get_accounts_details_alpaca():
    """
    Fetches account details from Alpaca.

    This function retrieves the account details from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the account details if the request is successful.
    """
    print("Fetching account details from Alpaca")
    try:
        account = TRADING_CLIENT.get_account()
        print(f"Account details: {account}")
        return f"Here are your account details: {account}"
    except Exception as e:
        return f"Error fetching account details: {e}"

# ORDERS
def get_all_order_alpaca():
    """
    Fetches all orders from Alpaca.

    This function retrieves all orders from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with all orders if the request is successful.
    """
    print("Fetching all orders from Alpaca")
    try:
        orders = TRADING_CLIENT.get_orders()
        print(f"All orders: {orders}")
        return f"Here are all your orders: {orders}"
    except Exception as e:
        return f"Error fetching all orders: {e}"

def get_order_by_id_alpaca(order_id: str):
    """
    Fetches an order by ID from Alpaca.

    Args:
        order_id (str): The ID of the order to fetch.

    Returns:
        str: A message with the order details if the request is successful.
    """
    print(f"Fetching order by ID from Alpaca: {order_id}")
    try:
        order = TRADING_CLIENT.get_order_by_id(order_id)
        print(f"Order details: {order}")
        return f"Here are the details for order {order_id}: {order}"
    except Exception as e:
        return f"Error fetching order by ID: {e}"

def cancel_all_order_alpaca():
    """
    Cancels all orders on Alpaca.

    This function cancels all orders on the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the cancel responses if the request is successful.
    """
    print("Cancelling all orders on Alpaca")
    try:
        cancel_responses = TRADING_CLIENT.cancel_orders()
        print(f"Cancel responses: {cancel_responses}")
        return f"All orders have been cancelled: {cancel_responses}"
    except Exception as e:
        return f"Error cancelling all orders: {e}"

def cancel_order_by_id_alpaca(order_id: str):
    """
    Cancels an order by ID on Alpaca.

    Args:
        order_id (str): The ID of the order to cancel.

    Returns:
        str: A message with the cancel response if the request is successful.
    """
    print(f"Cancelling order by ID on Alpaca: {order_id}")
    try:
        cancel_response = TRADING_CLIENT.cancel_order_by_id(order_id)
        print(f"Cancel response: {cancel_response}")
        return f"Order {order_id} has been cancelled: {cancel_response}"
    except Exception as e:
        return f"Error cancelling order by ID: {e}"

def get_open_orders_alpaca():
    """
    Fetches open orders from Alpaca.

    This function retrieves all open orders from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the open orders if the request is successful.
    """
    print("Fetching open orders from Alpaca")
    try:
        # Create a GetOrdersRequest object for open orders
        request_params = GetOrdersRequest(
            status=QueryOrderStatus.OPEN,
            limit=100,  # You can adjust this limit as needed
            nested=True  # Include nested multi-leg orders
        )
        
        # Fetch the open orders using the request parameters
        open_orders = TRADING_CLIENT.get_orders(filter=request_params)
        
        print(f"Open orders: {open_orders}")
        return f"Here are your open orders: {open_orders}"
    except Exception as e:
        return f"Error fetching open orders: {e}"

def post_order_alpaca(symbol: str, qty: float, side: str, order_type: str, limit_price: float = None, stop_price: float = None):
    """
    Posts an order to Alpaca.

    Args:
        symbol (str): The symbol of the asset to trade (e.g., "BTC", "ETH").
        qty (float): The quantity of the asset to buy or sell.
        side (str): The side of the trade (buy or sell).
        order_type (str): The type of the order (market, limit, stop, stop_limit).
        limit_price (float, optional): The limit price for limit and stop-limit orders.
        stop_price (float, optional): The stop price for stop and stop-limit orders.

    Returns:
        str: A message with the order details if the request is successful.
    """
    print(f"Posting order to Alpaca for {symbol}")
    try:
        # Ensure symbol is in the correct format
        #formatted_symbol = f"{symbol.upper()}/USD" if '/' not in symbol else symbol.upper()
        
        # Determine the order side
        order_side = OrderSide.BUY if side.lower() == 'buy' else OrderSide.SELL
        
        # Prepare the order data based on the order type
        if order_type.lower() == 'market':
            order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.GTC
            )
        elif order_type.lower() == 'limit':
            order_data = LimitOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.GTC,
                limit_price=limit_price
            )
        elif order_type.lower() == 'stop':
            order_data = StopOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.GTC,
                stop_price=stop_price
            )
        elif order_type.lower() == 'stop_limit':
            order_data = StopLimitOrderRequest(
                symbol=symbol,
                qty=qty,
                side=order_side,
                time_in_force=TimeInForce.GTC,
                limit_price=limit_price,
                stop_price=stop_price
            )
        else:
            raise ValueError(f"Invalid order type: {order_type}")

        # Submit the order
        submitted_order = TRADING_CLIENT.submit_order(order_data=order_data)
        print(f"Order submitted: {submitted_order}")
        return f"Here is a breakdown of the order has been submitted: \n{submitted_order}"
    except Exception as e:
        return f"Error posting order: {e}"

# POSITIONS
def get_positions_alpaca():
    """
    Fetches positions from Alpaca.

    This function retrieves all positions from the Alpaca trading platform using the configured trading client.

    Returns:
        str: A message with the positions if the request is successful.
    """
    print("Fetching positions from Alpaca")
    try:
        positions = TRADING_CLIENT.get_all_positions()
        print(f"Positions: {positions}")
        return f"Here are your positions: {positions}"
    except Exception as e:
        return f"Error fetching positions: {e}"

def close_all_positions(cancel_orders: bool = False):
    """
    Closes all positions on Alpaca.

    Args:
        cancel_orders (bool): If true, cancel all open orders before liquidating all positions.

    Returns:
        str: A message with the close responses if the request is successful.
    """
    print("Closing all positions on Alpaca")
    try:
        close_responses = TRADING_CLIENT.close_all_positions(cancel_orders=cancel_orders)
        print(f"Close responses: {close_responses}")
        return f"All positions have been closed: {close_responses}"
    except Exception as e:
        return f"Error closing all positions: {e}"

def close_a_position(symbol_or_asset_id: str, close_options: Optional[dict] = None):
    """
    Closes a position for a specific asset on Alpaca.

    Args:
        symbol_or_asset_id (str): The symbol name or asset ID of the position to close.
        close_options (Optional[dict]): The various close position request parameters.

    Returns:
        str: A message with the close response if the request is successful.
    """
    print(f"Closing position for asset: {symbol_or_asset_id}")
    try:
        close_response = TRADING_CLIENT.close_position(symbol_or_asset_id, close_options=close_options)
        print(f"Close response: {close_response}")
        return f"Position for asset {symbol_or_asset_id} has been closed: {close_response}"
    except Exception as e:
        return f"Error closing position for asset {symbol_or_asset_id}: {e}"

def get_all_assets_alpaca(asset_class: Optional[AssetClass] = None):
    """
    Fetches a list of assets from Alpaca.

    Args:
        asset_class (Optional[AssetClass]): The asset class to filter by. If None, all assets are returned.

    Returns:
        str: A message with the list of assets if the request is successful.
    """
    print("Fetching list of assets from Alpaca")
    try:
        search_params = GetAssetsRequest(asset_class=asset_class) if asset_class else None
        assets = TRADING_CLIENT.get_all_assets(search_params)
        print(f"Assets: {assets}")
        return f"Here is the list of assets: {assets}"
    except Exception as e:
        return f"Error fetching list of assets: {e}"

def is_asset_tradable_alpaca(symbol: str):
    """
    Checks if a particular asset is tradable on Alpaca.

    Args:
        symbol (str): The symbol of the asset to check.

    Returns:
        str: A message indicating whether the asset is tradable or not.
    """
    print(f"Checking if {symbol} is tradable on Alpaca")
    try:
        asset = TRADING_CLIENT.get_asset(symbol)
        if asset.tradable:
            return f"{symbol} is tradable on Alpaca."
        else:
            return f"{symbol} is not tradable on Alpaca."
    except Exception as e:
        return f"Error checking if {symbol} is tradable: {e}"