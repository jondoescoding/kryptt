"""
CORS Middleware Configuration

This module configures Cross-Origin Resource Sharing (CORS) for the API.
It defines allowed origins, methods, and headers for cross-origin requests.

Configuration:
- Allowed origins (domains that can access the API)
- Allowed methods (HTTP methods that can be used)
- Allowed headers (HTTP headers that can be included)
- Credentials support (whether to allow cookies/authentication)

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from ..config import Settings

def setup_cors(app: FastAPI, settings: Settings) -> None:
    """
    Configure CORS for the application.
    
    Args:
        app: FastAPI application instance
        settings: Application settings
    """
    # Define allowed origins based on environment
    origins = [
        "http://localhost:3000",  # Next.js development server
        "http://localhost:8000",  # FastAPI development server
    ]
    
    # Add production origins if not in debug mode
    if not settings.DEBUG:
        origins.extend([
            "https://kryptt.com",
            "https://api.kryptt.com",
        ])
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=[
            "Content-Type",
            "Authorization",
            "Accept",
            "Origin",
            "X-Requested-With",
        ],
    ) 