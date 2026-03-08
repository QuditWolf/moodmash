# Troubleshooting Guide

This guide provides solutions to common issues you may encounter when running VibeGraph. Issues are organized by category with diagnostic commands and step-by-step solutions.

## Table of Contents

- [Container Startup Issues](#container-startup-issues)
- [Health Check Failures](#health-check-failures)
- [Connection Timeouts](#connection-timeouts)
- [Database Issues](#database-issues)
- [API Errors](#api-errors)
- [Frontend Issues](#frontend-issues)
- [Performance Issues](#performance-issues)
- [Diagnostic Commands](#diagnostic-commands)

## Container Startup Issues

### Containers Won't Start

**Symptoms:**
- `make up` fails with error
- Containers exit immediately after starting
- `docker ps` shows no running containers

**Diagnosis:**
```bash
# Check container status
docker-compose ps

# View logs for errors
make logs

# Check Docker daemon status
docker info
```

**Common Causes and Solutions:**

#### 1. Port Already in Use

**Error Message:** `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Solution:**
```bash
# Find process using the port
lsof -i :8000

# Kill the process
kill -9 [PID]

# Or change port in docker-compose.yml
# Edit docker-compose.yml and change port mapping:
# ports:
#   - "8001:8000"  # Use different external port
```

#### 2. Insufficient Docker Resources

**Error Message:** `Cannot start service: insufficient memory`

**Solution:**
```bash
# Check Docker resources
docker info | grep -E "CPUs|Total Memory"

# Increase Docker memory:
# - Docker Desktop: Settings → Resources → Memory (set to 8GB+)
# - Linux: Edit /etc/docker/daemon.json
```

#### 3. Image Build Failures

**Error Message:** `failed to solve: process "/bin/sh -c npm install" did not complete successfully`

**Solution:**
```bash
# Clean Docker build cache
docker builder prune -a

# Rebuild without cache
make rebuild

# Check for network issues
ping registry.npmjs.org
ping pypi.org
```

#### 4. Permission Issues

**Error Message:** `Permission denied` or `EACCES`

**Solution:**
```bash
# Fix file permissions
chmod -R 755 ./frontend
chmod -R 755 ./backend

# Fix ownership (Linux)
sudo chown -R $USER:$USER .

# Run with current user
docker-compose run --user $(id -u):$(id -g) backend-api sh
```

### Containers Start But Exit Immediately

**Diagnosis:**
```bash
# Check exit codes
docker-compose ps

# View container logs
docker logs vibegraph-backend-api

# Check for errors in entrypoint
docker-compose logs backend-api | grep -i error
```

**Common Causes:**

#### 1. Missing Environment Variables

**Solution:**
```bash
# Verify environment files exist
ls -la frontend/.env
ls -la backend/.env

# Copy from examples if missing
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env

# Verify variables are loaded
docker-compose config | grep -A 10 environment
```

#### 2. Entrypoint Script Errors

**Solution:**
```bash
# Check entrypoint script syntax
bash -n backend/docker-entrypoint.sh

# Make entrypoint executable
chmod +x backend/docker-entrypoint.sh
chmod +x frontend/docker-entrypoint.sh

# Test entrypoint manually
docker-compose run backend-api bash
```

#### 3. Dependency Installation Failures

**Solution:**
```bash
# Rebuild with verbose output
docker-compose build --no-cache --progress=plain backend-api

# Check requirements files
cat backend/requirements.txt
cat frontend/package.json

# Test dependency installation locally
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

## Health Check Failures

### Health Checks Never Pass

**Symptoms:**
- `make wait-healthy` times out
- `docker ps` shows containers as "unhealthy"
- Health check endpoints return errors

**Diagnosis:**
```bash
# Check health status
make health

# View health check logs
docker inspect vibegraph-backend-api | jq '.[0].State.Health'

# Test health endpoints manually
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/status
```

**Common Causes and Solutions:**

#### 1. Backend API Not Ready

**Error:** Health endpoint returns 503 or connection refused

**Solution:**
```bash
# Check backend logs
make logs-backend

# Verify backend is listening
docker-compose exec backend-api netstat -tlnp | grep 8000

# Check if dependencies are ready
curl http://localhost:8000/health/db
curl http://localhost:8000/health/bedrock

# Increase health check start period
# Edit docker-compose.yml:
# healthcheck:
#   start_period: 60s  # Increase from 40s
```

#### 2. DynamoDB Not Initialized

**Error:** `/health/db` returns error about missing tables

**Solution:**
```bash
# Check DynamoDB is running
docker-compose ps dynamodb-local

# Initialize tables manually
make init-db

# Verify tables exist
aws dynamodb list-tables --endpoint-url http://localhost:8001

# Check table creation logs
docker-compose logs dynamodb-local
```

#### 3. Network Issues Between Containers

**Error:** Backend can't reach DynamoDB or LocalStack

**Solution:**
```bash
# Test inter-container connectivity
docker-compose exec backend-api ping dynamodb-local
docker-compose exec backend-api curl http://dynamodb-local:8001

# Check network configuration
docker network inspect vibegraph_vibegraph-network

# Recreate network
make down
docker network prune
make up
```

#### 4. Health Check Configuration Too Strict

**Solution:**
```bash
# Edit docker-compose.yml to relax health checks:
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s      # Increase timeout
  retries: 5        # Increase retries
  start_period: 60s # Increase start period
```

### Intermittent Health Check Failures

**Symptoms:**
- Health checks pass sometimes, fail other times
- Containers marked unhealthy then healthy repeatedly

**Diagnosis:**
```bash
# Monitor health checks in real-time
watch -n 5 'docker ps --format "table {{.Names}}\t{{.Status}}"'

# Check for resource constraints
docker stats

# Review health check logs
docker inspect vibegraph-backend-api | jq '.[0].State.Health.Log'
```

**Solutions:**

#### 1. Resource Constraints

```bash
# Increase container resources in docker-compose.yml:
services:
  backend-api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

#### 2. Slow Dependencies

```bash
# Add retry logic to health checks
# Edit backend/api/health.py:
@app.get("/health/db")
async def health_db():
    for attempt in range(3):
        try:
            client.list_tables()
            return {"status": "healthy"}
        except Exception as e:
            if attempt == 2:
                raise
            await asyncio.sleep(1)
```

## Connection Timeouts

### Frontend Can't Reach Backend

**Symptoms:**
- Frontend shows "Network Error" or "Failed to fetch"
- Browser console shows CORS errors
- API requests timeout

**Diagnosis:**
```bash
# Test backend from host
curl http://localhost:8000/health

# Test from frontend container
docker-compose exec frontend curl http://backend-api:8000/health

# Check frontend environment
docker-compose exec frontend env | grep API

# Check browser network tab for errors
```

**Solutions:**

#### 1. Incorrect API URL

**Solution:**
```bash
# Verify frontend environment variable
cat frontend/.env
# Should contain: VITE_API_BASE_URL=http://localhost:8000

# For container-to-container:
# VITE_API_BASE_URL=http://backend-api:8000

# Rebuild frontend after changing .env
docker-compose build frontend
docker-compose up -d frontend
```

#### 2. CORS Configuration Issues

**Error:** `Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' has been blocked by CORS policy`

**Solution:**
```bash
# Check CORS configuration in backend/api/main.py
docker-compose exec backend-api cat api/main.py | grep -A 10 CORS

# Verify CORS headers
curl -H "Origin: http://localhost:3000" \
     -H "Access-Control-Request-Method: POST" \
     -X OPTIONS \
     http://localhost:8000/api/quiz/section1/start -v

# Update CORS configuration if needed
# Edit backend/api/main.py:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 3. Network Connectivity Issues

**Solution:**
```bash
# Test network connectivity
docker-compose exec frontend ping backend-api

# Check DNS resolution
docker-compose exec frontend nslookup backend-api

# Verify network configuration
docker network inspect vibegraph_vibegraph-network

# Restart networking
make down
make up
```

### Backend Can't Reach DynamoDB

**Symptoms:**
- `/health/db` returns error
- API operations fail with database errors
- Logs show connection timeouts

**Diagnosis:**
```bash
# Test DynamoDB from backend
docker-compose exec backend-api curl http://dynamodb-local:8001

# Check DynamoDB is running
docker-compose ps dynamodb-local

# Test with AWS CLI
aws dynamodb list-tables --endpoint-url http://localhost:8001
```

**Solutions:**

#### 1. DynamoDB Not Running

```bash
# Start DynamoDB
docker-compose up -d dynamodb-local

# Wait for it to be ready
make wait-healthy

# Verify it's accessible
curl http://localhost:8001
```

#### 2. Incorrect Endpoint Configuration

```bash
# Check backend environment
docker-compose exec backend-api env | grep DYNAMODB

# Should be: DYNAMODB_ENDPOINT=http://dynamodb-local:8001

# Update if incorrect in docker-compose.yml or .env
# Restart backend
docker-compose restart backend-api
```

#### 3. Network Issues

```bash
# Test connectivity
docker-compose exec backend-api ping dynamodb-local

# Check if DynamoDB port is exposed
docker-compose exec backend-api nc -zv dynamodb-local 8001

# Recreate containers
make down
make up
```

### Backend Can't Reach Bedrock (LocalStack)

**Symptoms:**
- `/health/bedrock` returns error
- Quiz generation fails
- Logs show Bedrock connection errors

**Diagnosis:**
```bash
# Test LocalStack from backend
docker-compose exec backend-api curl http://localstack:4566/_localstack/health

# Check LocalStack is running
docker-compose ps localstack

# View LocalStack logs
docker-compose logs localstack
```

**Solutions:**

#### 1. LocalStack Not Ready

```bash
# Wait for LocalStack to initialize
docker-compose logs localstack | grep "Ready"

# Restart LocalStack
docker-compose restart localstack

# Increase start period in docker-compose.yml
```

#### 2. Bedrock Service Not Configured

```bash
# Check LocalStack services
curl http://localhost:4566/_localstack/health

# Configure Bedrock in LocalStack (if needed)
# LocalStack Pro may be required for Bedrock
```

## Database Issues

### Tables Not Created

**Symptoms:**
- API returns "Table not found" errors
- `/health/db` fails
- DynamoDB operations fail

**Diagnosis:**
```bash
# List tables
aws dynamodb list-tables --endpoint-url http://localhost:8001

# Check initialization logs
docker-compose logs backend-api | grep -i "table"
```

**Solutions:**

#### 1. Initialization Script Didn't Run

```bash
# Run initialization manually
make init-db

# Or run script directly
docker-compose exec backend-api python scripts/init-dynamodb.py

# Verify tables created
aws dynamodb list-tables --endpoint-url http://localhost:8001
```

#### 2. DynamoDB Data Corrupted

```bash
# Remove DynamoDB volume
make down
docker volume rm vibegraph_dynamodb-data

# Restart and reinitialize
make up
make init-db
```

### Can't Write to Database

**Symptoms:**
- API returns 500 errors on write operations
- Logs show "ProvisionedThroughputExceededException"

**Diagnosis:**
```bash
# Check table configuration
aws dynamodb describe-table \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8001

# Check for errors in logs
make logs-backend | grep -i dynamodb
```

**Solutions:**

#### 1. Table Configuration Issues

```bash
# Recreate tables with correct configuration
docker-compose exec backend-api python scripts/init-dynamodb.py --reset

# Verify billing mode is on-demand
aws dynamodb describe-table \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8001 \
  | jq '.Table.BillingModeSummary'
```

#### 2. Permission Issues

```bash
# Check AWS credentials (for production)
docker-compose exec backend-api env | grep AWS

# For local development, credentials shouldn't be needed
# Verify DYNAMODB_ENDPOINT points to local instance
```

## API Errors

### 500 Internal Server Error

**Symptoms:**
- API returns 500 for all requests
- Specific endpoints fail consistently

**Diagnosis:**
```bash
# Check backend logs
make logs-backend

# Test specific endpoint
curl -X POST http://localhost:8000/api/quiz/section1/start -v

# Check health status
curl http://localhost:8000/health/status | jq
```

**Solutions:**

#### 1. Application Error

```bash
# View detailed error logs
docker-compose logs backend-api | grep -A 20 "ERROR"

# Check Python traceback
docker-compose logs backend-api | grep -A 50 "Traceback"

# Fix code error and restart
docker-compose restart backend-api
```

#### 2. Missing Dependencies

```bash
# Check if all dependencies are installed
docker-compose exec backend-api pip list

# Reinstall dependencies
docker-compose exec backend-api pip install -r requirements.txt

# Or rebuild container
docker-compose build backend-api
docker-compose up -d backend-api
```

### 404 Not Found

**Symptoms:**
- API returns 404 for valid endpoints
- Routes not registered

**Diagnosis:**
```bash
# Check registered routes
curl http://localhost:8000/docs

# View route registration logs
docker-compose logs backend-api | grep -i "route"
```

**Solutions:**

#### 1. Routes Not Registered

```bash
# Check route registration in backend/api/main.py
docker-compose exec backend-api cat api/main.py | grep include_router

# Verify route files exist
docker-compose exec backend-api ls -la api/routes/
```

#### 2. Incorrect URL Path

```bash
# Check API documentation
open http://localhost:8000/docs

# Verify correct path format:
# /api/quiz/section1/start (not /quiz/section1/start)
```

### 401 Unauthorized

**Symptoms:**
- API returns 401 for authenticated endpoints
- Token validation fails

**Diagnosis:**
```bash
# Check if token is being sent
# In browser DevTools → Network → Headers

# Test without authentication (if endpoint should be public)
curl http://localhost:8000/api/quiz/section1/start
```

**Solutions:**

#### 1. Missing or Invalid Token

```bash
# Check token format in request
# Should be: Authorization: Bearer <token>

# Verify JWT secret is configured
docker-compose exec backend-api env | grep JWT_SECRET

# Check token validation logic
docker-compose logs backend-api | grep -i "auth"
```

#### 2. Token Expired

```bash
# Generate new token
# (Implementation depends on your auth system)

# Check token expiration time
# Decode JWT at jwt.io
```

## Frontend Issues

### Blank Page

**Symptoms:**
- Browser shows blank white page
- No errors in console
- React app doesn't load

**Diagnosis:**
```bash
# Check frontend logs
make logs-frontend

# Check browser console for errors
# Open DevTools → Console

# Verify frontend is running
curl http://localhost:3000
```

**Solutions:**

#### 1. Build Errors

```bash
# Check for build errors
docker-compose logs frontend | grep -i error

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend

# Check if files are being served
curl http://localhost:3000/index.html
```

#### 2. JavaScript Errors

```bash
# Check browser console for errors
# Common issues:
# - Module not found
# - Syntax errors
# - Import errors

# Rebuild with clean cache
docker-compose build --no-cache frontend
```

#### 3. Environment Variables Not Loaded

```bash
# Verify environment variables
docker-compose exec frontend env | grep VITE

# Rebuild after changing .env
docker-compose build frontend
docker-compose up -d frontend
```

### Components Not Rendering

**Symptoms:**
- Specific components don't appear
- Console shows component errors

**Diagnosis:**
```bash
# Check browser console
# Look for React errors

# Check frontend logs
make logs-frontend

# Verify component files exist
docker-compose exec frontend ls -la src/components/
```

**Solutions:**

#### 1. Import Errors

```bash
# Check import paths in browser console
# Fix import statements in code

# Restart frontend
docker-compose restart frontend
```

#### 2. API Data Issues

```bash
# Check if API is returning data
curl http://localhost:8000/api/quiz/section1/start

# Check network tab in browser DevTools
# Verify API responses are correct format
```

## Performance Issues

### Slow Response Times

**Symptoms:**
- API requests take >2 seconds
- Frontend feels sluggish
- Health checks timeout

**Diagnosis:**
```bash
# Check container resource usage
docker stats

# Check response times
time curl http://localhost:8000/health

# Monitor logs for slow operations
docker-compose logs backend-api | grep -i "duration"
```

**Solutions:**

#### 1. Resource Constraints

```bash
# Increase Docker resources
# Docker Desktop → Settings → Resources
# Set Memory to 8GB+, CPUs to 4+

# Increase container limits in docker-compose.yml
services:
  backend-api:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '2'
```

#### 2. Database Performance

```bash
# Check DynamoDB performance
docker stats vibegraph-dynamodb-local

# Optimize queries
# Add indexes if needed
# Use batch operations
```

#### 3. Too Many Logs

```bash
# Reduce log level
# Edit docker-compose.yml:
environment:
  LOG_LEVEL: warning  # Change from debug

# Restart services
docker-compose restart
```

### High Memory Usage

**Symptoms:**
- Containers using >1GB memory
- System becomes slow
- Out of memory errors

**Diagnosis:**
```bash
# Check memory usage
docker stats --no-stream

# Check for memory leaks
docker stats --format "table {{.Name}}\t{{.MemUsage}}"
```

**Solutions:**

#### 1. Memory Leaks

```bash
# Restart containers
make restart

# Monitor memory over time
watch -n 5 'docker stats --no-stream'

# If memory keeps growing, check application code for leaks
```

#### 2. Too Many Containers

```bash
# Stop unused containers
docker stop $(docker ps -aq)

# Remove unused containers
docker container prune

# Remove unused images
docker image prune -a
```

## Diagnostic Commands

### Container Status

```bash
# List all containers
docker-compose ps

# Show container health
docker ps --format "table {{.Names}}\t{{.Status}}"

# Inspect specific container
docker inspect vibegraph-backend-api

# View container resource usage
docker stats
```

### Logs

```bash
# View all logs
make logs

# View specific service logs
make logs-backend
make logs-frontend

# Follow logs in real-time
docker-compose logs -f backend-api

# Search logs for errors
docker-compose logs backend-api | grep -i error

# View last 100 lines
docker-compose logs --tail=100 backend-api
```

### Network

```bash
# List networks
docker network ls

# Inspect network
docker network inspect vibegraph_vibegraph-network

# Test connectivity between containers
docker-compose exec frontend ping backend-api
docker-compose exec backend-api ping dynamodb-local

# Check DNS resolution
docker-compose exec backend-api nslookup dynamodb-local

# Test port connectivity
docker-compose exec backend-api nc -zv dynamodb-local 8001
```

### Health Checks

```bash
# Check all health statuses
make health

# Test individual health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/db
curl http://localhost:8000/health/bedrock
curl http://localhost:8000/health/status | jq

# Wait for healthy state
make wait-healthy

# Monitor health continuously
make monitor
```

### Database

```bash
# List DynamoDB tables
aws dynamodb list-tables --endpoint-url http://localhost:8001

# Describe table
aws dynamodb describe-table \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8001

# Scan table
aws dynamodb scan \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8001

# Count items
aws dynamodb scan \
  --table-name vibegraph-users \
  --select COUNT \
  --endpoint-url http://localhost:8001
```

### System Resources

```bash
# Check Docker disk usage
docker system df

# Check Docker info
docker info

# Check host resources
free -h  # Memory
df -h    # Disk
top      # CPU and processes
```

### Cleanup

```bash
# Stop all containers
make down

# Remove all containers and volumes
make clean

# Remove unused Docker resources
docker system prune -a --volumes

# Remove specific volume
docker volume rm vibegraph_dynamodb-data

# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune -a
```

## Getting More Help

If you can't resolve the issue:

1. **Gather Information:**
   ```bash
   # Collect diagnostic information
   make health > health-status.txt
   make logs > logs.txt
   docker ps > containers.txt
   docker stats --no-stream > stats.txt
   ```

2. **Check Documentation:**
   - [Development Guide](./DEVELOPMENT.md)
   - [Docker Setup](./infrastructure/docker-setup.md)
   - [API Documentation](./api/README.md)

3. **Search Issues:**
   - Check GitHub issues for similar problems
   - Search error messages online

4. **Ask for Help:**
   - Open a GitHub issue with diagnostic information
   - Include logs, error messages, and steps to reproduce
   - Mention your OS, Docker version, and system specs

## Common Error Messages

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| `port is already allocated` | Port conflict | Kill process using port or change port |
| `no such file or directory` | Missing file or incorrect path | Check file exists and path is correct |
| `permission denied` | File permission issue | Fix permissions with chmod/chown |
| `connection refused` | Service not running | Start service and check health |
| `network not found` | Docker network issue | Recreate network with `make down && make up` |
| `table not found` | DynamoDB not initialized | Run `make init-db` |
| `CORS policy` | CORS misconfiguration | Update CORS settings in backend |
| `out of memory` | Insufficient Docker memory | Increase Docker memory allocation |
| `timeout` | Service taking too long | Check logs, increase timeout, or check resources |
| `unhealthy` | Health check failing | Check health endpoint and dependencies |

---

**Last Updated**: [Date]  
**Version**: 1.0.0

For additional support, see [DEVELOPMENT.md](./DEVELOPMENT.md) or contact the development team.
