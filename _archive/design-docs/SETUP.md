# VibeGraph Development Setup Guide

Complete guide for setting up the VibeGraph application for local development.

## Prerequisites

- **Docker** (v20.10+) and **Docker Compose** (v2.0+)
- **Node.js** (v20+) and **npm** (v9+) - for frontend development
- **Python** (v3.11+) - for backend development
- **Make** - for convenient command shortcuts
- **Git** - for version control

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd vibegraph-app

# Build all Docker images
make build

# Start all containers
make up

# Wait for all services to be healthy (up to 2 minutes)
make wait-healthy

# View logs
make logs

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Architecture Overview

The application consists of 6 Docker containers:

1. **frontend** - React app served by nginx (port 3000)
2. **backend-api** - FastAPI gateway (port 8000)
3. **backend-handlers** - Lambda function handlers
4. **backend-services** - Shared service layer
5. **dynamodb-local** - Local DynamoDB instance (port 8001)
6. **localstack** - Mock AWS services for Bedrock (port 4566)

## Detailed Setup

### 1. Environment Configuration

The application uses environment variables for configuration. Default values are provided in `docker-compose.yml` and `docker-compose.override.yml`.

**Key Environment Variables:**

```bash
# AWS Configuration (for local development)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test

# DynamoDB Configuration
DYNAMODB_ENDPOINT=http://dynamodb-local:8000
USERS_TABLE=vibegraph-users
SESSIONS_TABLE=vibegraph-sessions
CACHE_TABLE=vibegraph-embedding-cache

# Bedrock Configuration
BEDROCK_ENDPOINT=http://localstack:4566
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
TITAN_MODEL=amazon.titan-embed-text-v2:0

# Frontend Configuration
VITE_API_URL=http://localhost:8000
```

### 2. Building the Application

```bash
# Build all images
make build

# Build specific service
docker-compose build frontend
docker-compose build backend-api
```

The build process uses multi-stage Dockerfiles with BuildKit caching for faster rebuilds.

### 3. Starting Services

```bash
# Start all services in detached mode
make up

# Start specific service
docker-compose up -d frontend

# View real-time logs
make logs

# Follow logs for specific service
docker-compose logs -f backend-api
```

### 4. Database Initialization

DynamoDB tables are automatically created on first startup by the `dynamodb-init` container:

- `vibegraph-users` - User profiles and preferences
- `vibegraph-sessions` - Quiz sessions and progress
- `vibegraph-embedding-cache` - Cached embeddings for performance

**Verify tables:**

```bash
# Check init logs
docker logs vibegraph-dynamodb-init

# List tables via AWS CLI
aws dynamodb list-tables \
  --endpoint-url http://localhost:8001 \
  --region us-east-1 \
  --no-sign-request
```

### 5. Health Checks

All services have health checks that verify dependencies:

```bash
# Check all container status
docker ps

# Test backend API health
curl http://localhost:8000/health

# Test backend API readiness (includes dependency checks)
curl http://localhost:8000/health/ready

# Test frontend
curl http://localhost:3000
```

## Development Workflow

### Frontend Development

The frontend uses React + Vite with hot module replacement (HMR).

```bash
# Frontend runs in production mode (nginx) by default
# For development with HMR, run locally:
cd frontend
npm install
npm run dev
# Access at http://localhost:5173
```

**Frontend Structure:**
```
frontend/
├── src/
│   ├── components/     # React components
│   ├── pages/          # Page components
│   ├── hooks/          # Custom React hooks
│   ├── utils/          # Utility functions
│   └── App.jsx         # Main app component
├── public/             # Static assets
├── index.html          # HTML template
└── vite.config.js      # Vite configuration
```

### Backend Development

The backend uses FastAPI with hot reload enabled in development mode.

```bash
# Backend API runs with --reload flag automatically
# Edit files in backend/api/ and changes will auto-reload

# Run tests
cd backend
pytest

# Run specific test file
pytest tests/unit/test_validation.py

# Run with coverage
pytest --cov=src --cov-report=html
```

**Backend Structure:**
```
backend/
├── api/
│   ├── main.py         # FastAPI application
│   ├── health.py       # Health check endpoints
│   ├── startup.py      # Startup dependency checks
│   └── routes/         # API route handlers
├── src/
│   ├── handlers/       # Lambda function handlers
│   ├── services/       # Service layer (DynamoDB, Bedrock)
│   └── utils/          # Utility modules
└── tests/
    ├── unit/           # Unit tests
    └── integration/    # Integration tests
```

### Making Code Changes

**Backend API changes:**
1. Edit files in `backend/api/` or `backend/src/`
2. Changes are automatically detected and reloaded
3. Check logs: `docker-compose logs -f backend-api`

**Frontend changes:**
1. For production build: Edit files and rebuild
   ```bash
   docker-compose build frontend
   docker-compose up -d frontend
   ```
2. For development: Run locally with `npm run dev`

### Database Operations

**View data:**
```bash
# Scan users table
aws dynamodb scan \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8001 \
  --region us-east-1 \
  --no-sign-request

# Get specific item
aws dynamodb get-item \
  --table-name vibegraph-users \
  --key '{"userId": {"S": "user123"}}' \
  --endpoint-url http://localhost:8001 \
  --region us-east-1 \
  --no-sign-request
```

**Reset database:**
```bash
# Stop containers
make down

# Remove DynamoDB data volume
docker volume rm vibegraph-dynamodb-data

# Restart (tables will be recreated)
make up
```

## Testing

### Running Tests

```bash
# Run all tests
make test

# Run backend tests only
cd backend
pytest

# Run frontend tests only
cd frontend
npm test

# Run integration tests
cd backend
pytest tests/integration/

# Run with coverage
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

### Manual API Testing

```bash
# Health check
curl http://localhost:8000/health

# Readiness check (includes dependencies)
curl http://localhost:8000/health/ready

# API documentation
open http://localhost:8000/docs

# Test quiz endpoint (example)
curl -X POST http://localhost:8000/api/quiz/start \
  -H "Content-Type: application/json" \
  -d '{"userId": "test-user"}'
```

## Troubleshooting

### Container Issues

**Container won't start:**
```bash
# Check logs
docker-compose logs <service-name>

# Check container status
docker ps -a

# Restart specific service
docker-compose restart <service-name>

# Rebuild and restart
docker-compose up -d --build <service-name>
```

**Port conflicts:**
```bash
# Check what's using a port
lsof -i :3000
lsof -i :8000

# Kill process using port
kill -9 <PID>
```

**DynamoDB connection issues:**
```bash
# Verify DynamoDB is running
docker logs vibegraph-dynamodb-local

# Test connection
curl http://localhost:8001

# Check tables were created
docker logs vibegraph-dynamodb-init
```

### Common Issues

**1. "Module not found" errors in backend:**
- Ensure PYTHONPATH is set correctly in docker-compose.override.yml
- Check that `backend/src/utils/__init__.py` exists
- Restart the container: `docker-compose restart backend-api`

**2. Frontend not loading:**
- Check nginx logs: `docker logs vibegraph-frontend`
- Verify build completed: `docker-compose build frontend`
- Check healthcheck: `docker exec vibegraph-frontend wget -O- http://127.0.0.1:3000`

**3. DynamoDB tables not created:**
- Check init logs: `docker logs vibegraph-dynamodb-init`
- Verify DynamoDB is healthy: `docker ps | grep dynamodb`
- Manually run init: `docker-compose up dynamodb-init`

**4. LocalStack/Bedrock errors:**
- This is expected in local development
- Bedrock functionality will be limited without real AWS credentials
- Check logs: `docker logs vibegraph-localstack`

### Performance Issues

**Slow builds:**
```bash
# Enable BuildKit for faster builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Clean build cache if needed
docker builder prune
```

**High memory usage:**
```bash
# Check container resource usage
docker stats

# Limit container resources in docker-compose.yml:
services:
  backend-api:
    deploy:
      resources:
        limits:
          memory: 512M
```

## Useful Commands

### Make Commands

```bash
make build          # Build all Docker images
make up             # Start all containers
make down           # Stop and remove all containers
make restart        # Restart all containers
make logs           # View logs from all containers
make ps             # Show container status
make clean          # Remove containers, networks, and volumes
make test           # Run all tests
make wait-healthy   # Wait for all containers to be healthy
```

### Docker Commands

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# Execute command in container
docker exec -it vibegraph-backend-api bash

# View container logs
docker logs vibegraph-backend-api

# Follow logs in real-time
docker logs -f vibegraph-backend-api

# Inspect container
docker inspect vibegraph-backend-api

# View container resource usage
docker stats
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart service
docker-compose restart backend-api

# Rebuild and start
docker-compose up -d --build

# View logs
docker-compose logs -f backend-api

# Execute command
docker-compose exec backend-api bash

# Scale service (if applicable)
docker-compose up -d --scale backend-api=3
```

## Development Best Practices

### Code Style

**Python (Backend):**
- Follow PEP 8 style guide
- Use type hints for function signatures
- Write docstrings for all public functions
- Run linting: `flake8 backend/`
- Format code: `black backend/`

**JavaScript/React (Frontend):**
- Use ESLint for linting
- Follow Airbnb style guide
- Use functional components with hooks
- Run linting: `npm run lint`
- Format code: `npm run format`

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push to remote
git push origin feature/your-feature-name

# Create pull request on GitHub
```

### Testing Guidelines

- Write unit tests for all new functions
- Write integration tests for API endpoints
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use meaningful test names

### Security Considerations

- Never commit real AWS credentials
- Use environment variables for sensitive data
- Keep dependencies up to date
- Review security advisories regularly
- Use HTTPS in production

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [DynamoDB Local Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
- [LocalStack Documentation](https://docs.localstack.cloud/)

## Getting Help

- Check the [Troubleshooting](#troubleshooting) section
- Review container logs: `make logs`
- Check GitHub issues
- Contact the development team

## Next Steps

After completing setup:

1. Review the [API Documentation](http://localhost:8000/docs)
2. Explore the codebase structure
3. Run the test suite: `make test`
4. Try making a small change and see hot reload in action
5. Read the [AWS Migration Guide](AWS_MIGRATION.md) for production deployment
