from ape import networks

# Import functions from traderjoe_tools.py
from traderjoe_tools import (
    impersonate_account,
    load_router_contract,
    load_token_contracts,
    find_arbitrage
)

# Sushiswap-specific constants
SUSHISWAP_ROUTER_ADDRESS = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506"  # Sushiswap Router v2 contract
WAVAX_ADDRESS = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"  # WAVAX on Avalanche

def find_arbitrage_sushiswap(token1_address: str, token2_address: str):
    with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:

        # Impersonate an account
        account = impersonate_account()

        # Load Sushiswap router contract
        router_contract = load_router_contract(router_address=SUSHISWAP_ROUTER_ADDRESS)

        # Load token contracts
        token0, token1 = load_token_contracts(token1_address, token2_address)

        # Find and execute arbitrage
        arbitrage_found = find_arbitrage(account, router_contract, token0['address'], token1['address'])
        
        if arbitrage_found:
            return ("Results from the arbitrage search: ", arbitrage_found)