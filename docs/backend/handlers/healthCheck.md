# healthCheck Handler

## Purpose

Provides health check endpoints for monitoring system status, service dependencies, and container readiness. Used by Docker health checks, load balancers, and monitoring systems.

## Location

`backend/src/handlers/healthCheck.js`

## Endpoints

### Basic Health Check
- **Method**: GET
- **Path**: `/health`
- **Purpose**: Liveness check - is the service running?

### Readiness Check
- **Method**: GET
- **Path**: `/health/ready`
- **Purpose**: Readiness check - is the service ready to accept requests?

### Database Health
- **Method**: GET
- **Path**: `/health/db`
- **Purpose**: Check DynamoDB connection

### Bedrock Health
- **Method**: GET
- **Path**: `/health/bedrock`
- **Purpose**: Check AWS Bedrock connection

### Cache Health
- **Method**: GET
- **Path**: `/health/cache`
- **Purpose**: Check cache service

### Comprehensive Status
- **Method**: GET
- **Path**: `/health/status`
- **Purpose**: Detailed status of all services

## Outputs

### Basic Health (200)
```json
{
  "status": "healthy",
  "timestamp": number,
  "uptime": number
}
```

### Readiness Check (200 or 503)
```json
{
  "status": "ready|not_ready",
  "timestamp": number,
  "dependencies": {
    "dynamodb": "healthy|unhealthy",
    "bedrock": "healthy|unhealthy",
    "cache": "healthy|unhealthy"
  }
}
```

### Database Health (200 or 503)
```json
{
  "status": "healthy|unhealthy",
  "timestamp": number,
  "responseTime": number,
  "tables": ["string"],
  "error": "string (if unhealthy)"
}
```

### Comprehensive Status (200)
```json
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": number,
  "uptime": number,
  "services": {
    "dynamodb": {
      "status": "healthy|unhealthy",
      "responseTime": number,
      "lastCheck": number,
      "errorCount": number
    },
    "bedrock": {
      "status": "healthy|unhealthy",
      "responseTime": number,
      "lastCheck": number,
      "errorCount": number
    },
    "cache": {
      "status": "healthy|unhealthy",
      "responseTime": number,
      "lastCheck": number,
      "errorCount": number
    }
  }
}
```

## Algorithm

### Basic Health Check
1. Return 200 with current timestamp and uptime
2. No dependency checks

### Readiness Check
1. Check DynamoDB connection (list tables)
2. Check Bedrock connection (list models)
3. Check cache service availability
4. Return 200 if all healthy, 503 if any unhealthy

### Database Health
1. Attempt to list DynamoDB tables
2. Measure response time
3. Return 200 if successful, 503 if failed
4. Include error message if failed

### Comprehensive Status
1. Check all services in parallel
2. Measure response times
3. Aggregate error counts
4. Determine overall status:
   - **healthy**: All services operational
   - **degraded**: Some services slow or intermittent
   - **unhealthy**: Critical services down
5. Return detailed status for each service

## Dependencies

- **Services**:
  - `dynamoClient` - DynamoDB health
  - `bedrockClient` - Bedrock health
  - `cacheService` - Cache health
- **Utils**:
  - `logger` - Log health checks

## Example Usage

```javascript
// Basic health check
GET /health

// Response
{
  "status": "healthy",
  "timestamp": 1704067200,
  "uptime": 3600
}

// Readiness check
GET /health/ready

// Response (healthy)
{
  "status": "ready",
  "timestamp": 1704067200,
  "dependencies": {
    "dynamodb": "healthy",
    "bedrock": "healthy",
    "cache": "healthy"
  }
}

// Response (unhealthy)
{
  "status": "not_ready",
  "timestamp": 1704067200,
  "dependencies": {
    "dynamodb": "unhealthy",
    "bedrock": "healthy",
    "cache": "healthy"
  }
}

// Comprehensive status
GET /health/status

// Response
{
  "status": "healthy",
  "timestamp": 1704067200,
  "uptime": 3600,
  "services": {
    "dynamodb": {
      "status": "healthy",
      "responseTime": 45,
      "lastCheck": 1704067195,
      "errorCount": 0
    },
    "bedrock": {
      "status": "healthy",
      "responseTime": 120,
      "lastCheck": 1704067195,
      "errorCount": 0
    },
    "cache": {
      "status": "healthy",
      "responseTime": 30,
      "lastCheck": 1704067195,
      "errorCount": 0
    }
  }
}
```

## Docker Integration

Used in `docker-compose.yml` health checks:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

## Monitoring Integration

- **Prometheus**: Expose metrics at `/metrics` (future enhancement)
- **CloudWatch**: Log health check results
- **Datadog**: Custom health check integration
- **Load Balancers**: Use `/health/ready` for routing decisions

## Performance Considerations

- Basic health check: <10ms (no I/O)
- Readiness check: 100-300ms (checks dependencies)
- Database health: 50-100ms
- Comprehensive status: 200-500ms (parallel checks)

## Error Handling

- Timeouts after 5 seconds per service check
- Retries not performed (health checks should be fast)
- Errors logged but don't crash the service
- Graceful degradation if checks fail

## Best Practices

1. **Liveness vs. Readiness**:
   - Liveness: Can the container be restarted?
   - Readiness: Should traffic be routed here?

2. **Fast Checks**:
   - Keep health checks under 1 second
   - Use timeouts to prevent hanging

3. **Dependency Checks**:
   - Only check critical dependencies
   - Don't cascade failures unnecessarily

4. **Logging**:
   - Log health check failures
   - Don't log successful checks (too noisy)

## Related Documentation

- [Docker Health Checks](../../infrastructure/docker-compose.md)
- [Monitoring Setup](../../infrastructure/monitoring.md)
