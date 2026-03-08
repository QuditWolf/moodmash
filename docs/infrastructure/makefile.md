# Makefile Build Commands Guide

## Overview

The Makefile provides convenient commands for building, running, and managing Docker containers. It simplifies common development workflows and provides consistent commands across the team.

## Prerequisites

- GNU Make 3.81 or higher
- Docker Engine 20.10 or higher
- Docker Compose 2.0 or higher

## Quick Reference

| Command | Description |
|---------|-------------|
| `make build` | Build all Docker images |
| `make up` | Start all containers |
| `make down` | Stop all containers |
| `make restart` | Restart all containers |
| `make logs` | View logs from all containers |
| `make logs-frontend` | View frontend logs only |
| `make logs-backend` | View backend logs only |
| `make clean` | Remove all containers, volumes, and images |
| `make shell-frontend` | Open shell in frontend container |
| `make shell-backend` | Open shell in backend container |
| `make test` | Run all tests in containers |
| `make init-db` | Initialize DynamoDB tables |
| `make health` | Check health of all containers |
| `make monitor` | Continuously monitor health status |
| `make ps` | Show container status with health checks |

## Basic Commands

### Build Commands

#### make build

Build all Docker images.

```bash
make build
```

**What it does**:
- Builds all Docker images defined in docker-compose.yml
- Uses Docker layer caching for faster builds
- Outputs build progress and errors

**Equivalent to**:
```bash
docker-compose build
```

#### make rebuild

Clean and rebuild all images without cache.

```bash
make rebuild
```

**What it does**:
- Removes all existing images
- Rebuilds all images from scratch
- Useful when dependencies change

**Equivalent to**:
```bash
docker-compose build --no-cache
```

### Start/Stop Commands

#### make up

Start all containers in detached mode.

```bash
make up
```

**What it does**:
- Starts all containers defined in docker-compose.yml
- Runs in background (detached mode)
- Waits for health checks to pass

**Equivalent to**:
```bash
docker-compose up -d
```

#### make down

Stop and remove all containers.

```bash
make down
```

**What it does**:
- Stops all running containers
- Removes containers
- Preserves volumes (data persists)

**Equivalent to**:
```bash
docker-compose down
```

#### make restart

Restart all containers.

```bash
make restart
```

**What it does**:
- Stops all containers
- Starts all containers
- Useful for applying configuration changes

**Equivalent to**:
```bash
docker-compose restart
```

### Development Commands

#### make dev

Start containers in development mode with hot reload.

```bash
make dev
```

**What it does**:
- Starts all containers with development configuration
- Enables hot module replacement
- Mounts source code as volumes
- Exposes debug ports

**Equivalent to**:
```bash
docker-compose -f docker-compose.yml up --build
```

#### make prod

Start containers in production mode.

```bash
make prod
```

**What it does**:
- Starts containers with production configuration
- Uses optimized builds
- Disables debug features
- Uses read-only volumes

**Equivalent to**:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Logging Commands

#### make logs

View logs from all containers.

```bash
make logs
```

**What it does**:
- Displays logs from all containers
- Follows log output (live updates)
- Color-coded by service

**Equivalent to**:
```bash
docker-compose logs -f
```

#### make logs-frontend

View frontend logs only.

```bash
make logs-frontend
```

**What it does**:
- Displays logs from frontend container only
- Follows log output
- Useful for debugging frontend issues

**Equivalent to**:
```bash
docker-compose logs -f frontend
```

#### make logs-backend

View backend logs only.

```bash
make logs-backend
```

**What it does**:
- Displays logs from backend-api container only
- Follows log output
- Useful for debugging backend issues

**Equivalent to**:
```bash
docker-compose logs -f backend-api
```

## Shell Access Commands

#### make shell-frontend

Open shell in frontend container.

```bash
make shell-frontend
```

**What it does**:
- Opens interactive shell in frontend container
- Allows running npm commands
- Useful for debugging and testing

**Equivalent to**:
```bash
docker-compose exec frontend sh
```

**Example usage**:
```bash
make shell-frontend
# Inside container:
npm run test
npm run lint
```

#### make shell-backend

Open shell in backend container.

```bash
make shell-backend
```

**What it does**:
- Opens interactive shell in backend-api container
- Allows running node commands
- Useful for debugging Lambda functions

**Equivalent to**:
```bash
docker-compose exec backend-api sh
```

**Example usage**:
```bash
make shell-backend
# Inside container:
node --version
npm run test
aws dynamodb list-tables --endpoint-url http://dynamodb-local:8000
```

## Health Check Commands

#### make health

Check health of all containers.

```bash
make health
```

**What it does**:
- Displays health status of all containers
- Shows which containers are healthy/unhealthy
- Exits with error if any container is unhealthy

**Equivalent to**:
```bash
docker-compose ps
```

#### make wait-healthy

Wait for all containers to be healthy.

```bash
make wait-healthy
```

**What it does**:
- Waits for all containers to pass health checks
- Polls every 5 seconds
- Timeout after 120 seconds
- Useful in CI/CD pipelines

**Example**:
```bash
make up
make wait-healthy
make test
```

#### make monitor

Continuously monitor health status.

```bash
make monitor
```

**What it does**:
- Displays real-time health status
- Updates every 10 seconds
- Shows response times for health endpoints
- Press Ctrl+C to stop

#### make ps

Show container status with health checks.

```bash
make ps
```

**What it does**:
- Lists all containers
- Shows status (running, exited, etc.)
- Shows health status (healthy, unhealthy, starting)
- Shows port mappings

**Equivalent to**:
```bash
docker-compose ps
```

## Database Commands

#### make init-db

Initialize DynamoDB tables.

```bash
make init-db
```

**What it does**:
- Creates Users table
- Creates Sessions table
- Creates EmbeddingCache table
- Runs automatically on first startup

**Equivalent to**:
```bash
docker-compose exec backend-api node scripts/init-dynamodb.js
```

#### make seed-db

Seed database with sample data.

```bash
make seed-db
```

**What it does**:
- Creates sample users
- Creates sample embeddings
- Creates sample DNA profiles
- Useful for testing

**Equivalent to**:
```bash
docker-compose exec backend-api node scripts/seed-data.js
```

#### make reset-db

Reset database (delete all data).

```bash
make reset-db
```

**What it does**:
- Deletes all DynamoDB tables
- Recreates tables
- Clears all data
- **Warning**: This is destructive!

**Equivalent to**:
```bash
docker-compose down -v
docker volume rm vibegraph_dynamodb-data
make up
make init-db
```

## Testing Commands

#### make test

Run all tests in containers.

```bash
make test
```

**What it does**:
- Runs frontend unit tests
- Runs backend unit tests
- Runs integration tests
- Displays test results

**Equivalent to**:
```bash
docker-compose exec frontend npm run test
docker-compose exec backend-api npm run test
```

#### make test-frontend

Run frontend tests only.

```bash
make test-frontend
```

**What it does**:
- Runs frontend unit tests with Jest
- Displays test coverage
- Exits with error if tests fail

**Equivalent to**:
```bash
docker-compose exec frontend npm run test
```

#### make test-backend

Run backend tests only.

```bash
make test-backend
```

**What it does**:
- Runs backend unit tests
- Runs Lambda function tests
- Displays test coverage

**Equivalent to**:
```bash
docker-compose exec backend-api npm run test
```

#### make test-integration

Run integration tests.

```bash
make test-integration
```

**What it does**:
- Runs end-to-end tests
- Tests complete quiz flow
- Tests API endpoints
- Requires all containers to be running

**Equivalent to**:
```bash
docker-compose exec backend-api npm run test:integration
```

## Cleanup Commands

#### make clean

Remove all containers, volumes, and images.

```bash
make clean
```

**What it does**:
- Stops all containers
- Removes all containers
- Removes all volumes (deletes data)
- Removes all images
- **Warning**: This is destructive!

**Equivalent to**:
```bash
docker-compose down -v --rmi all
docker volume prune -f
```

#### make reset

Stop, clean, rebuild, and start fresh.

```bash
make reset
```

**What it does**:
- Runs `make clean`
- Rebuilds all images
- Starts all containers
- Initializes database
- Useful for complete reset

**Equivalent to**:
```bash
make clean
make build
make up
make init-db
```

## Validation Commands

#### make check-connections

Verify all inter-service connections.

```bash
make check-connections
```

**What it does**:
- Tests frontend → backend-api connection
- Tests backend-api → dynamodb-local connection
- Tests backend-api → localstack connection
- Tests backend-api → backend-services connection
- Displays connection status

#### make validate

Run health checks and connection tests.

```bash
make validate
```

**What it does**:
- Runs `make health`
- Runs `make check-connections`
- Verifies all services are operational
- Useful before running tests

#### make diagnose

Run diagnostic checks and output detailed status.

```bash
make diagnose
```

**What it does**:
- Displays container status
- Displays health check status
- Displays network configuration
- Displays volume information
- Displays resource usage
- Useful for troubleshooting

## Advanced Commands

#### make stats

View real-time resource usage.

```bash
make stats
```

**What it does**:
- Displays CPU usage per container
- Displays memory usage per container
- Displays network I/O
- Updates in real-time

**Equivalent to**:
```bash
docker stats
```

#### make prune

Remove unused Docker resources.

```bash
make prune
```

**What it does**:
- Removes stopped containers
- Removes unused images
- Removes unused volumes
- Removes unused networks
- Frees up disk space

**Equivalent to**:
```bash
docker system prune -a --volumes -f
```

## Example Workflows

### Initial Setup

```bash
# Clone repository
git clone https://github.com/your-org/vibegraph.git
cd vibegraph

# Build and start containers
make build
make up

# Wait for containers to be healthy
make wait-healthy

# Initialize database
make init-db

# Verify everything is working
make health
make check-connections

# Open application
open http://localhost:5173
```

### Daily Development

```bash
# Start containers
make up

# View logs
make logs

# Make code changes (hot reload enabled)

# Run tests
make test

# Stop containers at end of day
make down
```

### Debugging Issues

```bash
# Check container status
make ps

# View logs for specific service
make logs-backend

# Open shell in container
make shell-backend

# Run diagnostic checks
make diagnose

# Restart containers
make restart
```

### Testing Changes

```bash
# Start containers
make up

# Run tests
make test

# Run integration tests
make test-integration

# Check health
make health

# Stop containers
make down
```

### Complete Reset

```bash
# Clean everything
make clean

# Rebuild and start fresh
make reset

# Verify everything works
make validate
```

## Makefile Implementation

### Basic Structure

```makefile
.PHONY: build up down restart logs clean

# Build all images
build:
	docker-compose build

# Start all containers
up:
	docker-compose up -d

# Stop all containers
down:
	docker-compose down

# Restart all containers
restart:
	docker-compose restart

# View logs
logs:
	docker-compose logs -f

# Clean everything
clean:
	docker-compose down -v --rmi all
	docker volume prune -f
```

### Advanced Targets

```makefile
# Wait for containers to be healthy
wait-healthy:
	@echo "Waiting for containers to be healthy..."
	@timeout=120; \
	elapsed=0; \
	while [ $$elapsed -lt $$timeout ]; do \
		if docker-compose ps | grep -q "unhealthy"; then \
			echo "Waiting... ($$elapsed/$$timeout seconds)"; \
			sleep 5; \
			elapsed=$$((elapsed + 5)); \
		else \
			echo "All containers are healthy!"; \
			exit 0; \
		fi; \
	done; \
	echo "Timeout waiting for containers to be healthy"; \
	exit 1

# Check connections
check-connections:
	@echo "Checking frontend → backend-api..."
	@docker-compose exec -T frontend wget -O- http://backend-api:3000/health
	@echo "Checking backend-api → dynamodb-local..."
	@docker-compose exec -T backend-api curl -f http://dynamodb-local:8000
	@echo "Checking backend-api → localstack..."
	@docker-compose exec -T backend-api curl -f http://localstack:4566/_localstack/health
	@echo "All connections verified!"
```

## Troubleshooting

### Make Command Not Found

```bash
# Install make on macOS
brew install make

# Install make on Ubuntu/Debian
sudo apt-get install make

# Install make on Windows (use WSL or Git Bash)
```

### Permission Denied

```bash
# Fix permissions on Makefile
chmod +x Makefile

# Or run with sudo (not recommended)
sudo make up
```

### Target Not Found

```bash
# List all available targets
make help

# Or view Makefile
cat Makefile
```

## Best Practices

1. **Use make commands** instead of docker-compose directly for consistency
2. **Run `make health`** before running tests to ensure containers are ready
3. **Use `make logs`** to debug issues instead of checking individual containers
4. **Run `make clean`** periodically to free up disk space
5. **Use `make reset`** when switching branches or after major changes
6. **Add custom targets** to Makefile for project-specific workflows

## Next Steps

- See [docker.md](./docker.md) for container details
- See [docker-compose.md](./docker-compose.md) for orchestration
- See [networking.md](./networking.md) for network configuration
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment

## References

- [GNU Make Documentation](https://www.gnu.org/software/make/manual/)
- [Docker Compose CLI Reference](https://docs.docker.com/compose/reference/)
- [Makefile Tutorial](https://makefiletutorial.com/)
