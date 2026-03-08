# Quick Start Guide

Get VibeGraph up and running in 5 minutes.

## Prerequisites

Before you begin, ensure you have:

- **Docker Engine** 20.10+ installed ([Install Docker](https://docs.docker.com/get-docker/))
- **Docker Compose** 2.0+ installed ([Install Docker Compose](https://docs.docker.com/compose/install/))
- **8 GB RAM** minimum (16 GB recommended)
- **10 GB free disk space**

### Verify Prerequisites

```bash
docker --version
# Expected: Docker version 20.10.0 or higher

docker-compose --version
# Expected: Docker Compose version 2.0.0 or higher
```

## Quick Start (3 Steps)

### 1. Clone and Navigate

```bash
git clone https://github.com/your-org/vibegraph.git
cd vibegraph
```

### 2. Start All Services

```bash
make up
```

This command will:
- Build all Docker images (first time only, ~5-10 minutes)
- Start all containers (frontend, backend, database, AWS mocks)
- Initialize DynamoDB tables
- Run health checks

### 3. Wait for Services to Be Ready

```bash
make wait-healthy
```

This waits for all containers to pass health checks (typically 30-60 seconds).

## Access the Application

Once all services are healthy:

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **DynamoDB Admin**: http://localhost:8001

## Verify Everything Works

### Check Health Status

```bash
make health
```

Expected output:
```
✓ frontend: healthy
✓ backend-api: healthy
✓ dynamodb-local: healthy
✓ localstack: healthy
```

### Test the Quiz Flow

1. Open http://localhost:3000 in your browser
2. Click "Start Quiz" or navigate to the onboarding page
3. Answer Section 1 questions (5 questions)
4. Answer Section 2 questions (5 adaptive questions)
5. View your Taste DNA profile

### Test API Endpoints

```bash
# Test health endpoint
curl http://localhost:8000/health

# Expected: {"status":"healthy","timestamp":"..."}

# Test quiz start endpoint
curl -X POST http://localhost:8000/api/quiz/section1/start

# Expected: {"sessionId":"...","questions":[...],"expiresAt":...}
```

## Common Commands

```bash
# View logs from all services
make logs

# View logs from specific service
make logs-backend
make logs-frontend

# Restart all services
make restart

# Stop all services
make down

# Clean up everything (containers, volumes, images)
make clean

# Rebuild from scratch
make rebuild
```

## Troubleshooting

### Containers Won't Start

**Problem**: `make up` fails or containers exit immediately

**Solution**:
```bash
# Check what went wrong
make logs

# Try rebuilding
make rebuild
```

### Health Checks Failing

**Problem**: `make wait-healthy` times out

**Solution**:
```bash
# Check which service is unhealthy
docker ps

# View logs for unhealthy service
docker logs vibegraph-backend-api

# Common fix: restart the service
docker-compose restart backend-api
```

### Port Already in Use

**Problem**: Error message about port 3000, 8000, or 8001 already in use

**Solution**:
```bash
# Find what's using the port
lsof -i :8000

# Kill the process
kill -9 [PID]

# Or change the port in docker-compose.yml
```

### Frontend Shows Blank Page

**Problem**: Browser shows blank page at http://localhost:3000

**Solution**:
```bash
# Check frontend logs
make logs-frontend

# Verify backend is accessible
curl http://localhost:8000/health

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

### Backend API Returns 500 Errors

**Problem**: API requests fail with 500 Internal Server Error

**Solution**:
```bash
# Check backend logs
make logs-backend

# Verify DynamoDB is running
curl http://localhost:8000/health/db

# Restart backend
docker-compose restart backend-api
```

### Out of Memory

**Problem**: Docker reports out of memory errors

**Solution**:
1. Open Docker Desktop settings
2. Increase memory allocation to at least 8 GB
3. Restart Docker
4. Run `make rebuild`

### Database Connection Issues

**Problem**: Backend can't connect to DynamoDB

**Solution**:
```bash
# Check DynamoDB is running
docker ps | grep dynamodb

# Test DynamoDB connection
aws dynamodb list-tables --endpoint-url http://localhost:8001

# Reinitialize tables
make init-db
```

## Next Steps

Now that you have VibeGraph running:

1. **Explore the UI**: Try the complete quiz flow at http://localhost:3000
2. **Test the API**: Visit http://localhost:8000/docs for interactive API documentation
3. **View the Code**: Check out the codebase structure
4. **Read the Docs**: See [Development Guide](./DEVELOPMENT.md) for detailed information
5. **Make Changes**: Edit code and see hot reload in action

## Development Workflow

### Making Frontend Changes

1. Edit files in `frontend/src/`
2. Changes automatically reload in browser
3. Check browser console for errors

### Making Backend Changes

1. Edit files in `backend/`
2. Server automatically reloads
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

## Stopping and Cleaning Up

### Stop Services (Keep Data)

```bash
make down
```

This stops all containers but preserves data in Docker volumes.

### Clean Everything (Remove Data)

```bash
make clean
```

This removes all containers, volumes, and images. You'll need to rebuild next time.

### Start Fresh

```bash
# Complete reset
make clean
make build
make up
make wait-healthy
```

## Getting Help

If you encounter issues not covered here:

1. **Check Logs**: `make logs` often reveals the problem
2. **Check Health**: `make health` shows which services are unhealthy
3. **Read Docs**: See [DEVELOPMENT.md](./DEVELOPMENT.md) for detailed troubleshooting
4. **Check Issues**: Search GitHub issues for similar problems
5. **Ask for Help**: Open a new issue with logs and error messages

## Additional Resources

- [Development Guide](./DEVELOPMENT.md) - Comprehensive development documentation
- [API Documentation](./api/README.md) - Complete API reference
- [Docker Setup](./infrastructure/docker-setup.md) - Docker configuration details
- [Troubleshooting Guide](./TROUBLESHOOTING.md) - Common issues and solutions
- [Architecture Overview](./architecture/design.md) - System design and architecture

## Quick Reference

### Essential Commands

| Command | Description |
|---------|-------------|
| `make up` | Start all services |
| `make down` | Stop all services |
| `make logs` | View all logs |
| `make health` | Check health status |
| `make test` | Run all tests |
| `make clean` | Remove everything |
| `make rebuild` | Clean and rebuild |

### Service URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | React application |
| Backend API | http://localhost:8000 | REST API endpoints |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| DynamoDB | http://localhost:8001 | Local database |

### Health Check Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/health` | Basic liveness check |
| `/health/ready` | Readiness with dependencies |
| `/health/db` | DynamoDB connection |
| `/health/bedrock` | Bedrock connection |
| `/health/status` | Comprehensive status |

## Success Checklist

You're ready to develop when:

- [ ] All containers are running: `docker ps` shows 4 containers
- [ ] All health checks pass: `make health` shows all green
- [ ] Frontend loads: http://localhost:3000 shows the app
- [ ] Backend responds: http://localhost:8000/health returns 200
- [ ] API docs work: http://localhost:8000/docs loads
- [ ] Quiz flow works: Can complete onboarding flow
- [ ] Tests pass: `make test` succeeds

## What's Next?

- **Build Features**: Start developing new features
- **Write Tests**: Add tests for your changes
- **Read Architecture**: Understand the system design
- **Explore API**: Try different API endpoints
- **Customize**: Modify configuration for your needs

Happy coding! 🚀
