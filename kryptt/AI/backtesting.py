import vectorbt as vbt
from typing import Optional
from datetime import datetime, timedelta

def backtest_with_trading_indicators(indicator: str, symbol: str, start_date: str, end_date: str):
    """
    Applies the specified trading indicator to the given OHLCV data and returns the indicator result and profit.

    Parameters:
    - indicator: str, the name of the indicator to use
    - symbol: str, the cryptocurrency symbol
    - start_date: str, the start date for the data
    - end_date: str, the end date for the data

    Returns:
    - tuple: (indicator_result, profit)
    """
    WINDOW = 14  # Default window size for indicators

    print(f"Fetching OHLCV data for {symbol} from {start_date} to {end_date}")
    ohlcv = get_ohlcv(symbol, start_date, end_date)
    close = ohlcv.get('Close')
    high = ohlcv.get('High')
    low = ohlcv.get('Low')
    volume = ohlcv.get('Volume')

    result = None
    entries = None
    exits = None

    print(f"Running {indicator} indicator")
    match indicator.upper():
        case 'STOCH':
            result = vbt.STOCH.run(high, low, close, k_window=WINDOW, d_window=3)
            entries = result.low_above(80)
            exits = result.low_below(20)
        case 'RSI':
            result = vbt.RSI.run(close, window=WINDOW)
            entries = result.rsi_above(70)
            exits = result.rsi_below(30)
        case 'OBV':
            result = vbt.OBV.run(close, volume)
            fast_obv = vbt.MA.run(result.obv, 10, short_name='fast')
            slow_obv = vbt.MA.run(result.obv, 20, short_name='slow')
            entries = fast_obv.ma_crossed_above(slow_obv)
            exits = fast_obv.ma_crossed_below(slow_obv)
        case 'MSTD':
            result = vbt.MSTD.run(close, window=WINDOW)
            entries = result.mstd_above(close)
            exits = result.mstd_below(close)
        case 'MACD':
            result = vbt.MACD.run(close, fast_window=12, slow_window=26, signal_window=9)
            entries = result.macd_above(result.signal)
            exits = result.macd_below(result.signal)
        case 'MA':
            fast_ma = vbt.MA.run(close, 10, short_name='fast')
            slow_ma = vbt.MA.run(close, 20, short_name='slow')
            result = (fast_ma, slow_ma)
            entries = fast_ma.ma_crossed_above(slow_ma)
            exits = fast_ma.ma_crossed_below(slow_ma)
        case 'ATR':
            result = vbt.ATR.run(high, low, close, window=WINDOW)
            entries = (result.atr > close * 0.02).to_numpy()  # Entry when ATR is above 2% of close price
            exits = (result.atr < close * 0.01).to_numpy()   # Exit when ATR is below 1% of close price
        case _:
            print(f"Unsupported indicator: {indicator}")
            raise ValueError(f"Unsupported indicator: {indicator}")
    
    profit = calculate_profit(close, entries, exits)
    
    #print(f"Indicator: {indicator}")
    #print(f"Profit: {profit}")

    return f"\nIndicator: {indicator}\nProfit: {profit}"

def calculate_profit(price, entries, exits):
    """
    Calculates the profit based on entry and exit signals.

    Parameters:
    - price: Series, the close price of the asset
    - entries: Series, entry signals
    - exits: Series, exit signals

    Returns:
    - float, the total return of the strategy
    """
    print("Calculating profit from entry and exit signals")
    pf = vbt.Portfolio.from_signals(price, entries, exits)
    total_return = pf.total_return()
    return(f"Total returns: {total_return}")
    #return total_return
def get_ohlcv(symbols: list[str] | str, start_date: str, end_date: str):
    """
    Download OHLCV (Open, High, Low, Close, Volume) data for the given symbols within the specified date range.

    Parameters:
    - symbols (list[str] | str): A list of symbols or a single symbol to download data for.
    - start_date (str): The start date for the data in YYYY-MM-DD format.
    - end_date (str): The end date for the data in YYYY-MM-DD format.

    Returns:
    - ohlcv_by_symbol: The downloaded OHLCV data.
    """
    print(f"Downloading OHLCV data for {symbols} from {start_date} to {end_date}")
    ohlcv_by_symbol = vbt.YFData.download(symbols, start=start_date, end=end_date)
    return ohlcv_by_symbol


def predict_profit_from_the_past(amount_invested: Optional[int], cryptocurrency: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """
    Predict the profit for a given cryptocurrency based on historical data.

    Parameters:
    - amount_invested (Optional[int]): The amount of cash invested. If None, a default of 100 will be used.
    - cryptocurrency (str): The cryptocurrency symbol (e.g., 'BTC' for Bitcoin).
    - start_date (Optional[str]): The start date for the data in YYYY-MM-DD format. If None, defaults to one year ago from today.
    - end_date (Optional[str]): The end date for the data in YYYY-MM-DD format. If None, defaults to today.

    Returns:
    - dict: A dictionary containing the total return, sharpe ratio, max drawdown, initial investment, cryptocurrency, start date, and end date.
    """
    print(f"Predicting profit for {cryptocurrency} with investment amount: {amount_invested}")
    
    # Set default date range if not provided
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')
    if not start_date:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    # Download price data
    price = vbt.YFData.download(f'{cryptocurrency.upper()}-USD', start=start_date, end=end_date).get('Close')
    
    if price.empty:
        return f"Error: No price data available for {cryptocurrency} in the specified date range."
    
    init_cash = amount_invested if amount_invested is not None else 100
    
    try:
        pf = vbt.Portfolio.from_holding(price, init_cash=init_cash)
    except ValueError as e:
        if "Attempt to go in long direction infinitely" in str(e):
            return f"Error: The initial investment of {init_cash} is too small for the current {cryptocurrency} price. Please try a larger amount."
        else:
            return e
    
    total_return = pf.total_return()
    sharpe_ratio = pf.sharpe_ratio()
    max_drawdown = pf.max_drawdown()
    
    return {
        "total_return": total_return,
        "sharpe_ratio": sharpe_ratio,
        "max_drawdown": max_drawdown,
        "initial_investment": init_cash,
        "cryptocurrency": cryptocurrency,
        "start_date": start_date,
        "end_date": end_date
    }