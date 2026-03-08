# API Gateway Entry Point

## Overview

The `backend/api/main.py` file serves as the main entry point for the VibeGraph backend API gateway. It sets up a FastAPI application with CORS middleware, health check endpoints, request logging, and global error handling.

## Purpose

- Provide a centralized entry point for all backend API requests
- Handle CORS configuration for frontend communication
- Implement health check endpoints for container orchestration
- Log all incoming requests and responses
- Handle global exceptions gracefully

## Components

### FastAPI Application

```python
app = FastAPI(
    title="VibeGraph API",
    description="Backend API for VibeGraph adaptive quiz and taste profiling system",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
```

The FastAPI application is configured with:
- **Title**: VibeGraph API
- **Version**: 1.0.0
- **Documentation**: Available at `/api/docs` (Swagger UI) and `/api/redoc` (ReDoc)

### CORS Middleware

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://frontend:3000",
        "http://frontend:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Configuration**:
- **Allowed Origins**: Frontend container and localhost (development)
- **Credentials**: Enabled for cookie-based authentication
- **Methods**: All HTTP methods allowed
- **Headers**: All headers allowed

**Production Note**: In production, restrict `allow_origins` to specific domains only.

### Request Logging Middleware

The request logging middleware logs:
- Request method and path
- Client IP address
- Response status code
- Request processing time

**Example Log Output**:
```
2024-01-15 10:30:45 - __main__ - INFO - Incoming request: GET /health from 172.18.0.5
2024-01-15 10:30:45 - __main__ - INFO - Request completed: GET /health status=200 duration=0.003s
```

The middleware also adds an `X-Process-Time` header to all responses with the processing time in seconds.

## Endpoints

### GET /health

**Purpose**: Basic health check for container liveness probe

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "vibegraph-api"
}
```

**Usage**: Used by Docker health checks to verify the container is running.

### GET /health/ready

**Purpose**: Readiness check for container readiness probe

**Response** (200 OK):
```json
{
  "status": "ready",
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "vibegraph-api",
  "dependencies": {
    "dynamodb": "not_checked",
    "bedrock": "not_checked",
    "cache": "not_checked"
  }
}
```

**Future Enhancement**: This endpoint will be enhanced to verify:
- DynamoDB connection
- Bedrock availability
- Cache service status

**Usage**: Used by Docker to verify the container is ready to accept traffic.

### GET /

**Purpose**: Root endpoint providing API information

**Response** (200 OK):
```json
{
  "name": "VibeGraph API",
  "version": "1.0.0",
  "docs": "/api/docs"
}
```

## Error Handling

### Global Exception Handler

All unhandled exceptions are caught by the global exception handler:

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Logs error and returns generic error response
```

**Response** (500 Internal Server Error):
```json
{
  "message": "Internal server error",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

**Behavior**:
- Logs full exception with stack trace
- Returns generic error message to client (no sensitive details)
- Includes timestamp for correlation with logs

## Lifecycle Events

### Startup Event

```python
@app.on_event("startup")
async def startup_event():
    # Initialization tasks
```

**Current Behavior**:
- Logs startup message
- Initializes FastAPI application

**Future Enhancements**:
- Initialize database connection pools
- Verify dependency availability
- Load configuration

### Shutdown Event

```python
@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup tasks
```

**Current Behavior**:
- Logs shutdown message

**Future Enhancements**:
- Close database connections
- Cleanup resources
- Flush logs

## Running the Application

### Development Mode

**Using Docker Compose** (recommended):
```bash
make up
```

**Direct execution**:
```bash
cd backend/api
python main.py
```

**Using uvicorn**:
```bash
cd backend/api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Production Considerations**:
- Use multiple workers for better performance
- Disable auto-reload
- Restrict CORS origins to production domains
- Enable HTTPS/TLS
- Use environment variables for configuration

## Configuration

### Environment Variables

Currently, the application uses default configuration. Future enhancements will support:

- `API_HOST`: Host to bind to (default: 0.0.0.0)
- `API_PORT`: Port to listen on (default: 8000)
- `LOG_LEVEL`: Logging level (default: INFO)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `DYNAMODB_ENDPOINT`: DynamoDB endpoint URL
- `BEDROCK_ENDPOINT`: Bedrock endpoint URL

## Logging

### Log Format

```
%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Example**:
```
2024-01-15 10:30:45,123 - __main__ - INFO - Starting VibeGraph API Gateway...
```

### Log Levels

- **INFO**: Normal operations (requests, responses, startup/shutdown)
- **ERROR**: Unhandled exceptions and errors
- **WARNING**: Potential issues (future)
- **DEBUG**: Detailed debugging information (future)

## Testing

### Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "service": "vibegraph-api"
}
```

### CORS Test

```bash
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/health
```

**Expected Headers**:
- `Access-Control-Allow-Origin: http://localhost:3000`
- `Access-Control-Allow-Methods: *`
- `Access-Control-Allow-Headers: *`

### API Documentation

Visit `http://localhost:8000/api/docs` for interactive Swagger UI documentation.

## Future Enhancements

1. **Dependency Health Checks**: Implement actual checks for DynamoDB, Bedrock, and cache service in `/health/ready`
2. **Route Registration**: Add quiz and profile route modules
3. **Authentication Middleware**: Add JWT token validation
4. **Rate Limiting**: Implement rate limiting per user/IP
5. **Metrics**: Add Prometheus metrics endpoint
6. **Structured Logging**: Use JSON logging for better log aggregation
7. **Configuration Management**: Use environment variables and config files
8. **API Versioning**: Support multiple API versions

## Related Documentation

- [Backend README](../README.md)
- [Docker Configuration](../../infrastructure/docker.md)
- [Networking](../../infrastructure/networking.md)
- [API Endpoints](../../api/endpoints.md)
