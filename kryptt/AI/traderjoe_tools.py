from ape import accounts, Contract, networks
from datetime import datetime
from tqdm import tqdm

MAX_ITERATIONS = 1000
ROUTER_ADDRESS = "0x60aE616a2155Ee3d9A68541Ba4544862310933d4" # Traderjoe V1 Router contract
NATIVE_TOKEN_ADDRESS = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"  # WAVAX on Avalanche

def setup_avalanche():
    """
    Connect to the Avalanche network.

    Returns:
        provider: The network provider for the Avalanche mainnet.
    
    Raises:
        Exception: If the connection to the Avalanche network fails.
    """
    try:
        # Connect to the Avalanche network
        with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:
            print("Connected to Avalanche mainnet")
            return provider
    except Exception as e:
        raise Exception(f"Failed to connect to Avalanche network: {str(e)}")

def impersonate_account():
    """
    Impersonate a specific account.

    Returns:
        hot_wallet: The impersonated account object.
    
    Raises:
        Exception: If impersonation of the account fails.
    """
    try:
        hot_wallet = accounts['0xf89d7b9c864f589bbF53a82105107622B35EaA40']
        print(f"Impersonated account: {hot_wallet.address}")
        return hot_wallet
    except Exception as e:
        return Exception(f"Failed to impersonate account: {str(e)}")

def load_router_contract(router_address: str):
    """
    Load the router contract.

    Args:
        router_address (str): The address of the router contract.

    Returns:
        router_contract: The loaded router contract object.
    
    Raises:
        Exception: If loading the router contract fails.
    """
    try:
        router_contract = Contract(address=router_address)
        print(f"Loaded router contract at address: {router_contract.address}")
        return router_contract
    except Exception as e:
        raise Exception(f"Failed to load router contract: {str(e)}")

def load_token_contracts(token1_address, token2_address):
    """
    Load the token contracts.

    Args:
        token1_address (str): The address of the first token contract.
        token2_address (str): The address of the second token contract.

    Returns:
        tuple: A tuple containing dictionaries with details of the two token contracts.
    
    Raises:
        Exception: If loading the token contracts fails.
    """
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
    """
    Approve the router to spend the specified amount of tokens.

    Args:
        account: The account object.
        token: The token contract object.
        router_address (str): The address of the router contract.
        amount (int): The amount of tokens to approve.

    Returns:
        str: A message indicating the result of the approval process.
    """
    try:
        # Check if there's enough gas (native token)
        if account.balance < 1e16:  # 0.01 AVAX
            return ("Not enough gas to perform the transaction")

        token_ = Contract(token["address"])

        # Check if there's enough of token1 to be traded
        token_balance = token_.balanceOf(account.address)
        if token_balance < amount:
            return (f"Not enough {token_.symbol()} to trade. Balance: {token_balance}, Required: {amount}")

        # Approve the router to spend the maximum amount of tokens
        max_amount = 2**256 - 1
        tx = token_.approve(router_address, max_amount, sender=account)
        return (f"Approved {token_.symbol()} for trading. Transaction hash: {tx.txn_hash}")
    except Exception as e:
        return (f"Error in approve_tokens: {str(e)}")

def execute_swap(account, router_contract, token_in, token_out, amount_in, min_amount_out, deadline):
    """
    Execute a token swap.

    Args:
        account: The account object.
        router_contract: The router contract object.
        token_in: The input token contract object.
        token_out: The output token contract object.
        amount_in (int): The amount of input tokens.
        min_amount_out (int): The minimum amount of output tokens.
        deadline (int): The deadline for the swap.

    Returns:
        str: A message indicating the result of the swap execution.
    """
    try:
        # Approve the router to spend token_in
        if not approve_tokens(account, token_in, router_contract.address, amount_in):
            return False

        # Execute the swap
        tx = router_contract.swapExactTokensForTokens(
            amount_in,
            min_amount_out,
            [token_in["address"], NATIVE_TOKEN_ADDRESS, token_out["address"]],
            account.address,
            deadline,
            sender=account
        )
        return f"Swap executed. Transaction hash: {tx.txn_hash}"
    except Exception as e:
        return f"Error occured in execute_swap: {str(e)}"

def find_arbitrage(account, router_contract, token0_address, token1_address):
    """
    Find arbitrage opportunities.

    Args:
        account: The account object.
        router_contract: The router contract object.
        token0_address (str): The address of the first token contract.
        token1_address (str): The address of the second token contract.

    Returns:
        str: A message indicating the result of the arbitrage search.
    """
    native_token = Contract(NATIVE_TOKEN_ADDRESS)
    token0, token1 = load_token_contracts(token1_address=token0_address, token2_address=token1_address)
    
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
                swap_result = execute_swap(account, router_contract, token0, token1, amount_in, min_amount_out, deadline)
                
                if swap_result:
                    print("Swap executed successfully")
                else:
                    print("Swap failed")
                
                return f"Successful swap. Here are the results: {swap_result}"
        
        except Exception as e:
            return (f"\nError occurred in finding arbitrage (find_arbitrage): {str(e)}")
    
    return ("\nNo arbitrage opportunities found after MAX_ITERATIONS")

def find_arbitrage_traderjoe(token1_address: str, token2_address: str):
    """
    Find arbitrage opportunities within TraderJoe for two given tokens on the Avalanche network.

    Args:
        token1_address (str): The contract address of the first token.
        token2_address (str): The contract address of the second token.

    Returns:
        str: A message indicating the results of the arbitrage search.
    """
    with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:
        # Impersonate an account
        account = impersonate_account()

        # Load Sushiswap router contract
        router_contract = load_router_contract(router_address=ROUTER_ADDRESS)

        # Load token contracts
        token0, token1 = load_token_contracts(token1_address, token2_address)

        # Find and execute arbitrage
        arbitrage_found = find_arbitrage(account, router_contract, token0['address'], token1['address'])

        if arbitrage_found:
            return ("Results from the arbitrage search: ", arbitrage_found)