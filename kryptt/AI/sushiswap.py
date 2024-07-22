from ape import accounts, Contract, networks
from datetime import datetime
from tqdm import tqdm

MAX_ITERATIONS = 1000
ROUTER_ADDRESS = "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506" # Sushiswap Router v2 contract
NATIVE_TOKEN_ADDRESS = "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7"  # WAVAX on Avalanche

