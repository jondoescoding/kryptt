from ape import Contract, networks
from datetime import datetime, timedelta
from traderjoe_tools import impersonate_account, load_router_contract, load_token_contracts, execute_swap
import time

# Constants
TRADERJOE_ROUTER = "0x60aE616a2155Ee3d9A68541Ba4544862310933d4"
SUSHISWAP_ROUTER = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"  # SushiSwap router on Avalanche
USDC = "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E"
USDT = "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7"

def check_prices(router_contract, token_in, token_out, amount_in):
    try:
        # Get the expected output amount for a given input amount
        amounts_out = router_contract.getAmountsOut(amount_in, [token_in, token_out])
        return amounts_out[-1]
    except Exception as e:
        print(f"Error checking prices: {str(e)}")
        return 0

def arbitrage_opportunity(traderjoe_price, sushiswap_price, threshold=0.005):
    # Check if the price difference exceeds the threshold
    price_diff = abs(traderjoe_price - sushiswap_price) / min(traderjoe_price, sushiswap_price)
    return price_diff > threshold

def main():
    print("Setting up Avalanche network...")
    with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:
    
        print("Impersonating account...")
        account = impersonate_account()
    
        print("Loading router contracts...")
        traderjoe_router = load_router_contract(router_address="0x60aE616a2155Ee3d9A68541Ba4544862310933d4")
        sushiswap_router = load_router_contract(router_address=SUSHISWAP_ROUTER)
    
        print("Loading token contracts...")
        usdc, usdt = load_token_contracts(USDC, USDT)
    
        amount_in = 10 * 10**usdc['decimals']  # x amount of USDC
        print(f"Setting input amount to {amount_in / 10**usdc['decimals']} USDC")
    
        while True:
            print("\nChecking prices...")
            traderjoe_price = check_prices(traderjoe_router, usdc['address'], usdt['address'], amount_in)
            sushiswap_price = check_prices(sushiswap_router, usdc['address'], usdt['address'], amount_in)
        
            traderjoe_rate = traderjoe_price / 10**usdt['decimals']
            sushiswap_rate = sushiswap_price / 10**usdt['decimals']
        
            print(f"TraderJoe rate: 1 USDC = {traderjoe_rate:.6f} USDT")
            print(f"SushiSwap rate: 1 USDC = {sushiswap_rate:.6f} USDT")
        
            if arbitrage_opportunity(traderjoe_rate, sushiswap_rate):
                print("Arbitrage opportunity found!")
                if traderjoe_rate < sushiswap_rate:
                    print("Buying on TraderJoe and selling on SushiSwap")
                    buy_router = traderjoe_router
                    sell_router = sushiswap_router
                else:
                    print("Buying on SushiSwap and selling on TraderJoe")
                    buy_router = sushiswap_router
                    sell_router = traderjoe_router
            
            # Execute buy
                print("Executing buy transaction...")
                deadline = int((datetime.now() + timedelta(minutes=5)).timestamp())
                min_amount_out = int(min(traderjoe_price, sushiswap_price) * 0.99)  # 1% slippage
                buy_success = execute_swap(account, buy_router, usdc, usdt, amount_in, min_amount_out, deadline)
            
                if buy_success:
                    print("Buy transaction successful")
                    # Execute sell
                    print("Executing sell transaction...")
                    #sell_amount = usdt['address'].balanceOf(account)
                    sell_amount = Contract(address=usdt["address"]).balanceOf(account.address)
                    min_amount_out = int(amount_in * 0.99)  # Ensure we get back at least 99% of our original USDC
                    sell_success = execute_swap(account, sell_router, usdt, usdc, sell_amount, min_amount_out, deadline)
                
                    if sell_success:
                        print("Sell transaction successful")
                        print("Arbitrage completed successfully!")
                    else:
                        print("Failed to complete the sell part of the arbitrage")
                else:
                    print("Failed to complete the buy part of the arbitrage")
        
            else:
                print("No arbitrage opportunity at the moment")
        
            # Wait for a short period before checking again
            print("Waiting for 60 seconds before next check...")
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
