# Langchain 
from langchain.pydantic_v1 import BaseModel, Field, validator

class AIInput(BaseModel):
    message: str = Field(description="The text prompt for the AI to process.")

class coinGeckoFetchTokenInput(BaseModel):
    token: str = Field(description="From the coin gecko platform you able to identify a cryptocurrency by its name, id, or symbol. Symbols sometimes start with $, eg: $BTC or $ETH. The ids many times have a hypen in them, eg: curve-dao-token. The name of a cryptocurrency would be a simple string, eg: Curve, Bitcoin.")
    
class coinGeckoFetchOHLCInput(BaseModel):
    token_id: str = Field(description="From the coin gecko platform you able to identify a cryptocurrency by its name, id, or symbol. Symbols sometimes start with $, eg: $BTC or $ETH. The ids many times have a hypen in them, eg: curve-dao-token. The name of a cryptocurrency would be a simple string, eg: Curve, Bitcoin.")
    days: int = Field(description="The total days of how far back we can retrieve data from in days. The options ONLY can be: 1, 7, 14, 30, 90, 180, 365.")
    
    @validator('days')
    def check_date(cls, value):
        allowed_time_periods = [1, 7, 14, 30, 90, 180, 365]
        if value not in allowed_time_periods:
            raise ValueError('Date range can only be: 1, 7, 14, 30, 90, 180, 365!')
        return value
        