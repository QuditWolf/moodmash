# Container Networking and Communication

This document describes the networking configuration for the VibeGraph Docker Compose setup, including CORS configuration, health checks, and inter-container communication.

## Network Architecture

### Docker Network

All services run on a custom bridge network named `vibegraph-network`:

```yaml
networks:
  vibegraph-network:
    driver: bridge
    name: vibegraph-network
```

This allows services to communicate using DNS names (container names or service names).

### Service Endpoints

| Service | Container Name | Internal Port | External Port | DNS Names |
|---------|---------------|---------------|---------------|-----------|
| Frontend | vibegraph-frontend | 3000 | 3000 | frontend, vibegraph-frontend |
| Backend API | vibegraph-backend-api | 8000 | 8000 | backend-api, vibegraph-backend-api |
| DynamoDB Local | vibegraph-dynamodb-local | 8000 | 8001 | dynamodb-local, vibegraph-dynamodb-local |
| LocalStack | vibegraph-localstack | 4566 | 4566 | localstack, vibegraph-localstack |

## CORS Configuration

### Backend API CORS Settings

The backend API is configured to accept requests from the frontend container:

```python
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
```

### Allowed Origins

- `http://localhost:3000` - Local development (Vite dev server)
- `http://localhost:5173` - Local development (alternative Vite port)
- `http://frontend:3000` - Docker container communication
- `http://vibegraph-frontend:3000` - Docker container communication (full name)

### Preflight Requests

The API automatically handles OPTIONS preflight requests for CORS. Preflight responses are cached for 1 hour (`max_age=3600`).

### Custom Headers

- **Request Headers**: Standard headers plus Authorization for JWT tokens
- **Response Headers**: `X-Process-Time` header shows request processing time

## Health Check System

### Health Check Endpoints

The backend API provides comprehensive health check endpoints:

#### 1. Basic Health Check (Liveness)

```
GET /health
```

Returns basic service status. Used by Docker for liveness probes.

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "vibegraph-api"
}
```

#### 2. Readiness Check

```
GET /health/ready
```

Checks all critical dependencies before marking service as ready.

**Response (200 OK if ready, 503 if not ready)**:
```json
{
  "status": "ready",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "vibegraph-api",
  "dependencies": {
    "dynamodb": {
      "status": "healthy",
      "tables": {
        "vibegraph-users": {"status": "ACTIVE", "healthy": true},
        "vibegraph-sessions": {"status": "ACTIVE", "healthy": true},
        "vibegraph-embedding-cache": {"status": "ACTIVE", "healthy": true}
      }
    },
    "bedrock": {
      "status": "healthy",
      "models_available": 2
    },
    "cache": {
      "status": "healthy",
      "table_status": "ACTIVE"
    }
  }
}
```

#### 3. DynamoDB Health Check

```
GET /health/db
```

Checks DynamoDB connection and table status.

**Response (200 OK if healthy, 503 if unhealthy)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "dynamodb",
  "details": {
    "status": "healthy",
    "tables": {
      "vibegraph-users": {"status": "ACTIVE", "healthy": true},
      "vibegraph-sessions": {"status": "ACTIVE", "healthy": true},
      "vibegraph-embedding-cache": {"status": "ACTIVE", "healthy": true}
    },
    "endpoint": "http://dynamodb-local:8000"
  }
}
```

#### 4. Bedrock Health Check

```
GET /health/bedrock
```

Checks AWS Bedrock availability.

**Note**: This may return unhealthy in local development with LocalStack.

**Response (200 OK if healthy, 503 if unhealthy)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "bedrock",
  "details": {
    "status": "healthy",
    "endpoint": "http://localstack:4566",
    "models_available": 2
  }
}
```

#### 5. Cache Health Check

```
GET /health/cache
```

Checks embedding cache table status.

**Response (200 OK if healthy, 503 if unhealthy)**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "cache",
  "details": {
    "status": "healthy",
    "table_status": "ACTIVE",
    "item_count": 42,
    "table_name": "vibegraph-embedding-cache"
  }
}
```

#### 6. Comprehensive Status Dashboard

```
GET /health/status
```

Provides detailed status of all services for monitoring dashboards.

**Response (200 OK)**:
```json
{
  "status": "operational",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "service": "vibegraph-api",
  "version": "1.0.0",
  "uptime": "N/A",
  "dependencies": {
    "dynamodb": { "status": "healthy", "details": {...} },
    "bedrock": { "status": "healthy", "details": {...} },
    "cache": { "status": "healthy", "details": {...} },
    "overall_status": "healthy"
  },
  "health_summary": {
    "healthy": true,
    "critical_services": {
      "dynamodb": true,
      "cache": true
    },
    "optional_services": {
      "bedrock": true
    }
  }
}
```

### Docker Health Check Configuration

Each service has a health check configured in `docker-compose.yml`:

#### Frontend Health Check

```yaml
healthcheck:
  test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000"]
  interval: 15s
  timeout: 5s
  retries: 3
  start_period: 30s
```

#### Backend API Health Check

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health/ready"]
  interval: 15s
  timeout: 5s
  retries: 5
  start_period: 30s
```

#### DynamoDB Local Health Check

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -s http://localhost:8000 || exit 1"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 20s
```

#### LocalStack Health Check

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:4566/_localstack/health"]
  interval: 10s
  timeout: 5s
  retries: 5
  start_period: 30s
```

### Health Check Parameters

- **interval**: Time between health checks
- **timeout**: Maximum time to wait for health check response
- **retries**: Number of consecutive failures before marking unhealthy
- **start_period**: Grace period during container startup

## Connection Validation

### Retry Logic with Exponential Backoff

All connection checks implement retry logic with exponential backoff:

```python
# Default configuration
max_retries = 3
initial_backoff = 0.1  # 100ms
max_backoff = 2.0      # 2 seconds
backoff_multiplier = 2.0

# Backoff sequence: 100ms, 200ms, 400ms
```

### Connection Checker

The `ConnectionChecker` class provides methods for validating connections:

```python
from utils.connection_check import connection_checker

# Check DynamoDB connection
status, details = connection_checker.check_dynamodb_connection()

# Check Bedrock connection
status, details = connection_checker.check_bedrock_connection()

# Check network connectivity
status, details = connection_checker.check_network_connectivity("dynamodb-local", 8000)

# Check all connections
results = connection_checker.check_all_connections()
```

### Connection Status

Connection checks return a `ConnectionStatus` enum:

- `CONNECTED`: Service is reachable and healthy
- `DISCONNECTED`: Service is unreachable
- `DEGRADED`: Service is reachable but not fully healthy
- `UNKNOWN`: Unable to determine status

## Startup Dependency Checks

### Fail-Fast Logic

The backend API implements startup checks with fail-fast logic:

```python
from startup import run_startup_checks, StartupCheckError

try:
    run_startup_checks(fail_fast=True)
except StartupCheckError as e:
    # Application will not start
    logger.critical(f"Startup checks failed: {e}")
    raise
```

### Startup Check Sequence

1. **Environment Variables**: Verify all required variables are set
2. **Network Connectivity**: Check network access to DynamoDB
3. **DynamoDB Connection**: Verify all tables are ACTIVE
4. **Bedrock Connection**: Check Bedrock availability (optional)

### Startup Check Output

```
============================================================
Running startup dependency checks...
============================================================

Checking environment variables...
✓ AWS_REGION=us-east-1
✓ USERS_TABLE=vibegraph-users
✓ SESSIONS_TABLE=vibegraph-sessions
✓ CACHE_TABLE=vibegraph-embedding-cache

Checking network connectivity...
✓ Network connectivity to DynamoDB (dynamodb-local:8000)
  Latency: 2.34ms

Checking DynamoDB connection...
✓ DynamoDB connection successful
  Tables: vibegraph-users, vibegraph-sessions, vibegraph-embedding-cache

Checking Bedrock connection...
⚠ Bedrock connection failed (expected in local dev)

============================================================
✓ All critical startup checks passed
  Passed: 4 checks
  Note: Bedrock unavailable (expected in local dev)
============================================================
```

## Inter-Container Communication

### DNS Resolution

Services can communicate using DNS names:

```bash
# From backend-api container
curl http://dynamodb-local:8000
curl http://localstack:4566/_localstack/health

# From frontend container
curl http://backend-api:8000/health
```

### Testing Connectivity

Use the connectivity test script to verify inter-container communication:

```bash
# Run from backend-api container
python /app/scripts/test_connectivity.py
```

This script tests:
- DNS resolution for all services
- TCP connectivity to all service ports
- HTTP endpoint availability

### Example Test Output

```
============================================================
VibeGraph Inter-Container Communication Tests
============================================================

============================================================
Testing: Backend API
============================================================

DNS Resolution: backend-api
✓ Resolved to 172.18.0.3

TCP Connection: backend-api:8000
✓ Connected (latency: 2.45ms)

HTTP Endpoint: http://backend-api:8000/health
✓ HTTP 200

============================================================
Test Summary
============================================================
Total tests: 12
✓ Passed: 12

Success rate: 100.0%

✓ All connectivity tests passed!
```

## Service Dependencies

### Dependency Graph

```
frontend
  └─> backend-api (condition: service_healthy)
        ├─> dynamodb-local (condition: service_healthy)
        └─> localstack (condition: service_healthy)

backend-handlers
  ├─> backend-services (condition: service_started)
  ├─> dynamodb-local (condition: service_healthy)
  └─> localstack (condition: service_healthy)

backend-services
  └─> dynamodb-local (condition: service_healthy)

dynamodb-init
  └─> dynamodb-local (condition: service_healthy)
```

### Startup Order

1. **dynamodb-local** - Starts first, waits for health check
2. **localstack** - Starts in parallel with DynamoDB
3. **dynamodb-init** - Runs once to create tables
4. **backend-services** - Starts after DynamoDB is healthy
5. **backend-api** - Starts after DynamoDB and LocalStack are healthy
6. **backend-handlers** - Starts after backend-services and dependencies
7. **frontend** - Starts last, after backend-api is healthy

## Troubleshooting

### Common Issues

#### 1. CORS Errors

**Symptom**: Frontend requests blocked by CORS policy

**Solution**: Verify frontend origin is in `allow_origins` list:
```python
allow_origins=[
    "http://localhost:3000",
    "http://frontend:3000",
    # Add your origin here
]
```

#### 2. Service Not Ready

**Symptom**: Health check returns 503

**Solution**: Check dependency status:
```bash
curl http://localhost:8000/health/status
```

#### 3. DNS Resolution Failure

**Symptom**: Cannot resolve service hostname

**Solution**: Verify all services are on the same network:
```bash
docker network inspect vibegraph-network
```

#### 4. Connection Timeout

**Symptom**: Requests timeout between containers

**Solution**: Check service health and logs:
```bash
docker-compose ps
docker-compose logs backend-api
```

### Debugging Commands

```bash
# Check service health
docker-compose ps

# View service logs
docker-compose logs -f backend-api

# Test connectivity from container
docker-compose exec backend-api curl http://dynamodb-local:8000

# Run connectivity tests
docker-compose exec backend-api python /app/scripts/test_connectivity.py

# Inspect network
docker network inspect vibegraph-network

# Check health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/status
```

## Production Considerations

### CORS Configuration

In production, restrict `allow_origins` to specific domains:

```python
allow_origins=[
    "https://vibegraph.com",
    "https://www.vibegraph.com",
]
```

### Health Check Intervals

Adjust health check intervals based on load:

```yaml
healthcheck:
  interval: 30s  # Increase for production
  timeout: 10s
  retries: 3
```

### Connection Pooling

Implement connection pooling for DynamoDB and Bedrock clients to improve performance.

### Monitoring

Integrate health check endpoints with monitoring tools:
- Prometheus metrics
- CloudWatch alarms
- Datadog monitoring
- Custom dashboards

### Load Balancing

Use health checks for load balancer target health:
- ALB target health checks
- ECS service health checks
- Kubernetes liveness/readiness probes

## References

- [Docker Compose Networking](https://docs.docker.com/compose/networking/)
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [Docker Health Checks](https://docs.docker.com/engine/reference/builder/#healthcheck)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
