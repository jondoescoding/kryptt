from ape import Contract, accounts, networks, project
from traderjoe_tools import find_arbitrage, load_router_contract, load_token_contracts, impersonate_account

AAVE_LENDING_POOL_ADDRESS = "0x794a61358D6845594F94dc1DB02A252b5b4814aD"  # Avalanche Mainnet
FLASH_LOAN_AMOUNT = 10_000  # 10,000 tokens with 18 decimals

def execute_flash_loan_arbitrage(token0_address: str, token1_address: str):
    try:
        with networks.parse_network_choice("avalanche:mainnet-fork:foundry") as provider:
            account = impersonate_account()
            print("Account Loaded...")
            lending_pool = Contract(AAVE_LENDING_POOL_ADDRESS)
            print("Lending Pool Contract loaded...")
            router_contract = load_router_contract()
            print("Router contract loaded...")
            token0, token1 = load_token_contracts(token0_address, token1_address)
            print("Tokens Loaded")
            
            # Deploy the FlashLoanArbitrage contract
            flash_loan_arbitrage = account.deploy(project.FlashLoanArbitrage, AAVE_LENDING_POOL_ADDRESS)
            print("FlashLoanArbitrage contract deployed")
            
            # Execute the flash loan
            tx = flash_loan_arbitrage.requestFlashLoan(
                token0['address'],
                FLASH_LOAN_AMOUNT,
                sender=account
            )

            # Check if arbitrage was successful
            print("Searching for arbitrage...")
            arbitrage_result = find_arbitrage(flash_loan_arbitrage, router_contract, token0, token1)

            if arbitrage_result:
                # Withdraw profits from the contract
                withdraw_tx = flash_loan_arbitrage.withdraw(token0['address'], sender=account)
                profit = account.balance() - account.balance_before(withdraw_tx)
                return f"Flash loan arbitrage executed successfully. Profit: {profit / 10**18} AVAX"
            else:
                return "No profitable arbitrage opportunity found"

    except Exception as e:
        return f"Error executing flash loan arbitrage: {str(e)}"