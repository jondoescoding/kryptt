# Langchain 
from langchain.pydantic_v1 import BaseModel, Field

class AIInput(BaseModel):
    message: str = Field(description="The text prompt for the AI to process.")
