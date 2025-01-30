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
Date: January 2024
"""

from fastapi import FastAPI

app = FastAPI(
    title="Kryptt API",
    description="Backend API for Kryptt trading application",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Root endpoint to verify API is running."""
    return {"status": "active", "message": "Welcome to Kryptt API"}
