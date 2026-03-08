# Docker Setup Guide

## Overview

This guide provides comprehensive documentation for Docker configuration, Dockerfiles, and container setup for the VibeGraph application.

## Container Architecture

VibeGraph uses 4 main Docker containers:

1. **Frontend** - React application (port 3000)
2. **Backend API** - FastAPI application (port 8000)
3. **DynamoDB Local** - Local database (port 8001)
4. **LocalStack** - AWS service mocking (port 4566)

## Dockerfiles

### Frontend Dockerfile

**Location**: `frontend/Dockerfile`

```dockerfile
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source code
COPY . .

# Expose port
EXPOSE 3000

# Start dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]
```

**Key Features**:
- Node.js 20 Alpine base (lightweight)
- Dependency caching layer
- Hot module replacement enabled
- Binds to all interfaces for Docker networking

### Backend Dockerfile

**Location**: `backend/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose ports
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**Key Features**:
- Python 3.11 slim base
- System dependencies for health checks
- Pip dependency caching
- Built-in health check
- Auto-reload for development

## Docker Ignore Files

### Frontend .dockerignore

**Location**: `frontend/.dockerignore`

```
node_modules
dist
.env
.env.local
npm-debug.log*
.DS_Store
.vscode
coverage
```

### Backend .dockerignore

**Location**: `backend/.dockerignore`

```
__pycache__
*.pyc
.env
.pytest_cache
.coverage
*.log
.DS_Store
.vscode
```

## Building Images

### Build All Images

```bash
# Using Makefile
make build

# Using Docker Compose
docker-compose build
```

### Build Specific Image

```bash
# Frontend only
docker-compose build frontend

# Backend only
docker-compose build backend
```

### Build with No Cache

```bash
make rebuild
```

## Running Containers

### Start All Containers

```bash
# Using Makefile
make up

# Using Docker Compose
docker-compose up
```

### Start in Detached Mode

```bash
docker-compose up -d
```

### Stop Containers

```bash
make down
```

## Health Checks

All containers implement health checks:

### Frontend Health Check

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 20s
```

### Backend Health Check

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### DynamoDB Health Check

```yaml
healthcheck:
  test: ["CMD-SHELL", "curl -f http://localhost:8001 || exit 1"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 10s
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs [service-name]

# Rebuild container
docker-compose up --build --force-recreate [service-name]
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 [PID]
```

### Permission Denied

```bash
# Fix permissions
chmod -R 755 ./frontend
chmod -R 755 ./backend
```

## Related Documentation

- [Docker Compose Guide](./docker-compose.md)
- [Makefile Commands](./makefile.md)
- [Networking Guide](./networking.md)
