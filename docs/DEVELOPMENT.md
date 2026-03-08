# Development Guide

## Overview

This guide provides comprehensive instructions for setting up, developing, and testing the VibeGraph application locally.

## Prerequisites

### Required Software

- **Docker Engine**: 20.10 or higher
- **Docker Compose**: 2.0 or higher
- **Make**: GNU Make 4.0 or higher (optional but recommended)
- **Git**: For version control

### System Requirements

- **RAM**: 8 GB minimum, 16 GB recommended
- **Disk Space**: 10 GB free space minimum
- **CPU**: 4 cores recommended
- **OS**: Linux, macOS, or Windows with WSL2

### Verify Installation

```bash
docker --version
docker-compose --version
make --version
git --version
```

## Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/your-org/vibegraph.git
cd vibegraph
```

### 2. Configure Environment

```bash
# Copy environment files
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env
```

### 3. Build and Start

```bash
# Build all containers
make build

# Start all services
make up

# Wait for services to be healthy
make wait-healthy
```

### 4. Verify Setup

```bash
# Check health status
make health

# View logs
make logs
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **DynamoDB Admin**: http://localhost:8001

## Development Workflow

### Making Changes

#### Frontend Changes

1. Edit files in `frontend/src/`
2. Changes auto-reload in browser
3. Check browser console for errors

#### Backend Changes

1. Edit files in `backend/`
2. Server auto-reloads on save
3. Check logs: `make logs-backend`

### Running Tests

```bash
# Run all tests
make test

# Run frontend tests only
make test-frontend

# Run backend tests only
make test-backend

# Run integration tests
make test-integration
```

### Viewing Logs

```bash
# All services
make logs

# Specific service
make logs-frontend
make logs-backend

# Follow logs in real-time
docker-compose logs -f
```

### Debugging

#### Frontend Debugging

1. Open browser DevTools
2. Use React DevTools extension
3. Check console for errors
4. Use `console.log()` for debugging

#### Backend Debugging

1. View logs: `make logs-backend`
2. Use Python debugger (pdb)
3. Check health endpoints: `curl http://localhost:8000/health`

### Database Management

#### View DynamoDB Tables

```bash
# List tables
aws dynamodb list-tables --endpoint-url http://localhost:8001

# Scan table
aws dynamodb scan --table-name vibegraph-users --endpoint-url http://localhost:8001
```

#### Initialize Tables

```bash
# Run initialization script
make init-db
```

#### Seed Test Data

```bash
# Seed database with test data
docker-compose exec backend-api python scripts/seed-data.py
```

## Common Tasks

### Restart Services

```bash
# Restart all services
make restart

# Restart specific service
docker-compose restart backend-api
```

### Clean and Rebuild

```bash
# Stop and remove everything
make clean

# Rebuild from scratch
make rebuild

# Start fresh
make up
```

### Shell Access

```bash
# Frontend container
make shell-frontend

# Backend container
make shell-backend
```

### Health Checks

```bash
# Check health status
make health

# Wait for healthy state
make wait-healthy

# Monitor continuously
make monitor
```

## Testing

### Unit Tests

#### Frontend Unit Tests

```bash
# Run tests
cd frontend
npm test

# Run with coverage
npm test -- --coverage
```

#### Backend Unit Tests

```bash
# Run tests
cd backend
pytest

# Run with coverage
pytest --cov=src
```

### Integration Tests

```bash
# Run integration tests
make test-integration

# Run specific test
docker-compose exec backend-api pytest tests/integration/test_quiz_flow.py
```

### End-to-End Tests

```bash
# Run E2E tests
cd frontend
npm run test:e2e
```

## Troubleshooting

### Containers Won't Start

**Problem**: Containers fail to start

**Solution**:
```bash
# Check logs
make logs

# Rebuild containers
make rebuild

# Check Docker resources
docker system df
```

### Health Checks Failing

**Problem**: Health checks don't pass

**Solution**:
```bash
# Check health status
make health

# Validate connections
make check-connections

# View diagnostics
make diagnose
```

### Port Conflicts

**Problem**: Port already in use

**Solution**:
```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 [PID]

# Or change port in docker-compose.yml
```

### Database Connection Issues

**Problem**: Can't connect to DynamoDB

**Solution**:
```bash
# Check DynamoDB is running
docker-compose ps dynamodb-local

# Test connection
aws dynamodb list-tables --endpoint-url http://localhost:8001

# Restart DynamoDB
docker-compose restart dynamodb-local
```

### Frontend Not Loading

**Problem**: Frontend shows blank page

**Solution**:
```bash
# Check frontend logs
make logs-frontend

# Check browser console
# Verify API_URL in frontend/.env

# Rebuild frontend
docker-compose build frontend
docker-compose up frontend
```

### Backend API Errors

**Problem**: API returns 500 errors

**Solution**:
```bash
# Check backend logs
make logs-backend

# Check health endpoint
curl http://localhost:8000/health

# Verify environment variables
docker-compose exec backend-api env | grep AWS
```

### Out of Memory

**Problem**: Docker runs out of memory

**Solution**:
```bash
# Check Docker memory
docker info | grep Memory

# Increase Docker memory in Docker Desktop settings
# Or reduce container limits in docker-compose.yml
```

## Best Practices

### Code Style

#### Frontend

- Use ESLint and Prettier
- Follow React best practices
- Use TypeScript for type safety
- Write meaningful component names

#### Backend

- Follow PEP 8 style guide
- Use type hints
- Write docstrings
- Keep functions small and focused

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/my-feature

# Create pull request
```

### Commit Messages

Follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Test changes
- `refactor:` Code refactoring
- `chore:` Maintenance tasks

### Testing Guidelines

- Write tests for new features
- Maintain test coverage above 80%
- Test edge cases and error conditions
- Use meaningful test names

## Environment Variables

### Frontend Environment Variables

**File**: `frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_ENV=development
```

### Backend Environment Variables

**File**: `backend/.env`

```env
AWS_REGION=us-east-1
DYNAMODB_ENDPOINT=http://dynamodb-local:8001
BEDROCK_ENDPOINT=http://localstack:4566
USERS_TABLE=vibegraph-users
SESSIONS_TABLE=vibegraph-sessions
CACHE_TABLE=vibegraph-embedding-cache
LOG_LEVEL=debug
```

## Performance Tips

### Development Mode

- Use hot reload for faster iteration
- Enable debug logging
- Use local AWS services (DynamoDB Local, LocalStack)

### Optimization

- Minimize Docker image size
- Use multi-stage builds
- Cache dependencies
- Use .dockerignore files

## Security Considerations

### Development

- Never commit secrets to Git
- Use environment variables for configuration
- Keep dependencies updated
- Use HTTPS in production

### Testing

- Test authentication flows
- Validate input sanitization
- Test rate limiting
- Check CORS configuration

## Additional Resources

- [API Documentation](./api/README.md)
- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)
- [Infrastructure Documentation](./infrastructure/README.md)
- [Docker Setup Guide](./infrastructure/docker-setup.md)

## Getting Help

- **Documentation Issues**: Check this guide and related docs
- **Bug Reports**: Open an issue on GitHub
- **Questions**: Ask in team discussions
- **Urgent Issues**: Contact the development team

## Next Steps

After setup:

1. Explore the codebase
2. Run the test suite
3. Try making a small change
4. Read the architecture documentation
5. Review the API documentation
