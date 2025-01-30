"""
API V1 Package Initialization

This module initializes the v1 version of the API.
It combines all endpoint routers into a single v1 router.

Components:
- Router configuration
- Endpoint registration
- Version-specific middleware

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

from fastapi import APIRouter
from .endpoints import health

# Create v1 router
router = APIRouter(prefix="/v1")

# Include all endpoint routers
router.include_router(health.router, tags=["Health"])
