# Logging and Monitoring

This document describes the logging and monitoring infrastructure for the VibeGraph backend integration.

## Overview

The VibeGraph system implements structured JSON logging across all backend services and comprehensive error logging in the frontend. Logs are aggregated in a shared volume and can be rotated automatically to prevent disk space issues.

## Backend Logging

### Structured JSON Logging

All backend services use structured JSON logging for consistent, parseable log output. Each log entry includes:

- **timestamp**: ISO 8601 timestamp in UTC
- **level**: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **logger**: Logger name (module/component)
- **message**: Human-readable log message
- **context**: Additional structured data (request IDs, user IDs, etc.)
- **error**: Error details for exceptions (type, message, traceback)

### Log Format Example

```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO",
  "logger": "backend.api.main",
  "message": "POST /api/quiz/section1/start - 200 (0.234s)",
  "context": {
    "method": "POST",
    "path": "/api/quiz/section1/start",
    "status_code": 200,
    "duration_ms": 234,
    "client_ip": "172.18.0.5",
    "user_agent": "Mozilla/5.0..."
  }
}
```

### What Gets Logged

#### API Requests
- HTTP method and path
- Response status code
- Request duration
- Client IP address
- User agent (filtered)
- Query parameters (filtered for sensitive data)

#### Handler Execution
- Handler name
- Execution duration
- Success/failure status
- Session IDs
- Question counts
- Error details (if failed)

#### External API Calls
- Claude API calls with response times
- Titan API calls with response times
- DynamoDB operations

#### Errors
- Error type and message
- Stack trace (full trace in logs, summary in responses)
- Request context
- User context (filtered for PII)

### What Does NOT Get Logged

For security and privacy, the following are never logged:

- JWT tokens or authorization headers
- Raw quiz answers
- Embedding vectors (1024-dimensional arrays)
- Passwords or API keys
- Any PII (personally identifiable information)

All sensitive data is automatically filtered using the `filter_sensitive_data()` function.

### Configuration

Backend logging is configured via environment variables:

```bash
# Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Log file path
LOG_FILE=/app/logs/api.log

# Unbuffered output for real-time logs
PYTHONUNBUFFERED=1
```

### Usage in Code

#### Basic Logging

```python
from utils.logger import get_logger

logger = get_logger(__name__)

# Simple log messages
logger.info("Processing request")
logger.error("Failed to process", exc_info=True)
```

#### Structured Context

```python
from utils.logger import LogContext

# Add context to all logs within the block
with LogContext(logger, session_id=session_id, user_id=user_id):
    logger.info("Starting Section 1 generation")
    # ... processing ...
    logger.info("Section 1 completed")
```

#### API Request Logging

```python
from utils.logger import log_api_request

log_api_request(
    logger=logger,
    method="POST",
    path="/api/quiz/section1/start",
    status_code=200,
    duration=0.234,
    session_id=session_id
)
```

#### Handler Execution Logging

```python
from utils.logger import log_handler_execution

log_handler_execution(
    logger=logger,
    handler_name="generate_section1",
    duration=1.234,
    success=True,
    session_id=session_id,
    question_count=5
)
```

## Frontend Logging

### Console Logging

The frontend uses structured console logging for development and debugging:

- **DEBUG**: Detailed debugging information (development only)
- **INFO**: General informational messages
- **WARN**: Warning messages for potential issues
- **ERROR**: Error messages with stack traces

### Error Boundary

React Error Boundary components catch and log component errors:

```jsx
import ErrorBoundary from './components/ErrorBoundary';

<ErrorBoundary name="OnboardingFlow">
  <OnboardingPage />
</ErrorBoundary>
```

The Error Boundary:
- Catches React component errors
- Logs errors with component stack traces
- Displays user-friendly error UI
- Provides "Try Again" and "Go Home" options
- Shows error details in development mode

### API Error Logging

All API errors are automatically logged with context:

```javascript
import { getLogger } from './utils/logger';

const logger = getLogger('MyComponent');

try {
  const result = await vibeGraphAPI.quiz.startSection1();
} catch (error) {
  logger.error('Failed to start quiz', error, {
    component: 'OnboardingPage',
    phase: 'section1'
  });
}
```

### Usage in Code

```javascript
import { getLogger } from '../utils/logger';

const logger = getLogger('ComponentName');

// Log levels
logger.debug('Debug message', { data: 'value' });
logger.info('Info message', { data: 'value' });
logger.warn('Warning message', { data: 'value' });
logger.error('Error message', error, { data: 'value' });

// API logging (automatic in vibeGraphAPI)
logger.logApiRequest('POST', '/api/quiz/start', 200, 234);
logger.logApiError('POST', '/api/quiz/start', error);
```

## Log Aggregation

### Shared Logs Directory

All backend containers write logs to a shared volume mounted at `/app/logs`:

```yaml
volumes:
  - ./logs:/app/logs
```

This allows:
- Centralized log collection
- Easy access from host machine
- Log aggregation across containers
- Persistent logs across container restarts

### Log Files

Each service writes to its own log file:

- `api.log` - API gateway logs
- `handlers.log` - Handler execution logs (future)
- `services.log` - Service layer logs (future)

### Accessing Logs

#### View logs from host machine
```bash
# View all logs
tail -f logs/*.log

# View API logs only
tail -f logs/api.log

# View logs with JSON formatting
tail -f logs/api.log | jq .
```

#### View logs from container
```bash
# View API container logs
docker logs vibegraph-backend-api

# Follow logs in real-time
docker logs -f vibegraph-backend-api

# View last 100 lines
docker logs --tail 100 vibegraph-backend-api
```

#### Using Makefile commands
```bash
# View all container logs
make logs

# View specific service logs
make logs-backend
make logs-frontend
```

## Log Rotation

### Configuration

Log rotation is configured in `backend/logrotate.conf`:

```
/app/logs/*.log {
    daily              # Rotate daily
    rotate 30          # Keep 30 days of logs
    compress           # Compress old logs
    delaycompress      # Compress after 1 day
    missingok          # Don't error if missing
    notifempty         # Don't rotate if empty
    create 0644        # File permissions
    dateext            # Use date suffix
    size 100M          # Max size before rotation
}
```

### Rotation Schedule

- **Frequency**: Daily at midnight
- **Retention**: 30 days
- **Compression**: Gzip after 1 day
- **Max Size**: 100MB per file
- **Naming**: `api.log.20240115.gz`

### Manual Rotation

To manually rotate logs:

```bash
# Rotate all logs
logrotate -f backend/logrotate.conf

# Test rotation without executing
logrotate -d backend/logrotate.conf
```

## Monitoring

### Health Check Logs

Health check endpoints log their status:

```bash
# Check all services
curl http://localhost:8000/health/status | jq .

# Check specific service
curl http://localhost:8000/health/db | jq .
```

### Log Monitoring

Monitor logs for errors and warnings:

```bash
# Watch for errors
tail -f logs/api.log | grep -i error

# Watch for slow requests (>1s)
tail -f logs/api.log | jq 'select(.context.duration_ms > 1000)'

# Count errors per minute
tail -f logs/api.log | jq -r 'select(.level=="ERROR") | .timestamp' | uniq -c
```

### Metrics to Monitor

- **Request Rate**: Requests per second
- **Response Time**: Average and P95 response times
- **Error Rate**: Errors per minute
- **Handler Duration**: Handler execution times
- **Cache Hit Rate**: Embedding cache hit percentage
- **API Call Duration**: Claude/Titan API response times

## Best Practices

### Do's

✅ Use structured logging with context
✅ Log all API requests and responses
✅ Log handler execution times
✅ Filter sensitive data before logging
✅ Include request IDs for tracing
✅ Log errors with full context
✅ Use appropriate log levels
✅ Add context managers for related logs

### Don'ts

❌ Don't log sensitive data (tokens, passwords, PII)
❌ Don't log raw quiz answers
❌ Don't log embedding vectors
❌ Don't log at DEBUG level in production
❌ Don't log inside tight loops
❌ Don't log without context
❌ Don't ignore log rotation

## Troubleshooting

### Logs not appearing

1. Check log file permissions:
   ```bash
   ls -la logs/
   ```

2. Check container logs:
   ```bash
   docker logs vibegraph-backend-api
   ```

3. Verify log directory is mounted:
   ```bash
   docker inspect vibegraph-backend-api | jq '.[0].Mounts'
   ```

### Disk space issues

1. Check log file sizes:
   ```bash
   du -sh logs/*
   ```

2. Manually rotate logs:
   ```bash
   logrotate -f backend/logrotate.conf
   ```

3. Clean old logs:
   ```bash
   find logs/ -name "*.gz" -mtime +30 -delete
   ```

### Performance impact

If logging impacts performance:

1. Increase log level to WARNING or ERROR
2. Disable debug logging in production
3. Use asynchronous logging (future enhancement)
4. Reduce log verbosity

## Future Enhancements

- [ ] Centralized log aggregation (ELK stack, CloudWatch)
- [ ] Real-time log streaming
- [ ] Automated alerting on errors
- [ ] Log analytics dashboard
- [ ] Distributed tracing with correlation IDs
- [ ] Asynchronous logging for better performance
- [ ] Log sampling for high-volume endpoints

## References

- [Python Logging Documentation](https://docs.python.org/3/library/logging.html)
- [Logrotate Manual](https://linux.die.net/man/8/logrotate)
- [Structured Logging Best Practices](https://www.structlog.org/)
- [React Error Boundaries](https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary)
