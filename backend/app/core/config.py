"""
Application Configuration Settings

This module manages all configuration settings for the Kryptt API.
It uses Pydantic's BaseSettings for automatic environment variable loading
and validation, with Infisical integration for secure secret management.

Configuration Categories:
- API settings (title, version, description)
- Database settings
- Security settings
- External service configurations

Environment Variables:
- INFISICAL_TOKEN: Infisical authentication token
- INFISICAL_HOST: Infisical host URL
- PROJECT_ID: Infisical project ID
- ENVIRONMENT: Current environment (development/staging/production)

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with environment variable support and Infisical integration."""
    
    # API Settings
    API_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Kryptt API"
    DEBUG: bool = False
    

    
    class Config:
        """Pydantic config for environment variable loading."""
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Create cached instance of settings."""
    return Settings()
