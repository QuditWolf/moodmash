"""
FastAPI API Gateway Entry Point for VibeGraph Backend

This module serves as the main entry point for the VibeGraph backend API gateway.
It sets up FastAPI with CORS middleware, health check endpoints, and request logging.
"""

import logging
import time
import os
from typing import Dict, Any
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Import structured logging utilities
import sys
sys.path.insert(0, '/app/src')
from utils.logger import setup_structured_logging, get_logger, log_api_request, filter_sensitive_data

# Configure structured JSON logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
log_file = os.getenv('LOG_FILE', '/app/logs/api.log')

# Ensure logs directory exists
os.makedirs(os.path.dirname(log_file), exist_ok=True)

# Set up structured logging
setup_structured_logging(log_level=log_level, log_file=log_file)
logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="VibeGraph API",
    description="Backend API for VibeGraph adaptive quiz and taste profiling system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS middleware for frontend communication
# Allow requests from frontend container and localhost for development
# In production, this should be restricted to specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://frontend:3000",
        "http://frontend:5173",
        "http://vibegraph-frontend:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "Accept",
        "Origin",
        "X-Requested-With",
    ],
    expose_headers=["X-Process-Time"],
    max_age=3600,  # Cache preflight requests for 1 hour
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log all incoming requests and their response times with structured logging.
    
    This middleware logs:
    - Request method and path
    - Client IP address
    - Response status code
    - Request processing time
    - Request headers (filtered for sensitive data)
    """
    start_time = time.time()
    
    # Extract request context (filter sensitive data)
    request_context = {
        'client_ip': request.client.host if request.client else 'unknown',
        'user_agent': request.headers.get('user-agent', 'unknown'),
        'query_params': dict(request.query_params) if request.query_params else {}
    }
    
    # Filter sensitive data from context
    request_context = filter_sensitive_data(request_context)
    
    # Process request
    response = await call_next(request)
    
    # Calculate processing time
    process_time = time.time() - start_time
    
    # Log API request with structured data
    log_api_request(
        logger=logger,
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=process_time,
        **request_context
    )
    
    # Add processing time header
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Import health check functions
from health import (
    get_basic_health,
    get_readiness_status,
    get_db_health,
    get_bedrock_health,
    get_cache_health,
    get_comprehensive_status
)


# Health check endpoints
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check() -> Dict[str, Any]:
    """
    Basic health check endpoint for container liveness probe.
    
    Returns:
        Dict with status and timestamp
    """
    return get_basic_health()


@app.get("/health/ready")
async def readiness_check() -> JSONResponse:
    """
    Readiness check endpoint for container readiness probe.
    
    Verifies that all critical dependencies are available:
    - DynamoDB tables
    - Cache service
    - Bedrock (optional in local dev)
    
    Returns:
        JSONResponse with 200 if ready, 503 if not ready
    """
    status_code, response_data = get_readiness_status()
    return JSONResponse(status_code=status_code, content=response_data)


@app.get("/health/db")
async def db_health_check() -> JSONResponse:
    """
    DynamoDB health check endpoint.
    
    Checks the status of all DynamoDB tables.
    
    Returns:
        JSONResponse with 200 if healthy, 503 if unhealthy
    """
    status_code, response_data = get_db_health()
    return JSONResponse(status_code=status_code, content=response_data)


@app.get("/health/bedrock")
async def bedrock_health_check() -> JSONResponse:
    """
    Bedrock health check endpoint.
    
    Checks AWS Bedrock availability.
    Note: May return unhealthy in local development.
    
    Returns:
        JSONResponse with 200 if healthy, 503 if unhealthy
    """
    status_code, response_data = get_bedrock_health()
    return JSONResponse(status_code=status_code, content=response_data)


@app.get("/health/cache")
async def cache_health_check() -> JSONResponse:
    """
    Cache service health check endpoint.
    
    Checks the embedding cache table status.
    
    Returns:
        JSONResponse with 200 if healthy, 503 if unhealthy
    """
    status_code, response_data = get_cache_health()
    return JSONResponse(status_code=status_code, content=response_data)


@app.get("/health/status")
async def comprehensive_status() -> Dict[str, Any]:
    """
    Comprehensive service status endpoint for monitoring dashboard.
    
    Provides detailed status of all services and dependencies.
    
    Returns:
        Dict with comprehensive service status
    """
    return get_comprehensive_status()


# Root endpoint
@app.get("/")
async def root() -> Dict[str, str]:
    """
    Root endpoint providing API information.
    
    Returns:
        Dict with API name and version
    """
    return {
        "name": "VibeGraph API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled errors.
    
    Logs the error and returns a generic error response to the client.
    
    Args:
        request: The incoming request
        exc: The exception that was raised
        
    Returns:
        JSONResponse with error details
    """
    logger.error(
        f"Unhandled exception for {request.method} {request.url.path}: {str(exc)}",
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Register API routes
from routes import quiz, profile

app.include_router(quiz.router)
app.include_router(profile.router)


# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Startup event handler.
    
    Performs initialization tasks when the application starts:
    - Run dependency checks
    - Verify all critical services are available
    - Initialize connections
    """
    logger.info("Starting VibeGraph API Gateway...")
    
    # Import startup checker
    from startup import run_startup_checks, StartupCheckError
    
    try:
        # Run startup checks with fail-fast logic
        run_startup_checks(fail_fast=True)
        logger.info("All startup checks passed successfully")
    except StartupCheckError as e:
        logger.critical(f"Startup checks failed: {e}")
        logger.critical("Application will not start. Please fix the issues and restart.")
        # Re-raise to prevent application from starting
        raise
    except Exception as e:
        logger.error(f"Unexpected error during startup checks: {e}")
        # Continue anyway for development
        logger.warning("Continuing despite startup check errors...")
    
    logger.info("Registered routes: quiz, profile, health")
    logger.info("FastAPI application initialized successfully")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler.
    
    Performs cleanup tasks when the application shuts down:
    - Log shutdown message
    - Close connections (future)
    - Cleanup resources (future)
    """
    logger.info("Shutting down VibeGraph API Gateway...")
    # TODO: Add connection cleanup
    # TODO: Add resource cleanup


if __name__ == "__main__":
    # This allows running the app directly with: python main.py
    # In production, use: uvicorn main:app
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
