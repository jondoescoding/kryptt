"""
Main FastAPI Application Entry Point

This module initializes and configures the FastAPI application.
It serves as the main entry point for the API server.

Key Components:
- FastAPI app instance creation
- Middleware configuration
- API router registration
- Exception handlers
- Startup and shutdown events

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

import os
from fastapi import FastAPI
from .core.config import get_settings
from .core.middleware import setup_cors, setup_logging, RequestLoggingMiddleware

# Create FastAPI application
app = FastAPI(
    title="Kryptt API",
    description="Backend API for Kryptt trading application",
    version="1.0.0"
)

# Get settings
settings = get_settings()

# Set up logging
setup_logging(settings)

# Set up CORS
setup_cors(app, settings)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)



@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {
        "status": "active",
        "message": "Welcome to Kryptt API",
        "docs_url": "/docs",
        "openapi_url": "/openapi.json"
    }
