# Container Orchestration Testing Guide

This guide explains how to test the VibeGraph Docker containerization setup to ensure all services are working correctly.

## Overview

The testing suite consists of 7 test scripts that validate different aspects of the containerized system:

1. **Build Process Validation** - Ensures all Docker images build successfully
2. **Container Startup** - Validates containers start and reach healthy state
3. **Health Endpoints** - Tests all health check endpoints
4. **Inter-Container Communication** - Validates network connectivity
5. **Connection Resilience** - Tests failure handling and recovery
6. **API Endpoints** - Validates all API endpoints are accessible
7. **Health Monitoring** - Continuous monitoring dashboard

## Quick Start

### Run All Tests

To run the complete test suite:

```bash
./scripts/run-all-tests.sh
```

This will run all tests in sequence and provide a comprehensive summary.

### Run Individual Tests

To run specific tests:

```bash
# Test 1: Build validation
./scripts/test-build.sh

# Test 2: Container startup
./scripts/test-startup.sh

# Test 3: Health endpoints
./scripts/test-health-endpoints.sh

# Test 4: Inter-container communication
./scripts/test-inter-container.sh

# Test 5: Connection resilience
./scripts/test-resilience.sh

# Test 6: API endpoints
./scripts/test-api-endpoints.sh

# Test 7: Health monitoring (continuous)
./scripts/monitor-health.sh
# or
make monitor
```

## Prerequisites

Before running tests:

1. **Docker and Docker Compose installed**
   ```bash
   docker --version
   docker-compose --version
   ```

2. **Build all images**
   ```bash
   make build
   ```

3. **Sufficient system resources**
   - Minimum 4GB RAM
   - 10GB free disk space
   - Docker daemon running

## Test Details

### 1. Build Process Validation

**Script**: `scripts/test-build.sh`

**Purpose**: Validates that all Docker images build without errors.

**What it checks**:
- docker-compose.yml configuration is valid
- All images build successfully
- Image sizes are reasonable (< 2GB)
- All expected images exist
- Build cache is effective

**Expected duration**: 5-10 minutes (first build), 30 seconds (cached)

**Success criteria**:
- All images build without errors
- No missing images
- Build cache reduces rebuild time

**Common issues**:
- **Build fails**: Check Dockerfile syntax, dependencies
- **Large images**: Review Dockerfile optimization
- **Cache ineffective**: Check layer ordering in Dockerfile

---

### 2. Container Startup and Health Checks

**Script**: `scripts/test-startup.sh`

**Purpose**: Validates containers start properly and reach healthy state.

**What it checks**:
- All containers start successfully
- Health checks pass within 120 seconds
- All expected containers are running
- Automatic restart policy works

**Expected duration**: 2-3 minutes

**Success criteria**:
- All containers running
- All health checks pass
- Restart policy functional

**Common issues**:
- **Timeout**: Increase timeout, check system resources
- **Unhealthy containers**: Check logs with `make logs`
- **Restart fails**: Verify restart policy in docker-compose.yml

---

### 3. Health Check Endpoints

**Script**: `scripts/test-health-endpoints.sh`

**Purpose**: Validates all health check endpoints return correct responses.

**What it checks**:
- GET /health - Basic liveness (200)
- GET /health/ready - Readiness with dependencies (200)
- GET /health/db - DynamoDB connection (200)
- GET /health/bedrock - Bedrock connection (200 or 503)
- GET /health/cache - Cache service (200)
- GET /health/status - Comprehensive status (200)
- Failure detection works correctly

**Expected duration**: 1-2 minutes

**Success criteria**:
- All endpoints return valid JSON
- Status codes are correct
- Failure detection works

**Common issues**:
- **503 from Bedrock**: Expected in local development
- **Connection refused**: Ensure containers are running
- **Invalid JSON**: Check backend logs

---

### 4. Inter-Container Communication

**Script**: `scripts/test-inter-container.sh`

**Purpose**: Validates containers can communicate via Docker network.

**What it checks**:
- Docker network exists
- Frontend → Backend communication
- Backend → DynamoDB communication
- Backend → LocalStack communication
- DNS resolution works
- Network latency is acceptable

**Expected duration**: 1 minute

**Success criteria**:
- All connections work
- DNS resolves correctly
- Latency < 1 second

**Common issues**:
- **Connection refused**: Check network configuration
- **DNS fails**: Verify service names in docker-compose.yml
- **High latency**: Check system resources

---

### 5. Connection Resilience

**Script**: `scripts/test-resilience.sh`

**Purpose**: Validates system handles failures gracefully.

**What it checks**:
- DynamoDB failure detection and recovery
- Backend restart resilience
- Transient failure handling
- Graceful degradation

**Expected duration**: 3-4 minutes

**Success criteria**:
- Failures detected within 10 seconds
- Automatic recovery works
- System operates in degraded mode

**Common issues**:
- **No recovery**: Check health check configuration
- **Slow recovery**: Increase wait times
- **Degradation fails**: Verify optional service handling

**Note**: This test temporarily stops containers to simulate failures.

---

### 6. API Endpoints End-to-End

**Script**: `scripts/test-api-endpoints.sh`

**Purpose**: Validates all API endpoints are accessible.

**What it checks**:
- All health endpoints
- Quiz endpoints (Section 1, Section 2, Complete)
- Profile endpoints (DNA, Path, Matches, Analytics)
- CORS headers

**Expected duration**: 1 minute

**Success criteria**:
- All endpoints accessible
- Valid responses (may be 404/500 without AWS)
- CORS headers present

**Common issues**:
- **404/500 responses**: Expected without full AWS setup
- **CORS missing**: Check CORS configuration in backend
- **Timeout**: Check backend logs

**Note**: This validates endpoint accessibility, not full functionality.

---

### 7. Health Monitoring Dashboard

**Script**: `scripts/monitor-health.sh`

**Purpose**: Continuous monitoring of all services.

**Features**:
- Real-time health status display
- Container status monitoring
- Service connectivity checks
- Status change alerts
- Health check history logging

**Usage**:
```bash
./scripts/monitor-health.sh
# or
make monitor
```

**Controls**:
- Press Ctrl+C to exit

**Log files**:
- `logs/health-monitor.log` - Complete history
- `logs/health-alerts.log` - Status changes only

**Display**:
- Green ● - Healthy
- Yellow ● - Degraded
- Red ● - Unhealthy/Unreachable

---

## Test Output

All test scripts provide:

- **Color-coded output**:
  - Green: Success
  - Red: Failure
  - Yellow: Warning
  - Blue: Information

- **Progress indicators**: Shows current test step

- **Detailed results**: Explains what was tested and results

- **Summary**: Overall pass/fail status

- **Next steps**: Suggestions for what to do next

## Interpreting Results

### All Tests Pass ✓

Your system is working correctly! You can:
- Access frontend at http://localhost:3000
- Access backend API at http://localhost:8000
- Start development work
- Run monitoring dashboard

### Some Tests Fail ✗

Check the following:

1. **Container logs**:
   ```bash
   make logs
   make logs-backend
   make logs-frontend
   ```

2. **Container status**:
   ```bash
   make ps
   make health
   ```

3. **Diagnostics**:
   ```bash
   make diagnose
   ```

4. **Common issues**:
   - Insufficient resources: Increase Docker memory/CPU
   - Port conflicts: Check if ports 3000, 8000, 8001, 4566 are available
   - Network issues: Recreate network with `make down && make up`

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

### GitHub Actions Example

```yaml
name: Container Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Build images
        run: ./scripts/test-build.sh
      
      - name: Test startup
        run: ./scripts/test-startup.sh
      
      - name: Test health endpoints
        run: ./scripts/test-health-endpoints.sh
      
      - name: Test communication
        run: ./scripts/test-inter-container.sh
      
      - name: Test resilience
        run: ./scripts/test-resilience.sh
      
      - name: Test API endpoints
        run: ./scripts/test-api-endpoints.sh
```

### GitLab CI Example

```yaml
test:
  stage: test
  script:
    - ./scripts/run-all-tests.sh
  artifacts:
    paths:
      - logs/
    when: always
```

## Automated Testing Schedule

For production environments, consider:

1. **Pre-deployment**: Run all tests before deploying
2. **Post-deployment**: Run health checks after deploying
3. **Continuous monitoring**: Run monitoring dashboard 24/7
4. **Scheduled tests**: Run full suite daily/weekly

## Troubleshooting

### Tests hang or timeout

**Cause**: Insufficient resources or slow startup

**Solution**:
- Increase Docker memory allocation
- Increase test timeouts
- Check system resources with `docker stats`

### Network tests fail

**Cause**: Network configuration issues

**Solution**:
- Recreate network: `make down && make up`
- Check network exists: `docker network ls`
- Verify service names in docker-compose.yml

### Health checks never pass

**Cause**: Service not starting correctly

**Solution**:
- Check logs: `make logs`
- Verify health check configuration
- Test health endpoint manually: `curl http://localhost:8000/health`

### API tests return 500/503

**Cause**: Missing AWS credentials or Bedrock unavailable

**Solution**:
- This is expected in local development
- Tests validate accessibility, not full functionality
- For full testing, configure AWS credentials

## Best Practices

1. **Run tests after changes**: Always run tests after modifying Docker configuration

2. **Monitor during development**: Keep monitoring dashboard running

3. **Check logs regularly**: Review logs for warnings and errors

4. **Test resilience**: Periodically test failure scenarios

5. **Update tests**: Keep tests updated when adding new services

## Additional Resources

- [Docker Setup Guide](docker-setup.md)
- [Docker Compose Configuration](docker-compose.md)
- [Health Check System](../api/health-endpoints.md)
- [Troubleshooting Guide](../TROUBLESHOOTING.md)
- [Test Scripts README](../../scripts/README.md)

## Support

For issues or questions:
- Check logs: `make logs`
- Run diagnostics: `make diagnose`
- Review documentation in `docs/` directory
- Check test script README: `scripts/README.md`
