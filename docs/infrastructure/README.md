# Infrastructure Documentation

## Overview

This documentation covers the infrastructure setup, deployment, and operations for the VibeGraph application. The system uses Docker containerization with Docker Compose orchestration to provide a consistent development and deployment environment.

## Quick Start

```bash
# Build all containers
make build

# Start all services
make up

# Wait for services to be healthy
make wait-healthy

# Check health status
make health

# View logs
make logs
```

## Architecture

The VibeGraph infrastructure consists of 5 Docker containers orchestrated by Docker Compose:

```
┌─────────────────────────────────────────────────────────┐
│                    Docker Network                        │
│                  (vibegraph-network)                     │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ Frontend │  │ Backend  │  │ DynamoDB │             │
│  │  :3000   │─▶│   :8000  │─▶│  :8001   │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                      │                                   │
│                      ▼                                   │
│                ┌──────────┐                             │
│                │LocalStack│                             │
│                │  :4566   │                             │
│                └──────────┘                             │
└─────────────────────────────────────────────────────────┘
```

### Container Roles

1. **Frontend Container** - React application with Vite dev server
2. **Backend API Container** - FastAPI application with Lambda handlers
3. **DynamoDB Local Container** - Local DynamoDB instance for data storage
4. **LocalStack Container** - Mock AWS services (Bedrock, S3, CloudWatch)

## Documentation Index

### Setup and Configuration

- [Docker Setup Guide](./docker-setup.md) - Detailed Docker configuration and Dockerfile documentation
- [Docker Compose Guide](./docker-compose.md) - Service orchestration and networking
- [Environment Configuration](./environment.md) - Environment variables and configuration files
- [Makefile Commands](./makefile.md) - Build and management commands
- [Optimization Guide](./optimization.md) - Docker image and build optimization strategies

### Operations

- [Networking Guide](./networking.md) - Container communication and DNS resolution
- [Logging Guide](./logging.md) - Structured logging and log aggregation
- [Deployment Guide](./DEPLOYMENT.md) - Production deployment procedures

### Reference

- [Installation Notes](./INSTALLATION_NOTES.md) - Installation history and notes

## Prerequisites

### Required Software

- **Docker Engine**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **Make**: GNU Make 4.0 or higher (optional but recommended)

### System Requirements

- **RAM**: 8 GB minimum, 16 GB recommended
- **Disk Space**: 10 GB free space minimum
- **CPU**: 4 cores recommended
- **OS**: Linux, macOS, or Windows with WSL2

### Verify Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version

# Check Make version
make --version

# Verify Docker is running
docker ps
```

## Container Overview

### Frontend Container

**Purpose**: Serve React application with hot module replacement

**Technology**: Node.js 20 Alpine, Vite, React 18

**Ports**:
- `3000` - HTTP server (mapped to host)

**Health Check**: HTTP GET to `http://localhost:3000`

**Key Features**:
- Hot module replacement for development
- Nginx for production builds
- Environment-based configuration

See [Docker Setup Guide](./docker-setup.md#frontend-container) for details.

### Backend API Container

**Purpose**: Run FastAPI application with Lambda handlers

**Technology**: Python 3.11, FastAPI, Uvicorn

**Ports**:
- `8000` - API Gateway endpoints
- `9229` - Python debugger (development only)

**Health Check**: HTTP GET to `http://localhost:8000/health`

**Key Features**:
- Auto-reload on code changes
- Structured JSON logging
- Health check endpoints
- Connection validation

See [Docker Setup Guide](./docker-setup.md#backend-api-container) for details.

### DynamoDB Local Container

**Purpose**: Local DynamoDB instance for data persistence

**Technology**: Amazon DynamoDB Local

**Ports**:
- `8001` - DynamoDB API

**Health Check**: AWS CLI table list command

**Key Features**:
- Persistent data storage with volumes
- Automatic table initialization
- Compatible with AWS SDK

See [Docker Setup Guide](./docker-setup.md#dynamodb-local-container) for details.

### LocalStack Container

**Purpose**: Mock AWS services for local development

**Technology**: LocalStack

**Ports**:
- `4566` - LocalStack gateway

**Services**: S3, CloudWatch, Secrets Manager, Bedrock (mocked)

**Health Check**: HTTP GET to `http://localhost:4566/_localstack/health`

See [Docker Setup Guide](./docker-setup.md#localstack-container) for details.

## Common Tasks

### Building Containers

```bash
# Build all containers
make build

# Build specific container
docker-compose build frontend

# Build without cache
make rebuild
```

### Starting Services

```bash
# Start all services
make up

# Start in detached mode
make up -d

# Start specific service
docker-compose up frontend
```

### Stopping Services

```bash
# Stop all services
make down

# Stop and remove volumes
make clean
```

### Viewing Logs

```bash
# View all logs
make logs

# View specific service logs
make logs-frontend
make logs-backend

# Follow logs in real-time
docker-compose logs -f
```

### Health Checks

```bash
# Check health of all services
make health

# Wait for all services to be healthy
make wait-healthy

# Monitor health continuously
make monitor
```

### Debugging

```bash
# Open shell in container
make shell-frontend
make shell-backend

# View container status
docker-compose ps

# Inspect container
docker inspect vibegraph-backend-api
```

## Networking

All containers run on a shared Docker bridge network (`vibegraph-network`) with DNS resolution enabled.

### Service Discovery

Containers can communicate using service names:

```bash
# Frontend to Backend
http://backend-api:8000

# Backend to DynamoDB
http://dynamodb-local:8001

# Backend to LocalStack
http://localstack:4566
```

### Port Mapping

| Service | Internal Port | External Port | Purpose |
|---------|--------------|---------------|---------|
| frontend | 3000 | 3000 | HTTP server |
| backend-api | 8000 | 8000 | API endpoints |
| dynamodb-local | 8001 | 8001 | DynamoDB API |
| localstack | 4566 | 4566 | AWS services |

See [Networking Guide](./networking.md) for detailed information.

## Data Persistence

### Named Volumes

**dynamodb-data**: Persists DynamoDB tables across container restarts

```bash
# Backup DynamoDB data
aws dynamodb scan --table-name vibegraph-users --endpoint-url http://localhost:8001 > backup.json

# Restore DynamoDB data
aws dynamodb batch-write-item --request-items file://backup.json --endpoint-url http://localhost:8001
```

**localstack-data**: Persists LocalStack service data

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect vibegraph_dynamodb-data

# Remove volume
docker volume rm vibegraph_dynamodb-data
```

## Environment Configuration

Environment variables are configured in multiple locations:

1. **docker-compose.yml** - Default values for all services
2. **docker-compose.override.yml** - Local development overrides
3. **.env files** - Service-specific configuration

See [Environment Configuration](./environment.md) for complete reference.

## Health Monitoring

### Health Check Endpoints

- `GET /health` - Basic liveness check
- `GET /health/ready` - Readiness check with dependencies
- `GET /health/db` - DynamoDB connection status
- `GET /health/bedrock` - Bedrock connection status
- `GET /health/status` - Comprehensive status report

### Monitoring Commands

```bash
# Check health status
make health

# Wait for healthy state
make wait-healthy

# Continuous monitoring
make monitor

# Diagnose issues
make diagnose
```

See [Networking Guide](./networking.md#health-checks) for details.

## Troubleshooting

### Container Won't Start

```bash
# Check logs for errors
make logs

# Check container status
docker-compose ps

# Rebuild container
make rebuild
```

### Health Check Failing

```bash
# Check health status
make health

# Validate connections
make check-connections

# View detailed diagnostics
make diagnose
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

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

### Permission Issues

```bash
# Fix permissions on bind mounts
chmod -R 755 ./frontend
chmod -R 755 ./backend

# Run as current user
docker-compose run --user $(id -u):$(id -g) backend-api sh
```

For more troubleshooting tips, see the [Development Guide](../DEVELOPMENT.md#troubleshooting).

## Performance Optimization

### Build Optimization

The project uses several optimization strategies to reduce build times and image sizes:

- **Multi-stage builds** - Separate build and runtime dependencies
- **BuildKit** - Docker's next-generation build system with improved caching
- **Cache mounts** - Persistent caches for npm and pip packages
- **Layer caching** - Optimized Dockerfile layer ordering
- **.dockerignore** - Exclude unnecessary files from build context

**Expected improvements:**
- 50-90% reduction in image sizes
- 80-90% faster rebuilds with cached dependencies
- Reduced network usage during builds

**Verify optimizations:**
```bash
# Check BuildKit status and image sizes
make build-info

# Run comprehensive verification
./scripts/verify-optimizations.sh

# View image sizes
make image-sizes

# Inspect image layers
make inspect-layers IMAGE=vibegraph-frontend
```

See [Optimization Guide](./optimization.md) for detailed information.

### Runtime Optimization

- Use provisioned concurrency for Lambda functions
- Implement caching for expensive operations
- Use connection pooling for database connections
- Enable compression for API responses

See [Docker Setup Guide](./docker-setup.md#performance-optimization) for details.

## Security Best Practices

### Development

- Never commit secrets to version control
- Use environment variables for configuration
- Restrict CORS to specific domains
- Keep base images updated

### Production

- Run containers as non-root user
- Use read-only file systems where possible
- Enable TLS/HTTPS for all external endpoints
- Use AWS IAM roles instead of access keys
- Rotate JWT secrets regularly
- Enable audit logging

See [Deployment Guide](./DEPLOYMENT.md#security) for production security.

## Makefile Commands

Quick reference for common Makefile commands:

```bash
make build          # Build all Docker images
make up             # Start all containers
make down           # Stop all containers
make restart        # Restart all containers
make logs           # View logs from all containers
make clean          # Remove containers, volumes, and images
make test           # Run all tests
make health         # Check health of all containers
make wait-healthy   # Wait for all containers to be healthy
make monitor        # Continuously monitor health status
```

See [Makefile Commands](./makefile.md) for complete reference.

## Next Steps

- Read the [Docker Setup Guide](./docker-setup.md) for detailed container configuration
- Review the [Docker Compose Guide](./docker-compose.md) for orchestration details
- Check the [Environment Configuration](./environment.md) for configuration options
- See the [Deployment Guide](./DEPLOYMENT.md) for production deployment

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [DynamoDB Local Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
- [LocalStack Documentation](https://docs.localstack.cloud/)
