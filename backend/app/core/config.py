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
from infisical_sdk import InfisicalSDKClient

class InfisicalConfig:
    """Infisical configuration and client setup."""
    
    def __init__(self):
        self.token = os.getenv("INFISICAL_TOKEN")
        self.host = os.getenv("INFISICAL_HOST", "https://app.infisical.com")
        self.project_id = os.getenv("PROJECT_ID")
        self.environment = os.getenv("ENVIRONMENT", "development")
        
        if not all([self.token, self.project_id]):
            raise ValueError("Missing required Infisical configuration")
        
        self.client = InfisicalSDKClient(
            host=self.host,
            token=self.token
        )

    def get_secret(self, secret_name: str) -> Optional[str]:
        """Retrieve a secret from Infisical."""
        try:
            secret = self.client.secrets.get_secret_by_name(
                secret_name=secret_name,
                project_id=self.project_id,
                environment_slug=self.environment,
                secret_path="/"
            )
            return secret.secretValue
        except Exception as e:
            print(f"Error fetching secret {secret_name}: {str(e)}")
            return None

class Settings(BaseSettings):
    """Application settings with environment variable support and Infisical integration."""
    
    # API Settings
    API_VERSION: str = "1.0.0"
    PROJECT_NAME: str = "Kryptt API"
    DEBUG: bool = False
    
    # Security (fetched from Infisical)
    SECRET_KEY: Optional[str] = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database (fetched from Infisical)
    DATABASE_URL: Optional[str] = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        try:
            infisical = InfisicalConfig()
            # Fetch secrets from Infisical
            self.SECRET_KEY = infisical.get_secret("SECRET_KEY") or "your-secret-key-here"
            self.DATABASE_URL = infisical.get_secret("DATABASE_URL") or "sqlite:///./kryptt.db"
        except Exception as e:
            print(f"Warning: Failed to load secrets from Infisical: {str(e)}")
    
    class Config:
        """Pydantic config for environment variable loading."""
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Create cached instance of settings."""
    return Settings()
