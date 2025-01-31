"""
Health Check Endpoints

This module provides endpoints for checking the health and status
of the API and its dependencies.

Endpoints:
- GET /health: Basic health check
- GET /health/detailed: Detailed system status

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

from fastapi import APIRouter, Depends
from typing import Dict
from ....core.dependencies import get_settings
from ....core.config import Settings

router = APIRouter(prefix="/health")

@router.get("")
async def health_check() -> Dict[str, str]:
    """
    Basic health check endpoint.
    Returns a simple status indicating the API is running.
    """
    return {
        "status": "healthy",
        "message": "API is operational"
    }

@router.get("/detailed")
async def detailed_health(settings: Settings = Depends(get_settings)) -> Dict[str, str]:
    """
    Detailed health check endpoint.
    Returns system version and environment information.
    """
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "environment": "development" if settings.DEBUG else "production",
        "project": settings.PROJECT_NAME
    }
