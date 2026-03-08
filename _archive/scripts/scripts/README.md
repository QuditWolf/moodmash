# Test Scripts for Container Orchestration and Health

This directory contains comprehensive test scripts for validating the VibeGraph Docker containerization setup. These scripts test various aspects of the system including build process, container startup, health checks, inter-container communication, resilience, and API endpoints.

## Overview

All test scripts are designed to be run **after** the Docker build is complete. They validate that the system is working correctly without requiring full AWS Bedrock integration.

## Test Scripts

### 1. test-build.sh - Build Process Validation (Task 21.1)

**Purpose**: Validates that all Docker images build successfully without errors.

**What it tests**:
- docker-compose.yml configuration validity
- All Docker images build without errors
- Image sizes are reasonable (warns if > 2GB)
- All expected images exist
- Build cache effectiveness

**Usage**:
```bash
./scripts/test-build.sh
```

**Expected outcome**: All images build successfully, no missing images, reasonable sizes.

---

### 2. test-startup.sh - Container Startup and Health Checks (Task 21.2)

**Purpose**: Validates that all containers start properly and reach healthy state.

**What it tests**:
- All containers start successfully
- Health checks pass within timeout (120s)
- All expected containers are running
- Automatic restart on failure works

**Usage**:
```bash
./scripts/test-startup.sh
```

**Expected outcome**: All containers running and healthy within 120 seconds.

**Note**: This script will temporarily stop and restart the backend-api container to test the restart policy.

---

### 3. test-health-endpoints.sh - Health Check Endpoints (Task 21.3)

**Purpose**: Validates all health check endpoints return correct responses.

**What it tests**:
- GET /health - Basic liveness check (200)
- GET /health/ready - Readiness check with dependencies (200)
- GET /health/db - DynamoDB connection status (200)
- GET /health/bedrock - Bedrock connection status (200 or 503 in local dev)
- GET /health/cache - Cache service status (200)
- GET /health/status - Comprehensive status with all dependencies (200)
- Health check failure detection (stops DynamoDB temporarily)

**Usage**:
```bash
./scripts/test-health-endpoints.sh
```

**Expected outcome**: All health endpoints return valid JSON responses with correct status codes.

**Note**: Bedrock health may return 503 in local development (expected behavior).

---

### 4. test-inter-container.sh - Inter-Container Communication (Task 21.4)

**Purpose**: Validates that containers can communicate with each other via Docker network.

**What it tests**:
- Docker network (vibegraph-network) exists
- Frontend can reach backend-api
- Backend-api can reach dynamodb-local
- Backend-api can reach localstack
- DNS resolution works for all service names
- Network latency is acceptable (< 1s)

**Usage**:
```bash
./scripts/test-inter-container.sh
```

**Expected outcome**: All inter-container connections work, DNS resolves correctly, latency is low.

---

### 5. test-resilience.sh - Connection Resilience (Task 21.5)

**Purpose**: Validates that the system handles service failures gracefully and recovers automatically.

**What it tests**:
- DynamoDB failure detection and automatic recovery
- Backend-api restart resilience
- Retry logic for transient failures
- Graceful degradation when optional services fail

**Usage**:
```bash
./scripts/test-resilience.sh
```

**Expected outcome**: System detects failures, recovers automatically, operates in degraded mode when needed.

**Note**: This script will temporarily stop and restart containers to simulate failures.

---

### 6. test-api-endpoints.sh - API Endpoints End-to-End (Task 21.6)

**Purpose**: Validates that all API endpoints are accessible and return expected responses.

**What it tests**:
- Health endpoints (all variants)
- POST /api/quiz/section1/start
- POST /api/quiz/section2/generate
- POST /api/quiz/complete
- GET /api/profile/dna/:userId
- GET /api/profile/path/:userId
- GET /api/profile/matches/:userId
- GET /api/profile/analytics/:userId
- CORS headers are present

**Usage**:
```bash
./scripts/test-api-endpoints.sh
```

**Expected outcome**: All endpoints are accessible and return valid responses (may be 404/500 without full AWS setup).

**Note**: This test validates endpoint accessibility, not full functionality. Full functional testing requires AWS Bedrock integration.

---

### 7. monitor-health.sh - Health Check Monitoring Dashboard (Task 21.7)

**Purpose**: Continuously monitors all health endpoints and displays status in real-time.

**Features**:
- Polls all health endpoints every 10 seconds
- Displays status with colors (green/red/yellow)
- Shows container status
- Tests service connectivity
- Alerts on status changes
- Logs health check history to `logs/health-monitor.log`
- Logs alerts to `logs/health-alerts.log`

**Usage**:
```bash
./scripts/monitor-health.sh
```

Or via Makefile:
```bash
make monitor
```

**Expected outcome**: Real-time dashboard showing health status of all services.

**Controls**:
- Press Ctrl+C to exit

**Log files**:
- `logs/health-monitor.log` - Complete health check history
- `logs/health-alerts.log` - Status change alerts only

---

## Running All Tests

To run all tests in sequence:

```bash
# 1. Build all images
./scripts/test-build.sh

# 2. Start containers and test startup
./scripts/test-startup.sh

# 3. Test health endpoints
./scripts/test-health-endpoints.sh

# 4. Test inter-container communication
./scripts/test-inter-container.sh

# 5. Test resilience
./scripts/test-resilience.sh

# 6. Test API endpoints
./scripts/test-api-endpoints.sh

# 7. Start monitoring (optional)
./scripts/monitor-health.sh
```

## Prerequisites

- Docker and Docker Compose installed
- All containers built (`make build`)
- Sufficient system resources (4GB RAM minimum)

## Troubleshooting

### Tests fail with "container not found"
- Ensure containers are running: `docker-compose ps`
- Start containers: `make up`

### Health checks timeout
- Increase timeout in test scripts
- Check container logs: `make logs`
- Verify system resources are sufficient

### Network tests fail
- Verify Docker network exists: `docker network ls | grep vibegraph`
- Recreate network: `make down && make up`

### API endpoint tests return 500/503
- This is expected without full AWS Bedrock setup
- Tests validate endpoint accessibility, not full functionality
- Check backend logs: `make logs-backend`

## Test Output

All test scripts provide:
- Color-coded output (green = success, red = failure, yellow = warning)
- Detailed progress information
- Summary at the end
- Next step suggestions

## Integration with CI/CD

These scripts can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Build Docker images
  run: ./scripts/test-build.sh

- name: Test container startup
  run: ./scripts/test-startup.sh

- name: Test health endpoints
  run: ./scripts/test-health-endpoints.sh

- name: Test inter-container communication
  run: ./scripts/test-inter-container.sh

- name: Test resilience
  run: ./scripts/test-resilience.sh

- name: Test API endpoints
  run: ./scripts/test-api-endpoints.sh
```

## Notes

- All scripts use `set -e` to exit on first error
- Scripts are idempotent and can be run multiple times
- Some tests temporarily stop containers to simulate failures
- Tests are designed for local development environment
- Full functional testing requires AWS credentials and Bedrock access

## Maintenance

When adding new services or endpoints:
1. Update relevant test scripts
2. Add new health check endpoints if needed
3. Update monitoring script to include new services
4. Update this README with new test information

## Support

For issues or questions:
- Check container logs: `make logs`
- Run diagnostics: `make diagnose`
- Review health status: `make health`
- Check documentation in `docs/` directory
