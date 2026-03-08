# Environment Configuration Guide

This document describes all environment variables used in the VibeGraph application, how to configure them for different environments, and setup instructions.

## Table of Contents

- [Overview](#overview)
- [Frontend Environment Variables](#frontend-environment-variables)
- [Backend Environment Variables](#backend-environment-variables)
- [Environment Setup](#environment-setup)
- [Docker Compose Override](#docker-compose-override)
- [Production Configuration](#production-configuration)
- [Troubleshooting](#troubleshooting)

## Overview

VibeGraph uses environment variables to configure different aspects of the application across frontend and backend services. Configuration is managed through:

- **`.env.example` files**: Template files with all available variables and descriptions
- **`.env` files**: Local environment files (not committed to git)
- **`docker-compose.yml`**: Default Docker environment configuration
- **`docker-compose.override.yml`**: Local development overrides

## Frontend Environment Variables

Frontend environment variables are prefixed with `VITE_` to be accessible in the Vite build process.

### Configuration File Locations

- **Template**: `frontend/.env.example`
- **Local Development**: `frontend/.env`
- **Docker Development**: `frontend/.env.docker`

### Available Variables

#### API Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_VIBEGRAPH_API_URL` | Base URL for backend API | `http://localhost:8000` | Yes |
| `VITE_API_TIMEOUT` | API request timeout in milliseconds | `30000` | No |

**Examples:**
- Local development: `http://localhost:8000`
- Docker development: `http://backend-api:8000`
- Production: `https://api.vibegraph.com`

#### Environment

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_ENV` | Application environment | `development` | No |
| `NODE_ENV` | Node environment | `development` | No |

**Options:** `development`, `staging`, `production`

#### Feature Flags

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_ENABLE_DARK_MODE` | Enable dark mode toggle | `true` | No |
| `VITE_ENABLE_SOCIAL_FEATURES` | Enable matching and analytics | `true` | No |

#### Logging

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_LOG_LEVEL` | Frontend logging level | `info` | No |

**Options:** `debug`, `info`, `warn`, `error`

#### Analytics (Optional)

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `VITE_ANALYTICS_ID` | Google Analytics tracking ID | - | No |
| `VITE_SENTRY_DSN` | Sentry error tracking DSN | - | No |

### Frontend Setup Example

```bash
# Copy the example file
cp frontend/.env.example frontend/.env

# Edit the file with your configuration
nano frontend/.env
```

**Local Development Configuration:**
```env
VITE_VIBEGRAPH_API_URL=http://localhost:8000
VITE_ENV=development
VITE_LOG_LEVEL=debug
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_SOCIAL_FEATURES=true
```

**Docker Development Configuration:**
```env
VITE_VIBEGRAPH_API_URL=http://backend-api:8000
VITE_ENV=development
NODE_ENV=development
```

## Backend Environment Variables

Backend environment variables configure AWS services, database connections, API settings, and application behavior.

### Configuration File Locations

- **Template**: `backend/.env.example`
- **Local Development**: `backend/.env`
- **Docker**: Set in `docker-compose.yml` and `docker-compose.override.yml`

### Available Variables

#### AWS Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `AWS_REGION` | AWS region for all services | `us-east-1` | Yes |
| `AWS_ACCESS_KEY_ID` | AWS access key | `test` (local) | Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | `test` (local) | Yes |

**Note:** For local development with LocalStack/DynamoDB Local, use test credentials. For production, use IAM roles or proper credentials.

#### DynamoDB Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DYNAMODB_ENDPOINT` | DynamoDB endpoint URL | `http://localhost:8001` | Yes (local) |
| `USERS_TABLE` | Users table name | `vibegraph-users` | Yes |
| `SESSIONS_TABLE` | Sessions table name | `vibegraph-sessions` | Yes |
| `CACHE_TABLE` | Embedding cache table name | `vibegraph-embedding-cache` | Yes |

**Endpoint Examples:**
- Local development: `http://localhost:8001`
- Docker development: `http://dynamodb-local:8000`
- Production: Leave empty to use AWS default

#### AWS Bedrock Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `BEDROCK_ENDPOINT` | Bedrock endpoint URL | `http://localhost:4566` | Yes (local) |
| `CLAUDE_MODEL` | Claude model identifier | `anthropic.claude-3-5-sonnet-20241022-v2:0` | Yes |
| `TITAN_MODEL` | Titan embedding model identifier | `amazon.titan-embed-text-v2:0` | Yes |

**Endpoint Examples:**
- Local development with LocalStack: `http://localhost:4566`
- Docker development: `http://localstack:4566`
- Production: Leave empty to use AWS default

#### API Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_HOST` | API server host | `0.0.0.0` | No |
| `API_PORT` | API server port | `8000` | No |
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated) | `http://localhost:3000` | Yes |
| `RATE_LIMIT` | Requests per minute per user | `100` | No |

**CORS Examples:**
- Development: `http://localhost:3000`
- Production: `https://vibegraph.com,https://www.vibegraph.com`

#### Logging Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `LOG_LEVEL` | Logging level | `INFO` | No |
| `PYTHONUNBUFFERED` | Python unbuffered output | `1` | No |
| `PYTHONPATH` | Python module path | `/app` | No |

**Log Levels:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

#### Cache Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CACHE_HIT_RATE_TARGET` | Target cache hit rate (0.0-1.0) | `0.4` | No |
| `CACHE_TTL` | Cache TTL in seconds | `2592000` (30 days) | No |

#### Retry Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `CLAUDE_RETRY_ATTEMPTS` | Claude API retry attempts | `3` | No |
| `TITAN_RETRY_ATTEMPTS` | Titan API retry attempts | `2` | No |
| `DYNAMODB_RETRY_ATTEMPTS` | DynamoDB retry attempts | `3` | No |
| `RETRY_BACKOFF_BASE_MS` | Retry backoff base in ms | `100` | No |

#### Security Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `JWT_SECRET_KEY` | JWT secret key | - | Yes |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` | No |
| `JWT_EXPIRATION` | JWT expiration in seconds | `86400` (24h) | No |

**Important:** Generate a secure random string for `JWT_SECRET_KEY` in production!

```bash
# Generate a secure JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Feature Flags

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `ENABLE_EMBEDDING_CACHE` | Enable embedding cache | `true` | No |
| `ENABLE_REQUEST_LOGGING` | Enable request logging | `true` | No |
| `ENABLE_METRICS` | Enable performance metrics | `true` | No |

#### Development Configuration

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DEBUG` | Enable debug mode | `false` | No |
| `HOT_RELOAD` | Enable hot reload | `true` | No |
| `MOCK_AWS_SERVICES` | Use LocalStack for AWS | `true` | No |

### Backend Setup Example

```bash
# Copy the example file
cp backend/.env.example backend/.env

# Edit the file with your configuration
nano backend/.env
```

**Local Development Configuration:**
```env
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test

# DynamoDB Configuration
DYNAMODB_ENDPOINT=http://localhost:8001
USERS_TABLE=vibegraph-users
SESSIONS_TABLE=vibegraph-sessions
CACHE_TABLE=vibegraph-embedding-cache

# Bedrock Configuration
BEDROCK_ENDPOINT=http://localhost:4566
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
TITAN_MODEL=amazon.titan-embed-text-v2:0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000

# Logging
LOG_LEVEL=DEBUG
PYTHONUNBUFFERED=1

# Development
DEBUG=true
HOT_RELOAD=true
MOCK_AWS_SERVICES=true
```

## Environment Setup

### Local Development Setup

1. **Install Prerequisites**
   ```bash
   # Install Docker and Docker Compose
   # Install Node.js 20+
   # Install Python 3.11+
   ```

2. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd vibegraph
   ```

3. **Create Environment Files**
   ```bash
   # Frontend
   cp frontend/.env.example frontend/.env
   
   # Backend
   cp backend/.env.example backend/.env
   ```

4. **Configure Environment Variables**
   - Edit `frontend/.env` with your frontend configuration
   - Edit `backend/.env` with your backend configuration
   - Use the examples above as a starting point

5. **Start Services**
   ```bash
   # Using Docker Compose
   make up
   
   # Or manually
   docker-compose up -d
   ```

6. **Verify Setup**
   ```bash
   # Check container health
   make health
   
   # Check logs
   make logs
   ```

### Docker Development Setup

When using Docker Compose, environment variables are configured in:

1. **`docker-compose.yml`**: Base configuration for all environments
2. **`docker-compose.override.yml`**: Local development overrides (auto-loaded)

The override file automatically applies when running `docker-compose up` without additional flags.

**To use only base configuration (no overrides):**
```bash
docker-compose -f docker-compose.yml up
```

**To use custom override file:**
```bash
docker-compose -f docker-compose.yml -f docker-compose.custom.yml up
```

## Docker Compose Override

The `docker-compose.override.yml` file provides development-specific configurations:

### Features

1. **Hot Reload**: Source code mounted as volumes for instant updates
2. **Debug Logging**: Enhanced logging for development
3. **Local Data Persistence**: Data stored in `./data/` directory
4. **Port Exposure**: All services accessible from host machine
5. **Development Commands**: Services run with development-friendly commands

### Override Configuration

The override file modifies:

- **Frontend**: Enables Vite dev server with HMR
- **Backend API**: Enables uvicorn auto-reload
- **Backend Services**: Mounts source code for hot reload
- **DynamoDB Local**: Persists data to local directory
- **LocalStack**: Enables debug mode and persistence

### Using the Override File

**Automatic (default behavior):**
```bash
# docker-compose.override.yml is automatically loaded
docker-compose up
```

**Disable override:**
```bash
# Use only base configuration
docker-compose -f docker-compose.yml up
```

**Custom override:**
```bash
# Use custom override file
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### Creating Custom Overrides

Create environment-specific override files:

**`docker-compose.staging.yml`:**
```yaml
services:
  backend-api:
    environment:
      - VITE_ENV=staging
      - LOG_LEVEL=INFO
```

**`docker-compose.prod.yml`:**
```yaml
services:
  backend-api:
    environment:
      - VITE_ENV=production
      - LOG_LEVEL=WARNING
      - DEBUG=false
    volumes: []  # Remove volume mounts for production
```

## Production Configuration

### Security Considerations

1. **Generate Secure Secrets**
   ```bash
   # JWT secret
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Use IAM Roles**
   - Don't use hardcoded AWS credentials in production
   - Use IAM roles for EC2/ECS/Lambda
   - Use AWS Secrets Manager for sensitive data

3. **Configure CORS Properly**
   ```env
   CORS_ORIGINS=https://vibegraph.com,https://www.vibegraph.com
   ```

4. **Enable TLS/HTTPS**
   - Use HTTPS for all API endpoints
   - Configure SSL certificates
   - Enable HSTS headers

5. **Disable Debug Mode**
   ```env
   DEBUG=false
   LOG_LEVEL=WARNING
   ```

### Production Environment Variables

**Frontend:**
```env
VITE_VIBEGRAPH_API_URL=https://api.vibegraph.com
VITE_ENV=production
VITE_LOG_LEVEL=error
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_SOCIAL_FEATURES=true
VITE_ANALYTICS_ID=UA-XXXXXXXXX-X
VITE_SENTRY_DSN=https://xxx@sentry.io/xxx
```

**Backend:**
```env
# AWS Configuration (use IAM roles, not hardcoded credentials)
AWS_REGION=us-east-1

# DynamoDB Configuration (use AWS default endpoint)
DYNAMODB_ENDPOINT=
USERS_TABLE=vibegraph-users-prod
SESSIONS_TABLE=vibegraph-sessions-prod
CACHE_TABLE=vibegraph-embedding-cache-prod

# Bedrock Configuration (use AWS default endpoint)
BEDROCK_ENDPOINT=
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
TITAN_MODEL=amazon.titan-embed-text-v2:0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://vibegraph.com,https://www.vibegraph.com
RATE_LIMIT=100

# Logging
LOG_LEVEL=WARNING
PYTHONUNBUFFERED=1

# Security
JWT_SECRET_KEY=<secure-random-string>
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400

# Feature Flags
ENABLE_EMBEDDING_CACHE=true
ENABLE_REQUEST_LOGGING=true
ENABLE_METRICS=true

# Production Settings
DEBUG=false
HOT_RELOAD=false
MOCK_AWS_SERVICES=false
```

### Deployment Checklist

- [ ] Generate secure JWT secret key
- [ ] Configure IAM roles for AWS access
- [ ] Set production API URLs
- [ ] Configure CORS for production domains
- [ ] Enable HTTPS/TLS
- [ ] Set appropriate log levels
- [ ] Disable debug mode
- [ ] Configure monitoring and alerting
- [ ] Set up backup and recovery
- [ ] Configure rate limiting
- [ ] Enable error tracking (Sentry)
- [ ] Configure analytics (Google Analytics)
- [ ] Test all environment variables
- [ ] Verify health checks work
- [ ] Test inter-service communication

## Troubleshooting

### Common Issues

#### 1. Frontend Can't Connect to Backend

**Symptom:** API requests fail with network errors

**Solutions:**
- Check `VITE_VIBEGRAPH_API_URL` is correct
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS configuration in backend
- Verify network connectivity between containers

```bash
# Test backend health
curl http://localhost:8000/health

# Check container networking
docker network inspect vibegraph-network
```

#### 2. Backend Can't Connect to DynamoDB

**Symptom:** Database operations fail

**Solutions:**
- Check `DYNAMODB_ENDPOINT` is correct
- Verify DynamoDB Local is running: `docker ps`
- Check DynamoDB health: `curl http://localhost:8001`
- Verify tables exist: `make init-db`

```bash
# Check DynamoDB Local
curl http://localhost:8001

# List tables
aws dynamodb list-tables --endpoint-url http://localhost:8001

# Reinitialize tables
make init-db
```

#### 3. Backend Can't Connect to Bedrock

**Symptom:** AI generation fails

**Solutions:**
- Check `BEDROCK_ENDPOINT` is correct
- Verify LocalStack is running: `docker ps`
- Check LocalStack health: `curl http://localhost:4566/_localstack/health`
- Verify Bedrock service is enabled in LocalStack

```bash
# Check LocalStack health
curl http://localhost:4566/_localstack/health

# Check LocalStack logs
docker logs vibegraph-localstack
```

#### 4. Environment Variables Not Loading

**Symptom:** Application uses default values instead of configured values

**Solutions:**
- Verify `.env` files exist and are not empty
- Check file permissions: `ls -la frontend/.env backend/.env`
- Restart containers: `make restart`
- Check environment variables in container: `docker exec vibegraph-backend-api env`

```bash
# Check environment variables in container
docker exec vibegraph-backend-api env | grep DYNAMODB

# Restart containers
make restart
```

#### 5. Hot Reload Not Working

**Symptom:** Code changes don't reflect in running application

**Solutions:**
- Verify `docker-compose.override.yml` is being used
- Check volume mounts: `docker inspect vibegraph-backend-api`
- Restart containers: `make restart`
- Check file permissions on mounted volumes

```bash
# Check if override file is loaded
docker-compose config

# Restart with rebuild
make rebuild
```

### Debug Commands

```bash
# View all environment variables in a container
docker exec <container-name> env

# Check container logs
docker logs <container-name>

# Inspect container configuration
docker inspect <container-name>

# Test network connectivity between containers
docker exec vibegraph-backend-api ping dynamodb-local

# Check health status
docker ps --format "table {{.Names}}\t{{.Status}}"

# View docker-compose configuration (with overrides)
docker-compose config
```

### Getting Help

If you encounter issues not covered here:

1. Check container logs: `make logs`
2. Check health status: `make health`
3. Review [TROUBLESHOOTING.md](../TROUBLESHOOTING.md)
4. Check [Docker Compose documentation](./docker-compose.md)
5. Check [Networking documentation](./networking.md)

## References

- [Docker Compose Documentation](./docker-compose.md)
- [Networking Guide](./networking.md)
- [Makefile Commands](./makefile.md)
- [Quick Start Guide](../../QUICKSTART.md)
- [Development Guide](../../DEVELOPMENT.md)
