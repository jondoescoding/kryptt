"""
FastAPI Dependency Injection Module

This module contains FastAPI dependencies that can be reused across different
routes and endpoints. Dependencies are used for:
- Database sessions
- Authentication
- Settings management
- Request validation
- Common business logic

Key Dependencies:
- get_settings: Application configuration
- get_db: Database session
- get_current_user: User authentication

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

from functools import lru_cache
from fastapi import Depends

from .config import Settings, get_settings

# Re-export settings dependency
get_settings = lru_cache()(get_settings)

async def get_db():
    """
    Dependency for getting database session.
    To be implemented when database is set up.
    """
    pass

async def get_current_user():
    """
    Dependency for getting authenticated user.
    To be implemented when authentication is set up.
    """
    pass
