#!/bin/bash

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}VibeGraph Backend Implementation Test${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Step 1: Build containers
echo -e "${YELLOW}Step 1: Building containers...${NC}"
make build
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Build successful${NC}"
echo ""

# Step 2: Start containers
echo -e "${YELLOW}Step 2: Starting containers...${NC}"
make up
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Failed to start containers${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Containers started${NC}"
echo ""

# Step 3: Wait for health
echo -e "${YELLOW}Step 3: Waiting for containers to be healthy...${NC}"
make wait-healthy
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Containers failed health check${NC}"
    docker-compose ps
    exit 1
fi
echo -e "${GREEN}✓ All containers healthy${NC}"
echo ""

# Step 4: Initialize database
echo -e "${YELLOW}Step 4: Initializing database...${NC}"
make init-db
if [ $? -ne 0 ]; then
    echo -e "${RED}✗ Database initialization failed${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Database initialized${NC}"
echo ""

# Step 5: Run backend tests
echo -e "${YELLOW}Step 5: Running backend unit tests...${NC}"
docker-compose run --rm backend-tests
TEST_RESULT=$?
echo ""

if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}✓ ALL TESTS PASSED!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "${BLUE}Backend implementation is complete and working!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Test API manually: curl -X POST http://localhost:8000/quiz/section1/start -H 'Content-Type: application/json' -d '{}'"
    echo "  2. View API docs: http://localhost:8000/docs"
    echo "  3. Check logs: make logs-backend"
    echo "  4. Run integration tests: make test-integration"
else
    echo -e "${RED}========================================${NC}"
    echo -e "${RED}✗ TESTS FAILED${NC}"
    echo -e "${RED}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Check the test output above for details${NC}"
    exit 1
fi
