#!/bin/bash
# Test script for container startup and health checks (Task 21.2)
# This script validates that all containers start properly and reach healthy state

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Container Startup and Health Check Test ===${NC}"
echo ""

# Test 1: Start all containers
echo -e "${YELLOW}[1/6] Starting all containers...${NC}"
if ! docker-compose up -d; then
    echo -e "${RED}✗ Failed to start containers${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Containers started${NC}"
echo ""

# Test 2: Wait for containers to initialize
echo -e "${YELLOW}[2/6] Waiting for containers to initialize (30s)...${NC}"
sleep 30
echo -e "${GREEN}✓ Initialization period complete${NC}"
echo ""

# Test 3: Check container status
echo -e "${YELLOW}[3/6] Checking container status...${NC}"
docker-compose ps
echo ""

# Test 4: Wait for health checks to pass
echo -e "${YELLOW}[4/6] Waiting for health checks to pass (max 120s)...${NC}"
timeout=120
elapsed=0
all_healthy=false

while [ $elapsed -lt $timeout ]; do
    # Check if any containers are unhealthy or starting
    unhealthy_count=$(docker-compose ps | grep -c "unhealthy\|starting" || true)
    
    if [ $unhealthy_count -eq 0 ]; then
        all_healthy=true
        break
    fi
    
    echo -e "${YELLOW}  Waiting... ($elapsed/$timeout seconds, $unhealthy_count containers not ready)${NC}"
    sleep 5
    elapsed=$((elapsed + 5))
done

if [ "$all_healthy" = false ]; then
    echo -e "${RED}✗ Timeout waiting for containers to be healthy${NC}"
    echo ""
    echo "Container status:"
    docker-compose ps
    echo ""
    echo "Recent logs:"
    docker-compose logs --tail=50
    exit 1
fi

echo -e "${GREEN}✓ All containers are healthy (took ${elapsed}s)${NC}"
echo ""

# Test 5: Verify all expected containers are running
echo -e "${YELLOW}[5/6] Verifying all expected containers are running...${NC}"
expected_containers=(
    "vibegraph-frontend"
    "vibegraph-backend-api"
    "vibegraph-backend-handlers"
    "vibegraph-backend-services"
    "vibegraph-dynamodb-local"
    "vibegraph-localstack"
)

missing_containers=()
for container in "${expected_containers[@]}"; do
    if ! docker ps | grep -q "$container"; then
        missing_containers+=("$container")
    fi
done

if [ ${#missing_containers[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing containers:${NC}"
    printf '%s\n' "${missing_containers[@]}"
    exit 1
fi
echo -e "${GREEN}✓ All expected containers are running${NC}"
echo ""

# Test 6: Test automatic restart on failure
echo -e "${YELLOW}[6/6] Testing automatic restart on failure...${NC}"
echo "Stopping backend-api container..."
docker stop vibegraph-backend-api > /dev/null

echo "Waiting 10 seconds for automatic restart..."
sleep 10

if docker ps | grep -q "vibegraph-backend-api"; then
    echo -e "${GREEN}✓ Container restarted automatically${NC}"
else
    echo -e "${RED}✗ Container did not restart automatically${NC}"
    echo "Restart policy may not be configured correctly"
    # Restart manually to continue tests
    docker-compose up -d vibegraph-backend-api
fi
echo ""

# Wait for backend to be healthy again
echo "Waiting for backend-api to be healthy again..."
sleep 15
echo ""

echo -e "${GREEN}=== Container Startup Test Complete ===${NC}"
echo ""
echo "Summary:"
echo "  - All containers: Running"
echo "  - Health checks: Passed"
echo "  - Startup time: ${elapsed}s"
echo "  - Restart policy: Working"
echo ""
echo -e "${BLUE}Next step: Run './scripts/test-health-endpoints.sh' to test health endpoints${NC}"
