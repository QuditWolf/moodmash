# Docker Setup Guide

## Overview

This guide covers the Docker containerization setup for the VibeGraph application. The system uses Docker containers to isolate the frontend, backend services, and supporting infrastructure, enabling consistent development and deployment environments.

## Prerequisites

- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher
- 8 GB RAM minimum (16 GB recommended)
- 10 GB free disk space

## Container Architecture

The VibeGraph application consists of 5 Docker containers:

1. **frontend** - React application with Vite dev server
2. **backend-api** - API Gateway and Lambda function runtime
3. **backend-services** - AWS Bedrock mock services (Claude + Titan)
4. **dynamodb-local** - Local DynamoDB instance
5. **localstack** - AWS service mocking (S3, CloudWatch, Secrets Manager)

## Container Specifications

### Frontend Container

**Purpose**: Serve React application with hot module replacement

**Base Image**: `node:18-alpine`

**Ports**:
- `5173` - Vite dev server (mapped to host)

**Environment Variables**:
```env
VITE_VIBEGRAPH_API_URL=http://backend-api:3000
VITE_ENV=development
NODE_ENV=development
```

**Volume Mounts**:
- `./frontend:/app` - Source code with hot reload
- `/app/node_modules` - Anonymous volume for dependencies

**Health Check**:
```yaml
test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:5173"]
interval: 10s
timeout: 5s
retries: 3
start_period: 20s
```

### Backend API Container

**Purpose**: Run Lambda functions locally with API Gateway emulation

**Base Image**: `amazon/aws-sam-cli-emulation-image-nodejs18.x`

**Ports**:
- `3000` - API Gateway endpoints
- `9229` - Node.js debugger

**Environment Variables**:
```env
AWS_REGION=us-east-1
DYNAMODB_ENDPOINT=http://dynamodb-local:8000
LOCALSTACK_ENDPOINT=http://localstack:4566
BEDROCK_ENDPOINT=http://backend-services:8080
SESSIONS_TABLE=vibegraph-sessions
USERS_TABLE=vibegraph-users
CACHE_TABLE=vibegraph-embedding-cache
LOG_LEVEL=debug
```

**Volume Mounts**:
- `./backend/src:/var/task/src` - Lambda function code
- `./backend/infrastructure/template.yaml:/var/task/template.yaml:ro` - SAM template

**Health Check**:
```yaml
test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
interval: 10s
timeout: 5s
retries: 5
start_period: 30s
```

### Backend Services Container

**Purpose**: Mock AWS Bedrock services for local development

**Base Image**: `python:3.11-slim`

**Ports**:
- `8080` - Bedrock mock API (internal only)

**Environment Variables**:
```env
BEDROCK_REGION=us-east-1
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
TITAN_MODEL=amazon.titan-embed-text-v2:0
MOCK_MODE=true
```

**Volume Mounts**:
- `./backend/mocks/bedrock:/app` - Mock service implementation
- `./backend/mocks/responses:/app/responses` - Pre-generated responses

**Health Check**:
```yaml
test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
interval: 10s
timeout: 5s
retries: 3
start_period: 15s
```

### DynamoDB Local Container

**Purpose**: Local DynamoDB instance for data persistence

**Base Image**: `amazon/dynamodb-local:latest`

**Ports**:
- `8000` - DynamoDB API

**Command**:
```bash
-jar DynamoDBLocal.jar -sharedDb -dbPath /data
```

**Volume Mounts**:
- `dynamodb-data:/data` - Persistent data storage (named volume)
- `./backend/infrastructure/dynamodb:/docker-entrypoint-initdb.d:ro` - Table schemas

**Health Check**:
```yaml
test: ["CMD-SHELL", "curl -f http://localhost:8000 || exit 1"]
interval: 10s
timeout: 5s
retries: 3
start_period: 10s
```

### LocalStack Container

**Purpose**: Mock AWS services for local development

**Base Image**: `localstack/localstack:latest`

**Ports**:
- `4566` - LocalStack gateway

**Environment Variables**:
```env
SERVICES=s3,cloudwatch,secretsmanager,logs
DEBUG=1
DATA_DIR=/tmp/localstack/data
AWS_DEFAULT_REGION=us-east-1
```

**Volume Mounts**:
- `localstack-data:/tmp/localstack` - Persistent service data
- `/var/run/docker.sock:/var/run/docker.sock:ro` - Docker socket
- `./backend/scripts/localstack-init.sh:/docker-entrypoint-initaws.d/init.sh:ro` - Init script

**Health Check**:
```yaml
test: ["CMD", "curl", "-f", "http://localhost:4566/_localstack/health"]
interval: 10s
timeout: 5s
retries: 5
start_period: 20s
```

## Dockerfile Structure

### Frontend Dockerfile

**Development**:
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Expose Vite dev server port
EXPOSE 5173

# Start dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
```

**Production** (Multi-stage):
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Backend API Dockerfile

```dockerfile
FROM amazon/aws-sam-cli-emulation-image-nodejs18.x

WORKDIR /var/task

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy Lambda functions and infrastructure
COPY src/ ./src/
COPY infrastructure/ ./infrastructure/

# Expose API Gateway and debugger ports
EXPOSE 3000 9229

# Start SAM local API
CMD ["sam", "local", "start-api", "--host", "0.0.0.0", "--port", "3000"]
```

### Backend Services Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mock service code
COPY . .

# Expose Bedrock mock API port
EXPOSE 8080

# Start mock service
CMD ["python", "server.py"]
```

## Docker Ignore Files

### Frontend .dockerignore

```
node_modules
dist
.env
.env.local
.env.*.local
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
.vscode
.idea
*.swp
*.swo
coverage
.cache
```

### Backend .dockerignore

```
node_modules
__pycache__
*.pyc
.env
.env.local
.pytest_cache
.coverage
dist
build
*.log
.DS_Store
.vscode
.idea
*.swp
*.swo
```

## Building Images

### Build All Images

```bash
docker-compose build
```

### Build Specific Image

```bash
docker-compose build frontend
docker-compose build backend-api
```

### Build with No Cache

```bash
docker-compose build --no-cache
```

### Build for Production

```bash
docker build -f frontend/Dockerfile.prod -t vibegraph-frontend:latest ./frontend
```

## Running Containers

### Start All Containers

```bash
docker-compose up
```

### Start in Detached Mode

```bash
docker-compose up -d
```

### Start with Build

```bash
docker-compose up --build
```

### Start Specific Container

```bash
docker-compose up frontend
```

### Stop All Containers

```bash
docker-compose down
```

### Stop and Remove Volumes

```bash
docker-compose down -v
```

## Container Management

### View Running Containers

```bash
docker-compose ps
```

### View Container Logs

```bash
# All containers
docker-compose logs -f

# Specific container
docker-compose logs -f backend-api

# Last 100 lines
docker-compose logs --tail=100 frontend
```

### Restart Container

```bash
docker-compose restart backend-api
```

### Execute Command in Container

```bash
docker-compose exec backend-api sh
docker-compose exec frontend npm run test
```

### View Resource Usage

```bash
docker stats
```

## Volume Management

### Named Volumes

**dynamodb-data**:
- Purpose: Persist DynamoDB tables across restarts
- Location: Docker managed volume
- Backup: `aws dynamodb scan --endpoint-url http://localhost:8000 > backup.json`

**localstack-data**:
- Purpose: Persist LocalStack service data
- Location: Docker managed volume
- Backup: `awslocal s3 sync s3://bucket ./backup`

### List Volumes

```bash
docker volume ls
```

### Inspect Volume

```bash
docker volume inspect vibegraph_dynamodb-data
```

### Remove Volume

```bash
docker volume rm vibegraph_dynamodb-data
```

### Remove All Unused Volumes

```bash
docker volume prune
```

## Resource Limits

### Default Allocation

| Container | CPU Limit | Memory Limit | CPU Reserve | Memory Reserve |
|-----------|-----------|--------------|-------------|----------------|
| frontend | 1.0 | 1 GB | 0.5 | 512 MB |
| backend-api | 2.0 | 2 GB | 1.0 | 1 GB |
| backend-services | 1.0 | 1 GB | 0.5 | 512 MB |
| dynamodb-local | 0.5 | 512 MB | 0.25 | 256 MB |
| localstack | 1.0 | 1 GB | 0.5 | 512 MB |

### Adjust Limits

Edit `docker-compose.yml`:

```yaml
services:
  backend-api:
    deploy:
      resources:
        limits:
          cpus: '3.0'
          memory: 4G
        reservations:
          cpus: '1.5'
          memory: 2G
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs [service-name]

# Check health status
docker-compose ps

# Rebuild container
docker-compose up --build --force-recreate [service-name]
```

### Port Already in Use

```bash
# Find process using port
lsof -i :5173

# Kill process
kill -9 [PID]

# Or change port in docker-compose.yml
```

### Out of Memory

```bash
# Check Docker memory limit
docker info | grep Memory

# Increase Docker memory in Docker Desktop settings
# Or reduce container memory limits in docker-compose.yml
```

### Permission Denied on Volume

```bash
# Fix permissions on bind mount
chmod -R 755 ./frontend
chmod -R 755 ./backend
```

### Health Check Failing

```bash
# Check container logs
docker-compose logs [service-name]

# Manually test health endpoint
docker-compose exec [service-name] curl http://localhost:[port]/health

# Verify dependencies are healthy
docker-compose ps
```

## Best Practices

### Development

1. **Use bind mounts** for source code to enable hot reload
2. **Use named volumes** for dependencies (node_modules)
3. **Enable debug ports** for debugging (9229 for Node.js)
4. **Use verbose logging** (LOG_LEVEL=debug)
5. **Keep containers running** with `restart: unless-stopped`

### Production

1. **Use multi-stage builds** to minimize image size
2. **Run as non-root user** for security
3. **Use read-only file systems** where possible
4. **Remove dev dependencies** from final image
5. **Use specific image tags** instead of `latest`
6. **Enable health checks** for all containers
7. **Set resource limits** to prevent resource exhaustion

### Security

1. **Never commit secrets** to version control
2. **Use environment variables** for configuration
3. **Rotate JWT secrets** regularly in production
4. **Use AWS IAM roles** instead of access keys in production
5. **Enable TLS/HTTPS** for all external endpoints
6. **Restrict CORS** to specific domains in production
7. **Keep base images updated** to patch vulnerabilities

## Performance Optimization

### Build Optimization

1. **Order Dockerfile commands** from least to most frequently changed
2. **Combine RUN commands** to reduce layers
3. **Use .dockerignore** to exclude unnecessary files
4. **Leverage build cache** by copying package.json before source code
5. **Use Alpine images** for smaller size

### Runtime Optimization

1. **Use provisioned concurrency** for Lambda functions
2. **Implement caching** for expensive operations
3. **Use connection pooling** for database connections
4. **Enable compression** for API responses
5. **Monitor resource usage** with `docker stats`

## Next Steps

- See [docker-compose.md](./docker-compose.md) for orchestration details
- See [networking.md](./networking.md) for container communication
- See [makefile.md](./makefile.md) for convenient build commands
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [AWS SAM Local](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-start-api.html)
