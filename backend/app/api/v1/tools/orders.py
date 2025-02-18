from fastapi import HTTPException
from app.core.logging import logging
from app.core.config import get_trading_client
from alpaca.trading.enums import AssetClass
from alpaca.trading.models import Order
from ..settings import api_keys_store
from typing import List, Union
from uuid import UUID
from langchain_core.tools import tool