from ape import Contract, networks
from datetime import datetime, timedelta
from traderjoe_tools import impersonate_account, load_router_contract, load_token_contracts, execute_swap
import time

# Constants
TRADERJOE_ROUTER = "0x60aE616a2155Ee3d9A68541Ba4544862310933d4"
SUSHISWAP_ROUTER = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"  # SushiSwap router on Avalanche

def check_prices(router_contract, token_in, token_out, amount_in):
    try:
        # Get the expected output amount for a given input amount
        amounts_out = router_contract.getAmountsOut(amount_in, [token_in, token_out])
        return amounts_out[-1]
    except Exception as e:
        print(f"Error checking prices: {str(e)}")
        return 0

def arbitrage_opportunity(traderjoe_price, sushiswap_price, threshold=0.005):
    if traderjoe_price == 0 or sushiswap_price == 0:
        return False
    price_diff = abs(traderjoe_price - sushiswap_price) / min(traderjoe_price, sushiswap_price)
    return price_diff > threshold

def find_arbitrage_sushiswap_traderjoe(token1_address, token2_address):
    MAX_ITERATIONS = 2
    total_profit = 0

    try:
        print("Setting up Avalanche network...")
        with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:
            print("Impersonating account...")
            account = impersonate_account()
        
            print("Loading router contracts...")
            traderjoe_router = load_router_contract(router_address=TRADERJOE_ROUTER)
            sushiswap_router = load_router_contract(router_address=SUSHISWAP_ROUTER)
        
            print("Loading token contracts...")
            token1, token2 = load_token_contracts(token1_address, token2_address)
        
            amount_in = 10 * 10**token1['decimals']  # x amount of token1
            print(f"Setting input amount to {amount_in / 10**token1['decimals']} {token1['symbol']}")
        
            for iteration in range(MAX_ITERATIONS):
                print(f"\nIteration {iteration + 1}/{MAX_ITERATIONS}")
                print("Checking prices...")
                traderjoe_price = check_prices(traderjoe_router, token1['address'], token2['address'], amount_in)
                sushiswap_price = check_prices(sushiswap_router, token1['address'], token2['address'], amount_in)
                
                if traderjoe_price == 0 or sushiswap_price == 0:
                    print("Unable to fetch prices. There might not be a liquidity pool for these tokens on one or both exchanges.")
                    continue
                
                traderjoe_rate = traderjoe_price / 10**token2['decimals']
                sushiswap_rate = sushiswap_price / 10**token2['decimals']
                
                print(f"TraderJoe rate: 1 {token1['symbol']} = {traderjoe_rate:.6f} {token2['symbol']}")
                print(f"SushiSwap rate: 1 {token1['symbol']} = {sushiswap_rate:.6f} {token2['symbol']}")
                
                if arbitrage_opportunity(traderjoe_rate, sushiswap_rate):
                    print("Arbitrage opportunity found!")
                    if traderjoe_rate < sushiswap_rate:
                        print(f"Buying on TraderJoe and selling on SushiSwap")
                        buy_router = traderjoe_router
                        sell_router = sushiswap_router
                    else:
                        print(f"Buying on SushiSwap and selling on TraderJoe")
                        buy_router = sushiswap_router
                        sell_router = traderjoe_router
            
                    # Execute buy
                    print("Executing buy transaction...")
                    deadline = int((datetime.now() + timedelta(minutes=5)).timestamp())
                    min_amount_out = int(min(traderjoe_price, sushiswap_price) * 0.99)  # 1% slippage
                    buy_success = execute_swap(account, buy_router, token1, token2, amount_in, min_amount_out, deadline)
            
                    if buy_success:
                        print("Buy transaction successful")
                        # Execute sell
                        print("Executing sell transaction...")
                        sell_amount = Contract(address=token2["address"]).balanceOf(account.address)
                        min_amount_out = int(amount_in * 0.99)  # Ensure we get back at least 99% of our original token1
                        sell_success = execute_swap(account, sell_router, token2, token1, sell_amount, min_amount_out, deadline)
                
                        if sell_success:
                            print("Sell transaction successful")
                            print("Arbitrage completed successfully!")
                            profit = Contract(address=token1["address"]).balanceOf(account.address) - amount_in
                            total_profit += profit
                            print(f"Profit from this arbitrage: {profit / 10**token1['decimals']} {token1['symbol']}")
                            print(f"Total profit so far: {total_profit / 10**token1['decimals']} {token1['symbol']}")
                        else:
                            print("Failed to complete the sell part of the arbitrage")
                    else:
                        print("Failed to complete the buy part of the arbitrage")
                
                else:
                    print("No arbitrage opportunity found between these tokens on TraderJoe and SushiSwap.")
                
                if iteration < MAX_ITERATIONS - 1:
                    print("Waiting for 3 seconds before next iteration...")
                    time.sleep(3)
        
        return f"Final total profit: {total_profit / 10**token1['decimals']} {token1['symbol']}"
        
    except ZeroDivisionError:
        return "Error: Unable to calculate price difference. One of the exchanges might not have a liquidity pool for these tokens."
    except Exception as e:
        return f"An error occurred: {str(e)}"