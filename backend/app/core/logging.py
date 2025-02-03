"""
Logging Configuration

This module configures logging for the API, including request/response logging
and general application logging.

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

import logging
import time
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from .config import Settings

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Log request start
        logging.info(f"Request started: {request.method} {request.url}")
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log request completion
        logging.info(
            f"Request completed: {request.method} {request.url} "
            f"- Status: {response.status_code} - Time: {process_time:.2f}s"
        )
        
        return response

def setup_logging(settings: Settings) -> None:
    """Configure logging for the application."""
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                filename="logs/kryptt-api.log",
                encoding="utf-8",
            ),
        ],
    )
    
    # Suppress noisy logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING) 