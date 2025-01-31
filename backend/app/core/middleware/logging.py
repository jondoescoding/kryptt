"""
Logging Middleware Configuration

This module configures logging for the API, including request/response logging
and general application logging.

Features:
- Request/Response logging middleware
- Structured JSON logging
- Log rotation
- Different log levels for different environments

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

import logging
import json
import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import Message
from ..config import Settings

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Process the request/response and log details."""
        start_time = time.time()
        
        # Log request
        logging.info(
            "Request started",
            extra={
                "request_id": request.headers.get("X-Request-ID"),
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("User-Agent"),
            }
        )
        
        # Process request and catch any errors
        try:
            response = await call_next(request)
            return_time = time.time() - start_time
            
            # Log response
            logging.info(
                "Request completed",
                extra={
                    "request_id": request.headers.get("X-Request-ID"),
                    "status_code": response.status_code,
                    "processing_time": return_time,
                }
            )
            
            return response
        except Exception as e:
            logging.error(
                "Request failed",
                extra={
                    "request_id": request.headers.get("X-Request-ID"),
                    "error": str(e),
                    "processing_time": time.time() - start_time,
                }
            )
            raise

def setup_logging(settings: Settings) -> None:
    """
    Configure logging for the application.
    
    Args:
        settings: Application settings
    """
    # Define log format based on environment
    log_format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        if settings.DEBUG
        else json.dumps({
            "timestamp": "%(asctime)s",
            "service": "kryptt-api",
            "level": "%(levelname)s",
            "message": "%(message)s",
            "extra": "%(extra)s"
        })
    )
    
    # Set up logging configuration
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(),  # Console handler
            logging.FileHandler(  # File handler
                filename="logs/kryptt-api.log",
                encoding="utf-8",
            ),
        ],
    )
    
    # Suppress noisy logs from other libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING) 