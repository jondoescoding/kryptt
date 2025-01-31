"""
Middleware Package Initialization

This package contains all middleware components for the Kryptt API.
Middleware components handle cross-cutting concerns like logging,
CORS, authentication, and request/response processing.

Components:
- cors.py: CORS configuration and middleware
- logging.py: Logging configuration and middleware

Project: Kryptt
Author: Jon
Social Media:
- Twitter: @jondoescoding
"""

from .cors import setup_cors
from .logging import setup_logging, RequestLoggingMiddleware

__all__ = ["setup_cors", "setup_logging", "RequestLoggingMiddleware"] 