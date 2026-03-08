# Docker Compose Configuration

## Overview

The `docker-compose.yml` file orchestrates all VibeGraph services in a containerized environment. It defines 7 services that work together to provide the complete VibeGraph backend integration.

## Services

### 1. Frontend (vibegraph-frontend)

**Purpose**: Serves the React application using nginx

**Configuration**:
- Build: `./frontend/Dockerfile`
- Port: `3000:3000`
- Network: vibegraph-network
- Health check: HTTP GET to `http://localhost:3000`

**Environment Variables**:
- `VITE_API_URL`: Points to backend-api service

**Volumes**:
- Source code mounted for hot reload (development)

**Dependencies**:
- Waits for backend-api to be healthy

---

### 2. Backend API (vibegraph-backend-api)

**Purpose**: FastAPI gateway for all backend operations

**Configuration**:
- Build: `./backend/api/Dockerfile`
- Port: `8000:8000`
- Network: vibegraph-network
- Health check: HTTP GET to `http://localhost:8000/health`

**Environment Variables**:
- AWS credentials and region
- DynamoDB endpoint and table names
- Bedrock endpoint and model names
- Logging configuration

**Volumes**:
- Source code mounted for hot reload
- Shared logs directory

**Dependencies**:
- Waits for dynamodb-local to be healthy
- Waits for localstack to be healthy

---

### 3. Backend Handlers (vibegraph-backend-handlers)

**Purpose**: Lambda function handlers for quiz and profile operations

**Configuration**:
- Build: `./backend/handlers/Dockerfile`
- Network: vibegraph-network
- No exposed ports (internal service)

**Environment Variables**:
- Same as backend-api
- Additional PYTHONPATH configuration

**Volumes**:
- Source code mounted for hot reload
- Shared logs directory

**Dependencies**:
- Waits for backend-services to start
- Waits for dynamodb-local to be healthy
- Waits for localstack to be healthy

---

### 4. Backend Services (vibegraph-backend-services)

**Purpose**: Shared service layer for DynamoDB, Bedrock, and caching

**Configuration**:
- Build: `./backend/services/Dockerfile`
- Network: vibegraph-network
- No exposed ports (internal service)

**Environment Variables**:
- AWS credentials and region
- DynamoDB endpoint and table names
- Bedrock endpoint
- Logging configuration

**Volumes**:
- Source code mounted for hot reload
- Shared logs directory

**Dependencies**:
- Waits for dynamodb-local to be healthy

---

### 5. DynamoDB Local (vibegraph-dynamodb-local)

**Purpose**: Local DynamoDB instance for development

**Configuration**:
- Image: `amazon/dynamodb-local:latest`
- Port: `8001:8000` (mapped to 8001 to avoid conflict)
- Network: vibegraph-network
- Health check: HTTP GET to `http://localhost:8000`

**Command**:
```bash
-jar DynamoDBLocal.jar -sharedDb -dbPath /data
```

**Volumes**:
- Named volume `dynamodb-data` for persistence

**Notes**:
- Accessible inside network at `http://dynamodb-local:8000`
- Accessible from host at `http://localhost:8001`

---

### 6. DynamoDB Init (vibegraph-dynamodb-init)

**Purpose**: Initialize DynamoDB tables on first startup

**Configuration**:
- Build: `./backend/scripts/Dockerfile.init`
- Network: vibegraph-network
- Restart: "no" (runs once)

**Environment Variables**:
- DynamoDB endpoint and credentials
- Table names

**Dependencies**:
- Waits for dynamodb-local to be healthy

**Notes**:
- Runs the `init-dynamodb.py` script
- Creates Users, Sessions, and EmbeddingCache tables
- Exits after completion

---

### 7. LocalStack (vibegraph-localstack)

**Purpose**: Mock AWS Bedrock services for development

**Configuration**:
- Image: `localstack/localstack:latest`
- Ports: `4566:4566`, `4571:4571`
- Network: vibegraph-network
- Health check: HTTP GET to `http://localhost:4566/_localstack/health`

**Environment Variables**:
- SERVICES=bedrock
- DEBUG=1
- AWS credentials and region

**Volumes**:
- Named volume `localstack-data` for persistence
- Docker socket for container management

---

## Network Configuration

### vibegraph-network

**Type**: Bridge network

**Purpose**: Isolates all VibeGraph services in a dedicated network

**DNS Resolution**: All services can reach each other by service name:
- `http://frontend:3000`
- `http://backend-api:8000`
- `http://dynamodb-local:8000`
- `http://localstack:4566`

---

## Volume Configuration

### Named Volumes

**dynamodb-data**:
- Purpose: Persist DynamoDB tables across container restarts
- Mount: `/data` in dynamodb-local container

**localstack-data**:
- Purpose: Persist LocalStack state
- Mount: `/tmp/localstack` in localstack container

### Bind Mounts

**Source Code (Development)**:
- Frontend: `./frontend/src`, `./frontend/public`
- Backend API: `./backend/api`, `./backend/src`, `./prompts`
- Backend Handlers: `./backend/handlers`, `./backend/src`, `./prompts`
- Backend Services: `./backend/services`, `./backend/src`

**Shared Logs**:
- `./logs:/app/logs` (mounted in all backend services)

---

## Health Checks

All HTTP services have health checks configured:

**Configuration**:
- Interval: 30 seconds
- Timeout: 10 seconds
- Retries: 3
- Start period: 40 seconds

**Endpoints**:
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000/health`
- DynamoDB Local: `http://localhost:8000`
- LocalStack: `http://localhost:4566/_localstack/health`

---

## Restart Policies

All services use `restart: unless-stopped` except:
- **dynamodb-init**: `restart: "no"` (runs once)

This ensures:
- Automatic restart on failure
- Restart after system reboot
- Manual stop prevents auto-restart

---

## Startup Order

The dependency chain ensures proper startup order:

```
1. dynamodb-local (starts and becomes healthy)
2. localstack (starts and becomes healthy)
3. dynamodb-init (runs once to create tables)
4. backend-services (starts)
5. backend-handlers (starts)
6. backend-api (starts and becomes healthy)
7. frontend (starts)
```

---

## Usage

### Start all services
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend-api
```

### Check service status
```bash
docker-compose ps
```

### Stop all services
```bash
docker-compose down
```

### Stop and remove volumes
```bash
docker-compose down -v
```

### Rebuild services
```bash
docker-compose up -d --build
```

### Restart a specific service
```bash
docker-compose restart backend-api
```

### View service health
```bash
docker-compose ps
# Look for "healthy" status in the State column
```

---

## Environment Variables

### Frontend
- `VITE_API_URL`: Backend API URL (default: http://backend-api:8000)

### Backend Services
- `AWS_REGION`: AWS region (default: us-east-1)
- `AWS_ACCESS_KEY_ID`: AWS access key (default: test)
- `AWS_SECRET_ACCESS_KEY`: AWS secret key (default: test)
- `DYNAMODB_ENDPOINT`: DynamoDB endpoint (default: http://dynamodb-local:8000)
- `BEDROCK_ENDPOINT`: Bedrock endpoint (default: http://localstack:4566)
- `USERS_TABLE`: Users table name (default: vibegraph-users)
- `SESSIONS_TABLE`: Sessions table name (default: vibegraph-sessions)
- `CACHE_TABLE`: Cache table name (default: vibegraph-embedding-cache)
- `CLAUDE_MODEL`: Claude model ID
- `TITAN_MODEL`: Titan model ID
- `LOG_LEVEL`: Logging level (default: INFO)

---

## Troubleshooting

### Service won't start
1. Check logs: `docker-compose logs <service-name>`
2. Verify dependencies are healthy: `docker-compose ps`
3. Check health check endpoint manually

### Port conflicts
- Frontend: Change `3000:3000` to `<new-port>:3000`
- Backend API: Change `8000:8000` to `<new-port>:8000`
- DynamoDB: Already mapped to 8001 to avoid conflicts

### Volume permission issues
```bash
# Fix permissions on logs directory
sudo chown -R $USER:$USER ./logs
```

### DynamoDB tables not created
```bash
# Manually run init script
docker-compose run --rm dynamodb-init
```

### Health checks failing
```bash
# Check if service is responding
curl http://localhost:8000/health  # Backend API
curl http://localhost:3000         # Frontend
curl http://localhost:8001         # DynamoDB
curl http://localhost:4566/_localstack/health  # LocalStack
```

### Hot reload not working
1. Verify volume mounts in docker-compose.yml
2. Check file permissions
3. Restart the service: `docker-compose restart <service-name>`

---

## Development vs Production

### Development Mode (Current Configuration)
- Source code mounted as volumes for hot reload
- Debug logging enabled
- LocalStack for mock AWS services
- DynamoDB Local for database

### Production Mode (Future)
- Remove volume mounts
- Use production builds
- Connect to real AWS services
- Use production DynamoDB
- Disable debug logging
- Add authentication and security

---

## Security Notes

### Development Credentials
The current configuration uses test credentials:
- AWS_ACCESS_KEY_ID=test
- AWS_SECRET_ACCESS_KEY=test

**⚠️ WARNING**: Never use these credentials in production!

### Production Recommendations
1. Use AWS IAM roles for authentication
2. Store secrets in AWS Secrets Manager
3. Use environment-specific configuration files
4. Enable HTTPS/TLS for all services
5. Implement proper CORS restrictions
6. Use production-grade databases

---

## Performance Optimization

### Build Cache
Docker Compose uses build cache to speed up rebuilds:
- Only changed layers are rebuilt
- Dependencies are cached in separate layers

### Volume Performance
- Use named volumes for better performance
- Avoid mounting large directories in development

### Resource Limits
Add resource limits in production:
```yaml
services:
  backend-api:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

---

## Monitoring

### Health Status
```bash
# Watch health status
watch -n 5 'docker-compose ps'
```

### Resource Usage
```bash
# View resource usage
docker stats
```

### Logs
```bash
# Follow logs with timestamps
docker-compose logs -f --timestamps

# Filter logs by service
docker-compose logs -f backend-api backend-handlers
```

---

## Related Documentation

- [Docker Setup Guide](./docker-setup.md)
- [Networking Configuration](./networking.md)
- [Environment Configuration](./environment.md)
- [Makefile Commands](./makefile.md)
