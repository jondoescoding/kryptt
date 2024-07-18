from ape import accounts, Contract, networks
from datetime import datetime
from tqdm import tqdm

MAX_ITERATIONS = 1000
ROUTER_ADDRESS = "0x60aE616a2155Ee3d9A68541Ba4544862310933d4" # Traderjoe V1 Router contract
NATIVE_TOKEN_ADDRESS = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"  # WAVAX on Avalanche

def setup_avalanche():
    try:
        # Connect to the Avalanche network
        #networks.default = "avalanche"
        with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:
            print("Connected to Avalanche mainnet")
    except Exception as e:
        raise Exception(f"Failed to connect to Avalanche network: {str(e)}")

def impersonate_account():
    try:
        hot_wallet = accounts['0xf89d7b9c864f589bbF53a82105107622B35EaA40']
        print(f"Impersonated account: {hot_wallet.address}")
        return hot_wallet
    except Exception as e:
        raise Exception(f"Failed to impersonate account: {str(e)}")

def load_router_contract():
    try:
        router_contract = Contract(address="0x60aE616a2155Ee3d9A68541Ba4544862310933d4")
        print(f"Loaded router contract at address: {router_contract.address}")
        return router_contract
    except Exception as e:
        raise Exception(f"Failed to load router contract: {str(e)}")

def load_token_contracts(token1_address, token2_address):
    try:
        token1_contract = Contract(token1_address)
        token2_contract = Contract(token2_address)
        
        token1 = {
            "address": token1_contract.address,
            "symbol": token1_contract.symbol(),
            "decimals": token1_contract.decimals(),
        }
        
        token2 = {
            "address": token2_contract.address,
            "symbol": token2_contract.symbol(),
            "decimals": token2_contract.decimals(),
        }
        
        print(f"Loaded token1: {token1}")
        print(f"Loaded token2: {token2}")
        
        return token1, token2
    except Exception as e:
        raise Exception(f"Failed to load token contracts: {str(e)}")

def approve_tokens(account, token, router_address, amount):
    try:
        # Check if there's enough gas (native token)
        if account.balance < 1e16:  # 0.01 AVAX
            print("Not enough gas to perform the transaction")
            return False

        # Check if there's enough of token1 to be traded
        token_balance = token.balanceOf(account)
        if token_balance < amount:
            print(f"Not enough {token.symbol()} to trade. Balance: {token_balance}, Required: {amount}")
            return False

        # Approve the router to spend the maximum amount of tokens
        max_amount = 2**256 - 1
        tx = token.approve(router_address, max_amount, sender=account)
        print(f"Approved {token.symbol()} for trading. Transaction hash: {tx.txn_hash}")
        return True
    except Exception as e:
        print(f"Error in approve_tokens: {str(e)}")
        return False

def execute_swap(account, router_contract, token_in, token_out, amount_in, min_amount_out, deadline):
    try:
        # Approve the router to spend token_in
        if not approve_tokens(account, token_in, router_contract.address, amount_in):
            return False

        # Execute the swap
        tx = router_contract.swapExactTokensForTokens(
            amount_in,
            min_amount_out,
            [token_in.address, token_out.address],
            account.address,
            deadline,
            sender=account
        )
        print(f"Swap executed. Transaction hash: {tx.txn_hash}")
        return True
    except Exception as e:
        print(f"Error in execute_swap: {str(e)}")
        return False

def find_arbitrage(flash_loan_contract, router_contract, token0: dict, token1: dict):
    native_token = Contract(NATIVE_TOKEN_ADDRESS)
    
    for _ in tqdm(range(MAX_ITERATIONS), desc="Searching for arbitrage"):
        try:
            qty_out = router_contract.getAmountsOut(
                10**token0['decimals'],
                [token0['address'], native_token.address, token1['address']]
            )[-1] / 10**token1['decimals']
            
            if 1.01 <= qty_out < 2.00:
                print(f"\nArbitrage opportunity found!")
                print(f"{datetime.now().strftime('[%I:%M:%S %p]')} {token0['symbol']} -> {token1['symbol']}: ({qty_out:.3f})")
                
                # Execute the swap
                amount_in = 10**token0['decimals']
                min_amount_out = int(qty_out * 0.99 * 10**token1['decimals'])  # 1% slippage
                deadline = int(datetime.now().timestamp()) + 300  # 5 minutes from now
                
                print(f"Executing swap with parameters: amount_in={amount_in}, min_amount_out={min_amount_out}, path=[{token0['symbol']}, {native_token.symbol()}, {token1['symbol']}], deadline={deadline}")
                
                # Call executeArbitrage on the flash loan contract
                flash_loan_contract.executeArbitrage(
                    router_contract.address,
                    token0['address'],
                    token1['address'],
                    amount_in,
                    min_amount_out,
                    deadline,
                    sender=flash_loan_contract.owner()
                )
                
                # Execute the swap through the flash loan contract
                swap_result = execute_swap(flash_loan_contract, router_contract, token0, token1, amount_in, min_amount_out, deadline)
                
                if swap_result:
                    print("Swap executed successfully")
                else:
                    print("Swap failed")
                
                return True
        
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
            return False
    
    print("\nNo arbitrage opportunities found after MAX_ITERATIONS")
    return False

# Example usage
#if __name__ == "__main__":
#    with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:
#    #with networks.avalanche.mainnet_fork.use_provider("foundry"):
#        account = impersonate_account()
#        router_contract = load_router_contract()
#        token0, token1 = load_token_contracts("0xc7198437980c041c805A1EDcbA50c1Ce5db95118", "0xd586E7F844cEa2F87f50152665BCbc2C279D8d70")
    
#        find_arbitrage(account, router_contract, token0, token1)