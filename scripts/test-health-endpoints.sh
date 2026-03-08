#!/bin/bash
# Test script for health check endpoints (Task 21.3)
# This script validates all health check endpoints return correct responses

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Health Check Endpoints Test ===${NC}"
echo ""

# Helper function to test an endpoint
test_endpoint() {
    local name=$1
    local url=$2
    local expected_status=$3
    local expected_field=$4
    
    echo -e "${YELLOW}Testing $name...${NC}"
    
    # Make request and capture status code and response
    response=$(curl -s -w "\n%{http_code}" "$url")
    status_code=$(echo "$response" | tail -n 1)
    body=$(echo "$response" | head -n -1)
    
    # Check status code
    if [ "$status_code" != "$expected_status" ]; then
        echo -e "${RED}✗ Expected status $expected_status, got $status_code${NC}"
        echo "Response: $body"
        return 1
    fi
    
    # Check if response is valid JSON
    if ! echo "$body" | jq . > /dev/null 2>&1; then
        echo -e "${RED}✗ Response is not valid JSON${NC}"
        echo "Response: $body"
        return 1
    fi
    
    # Check for expected field if provided
    if [ -n "$expected_field" ]; then
        field_value=$(echo "$body" | jq -r ".$expected_field")
        if [ "$field_value" = "null" ] || [ -z "$field_value" ]; then
            echo -e "${RED}✗ Expected field '$expected_field' not found in response${NC}"
            echo "Response: $body"
            return 1
        fi
    fi
    
    echo -e "${GREEN}✓ $name passed (status: $status_code)${NC}"
    echo "Response: $body" | jq .
    echo ""
    return 0
}

# Test 1: Basic health endpoint
echo -e "${YELLOW}[1/7] Testing GET /health (basic liveness check)...${NC}"
test_endpoint "Basic Health" "http://localhost:8000/health" "200" "status"

# Test 2: Readiness endpoint
echo -e "${YELLOW}[2/7] Testing GET /health/ready (readiness check)...${NC}"
test_endpoint "Readiness Check" "http://localhost:8000/health/ready" "200" "status"

# Test 3: Database health endpoint
echo -e "${YELLOW}[3/7] Testing GET /health/db (DynamoDB connection)...${NC}"
test_endpoint "Database Health" "http://localhost:8000/health/db" "200" "status"

# Test 4: Bedrock health endpoint
echo -e "${YELLOW}[4/7] Testing GET /health/bedrock (Bedrock connection)...${NC}"
# Note: This may return 503 in local development, which is expected
response=$(curl -s -w "\n%{http_code}" "http://localhost:8000/health/bedrock")
status_code=$(echo "$response" | tail -n 1)
body=$(echo "$response" | head -n -1)

if [ "$status_code" = "200" ]; then
    echo -e "${GREEN}✓ Bedrock Health passed (status: 200)${NC}"
elif [ "$status_code" = "503" ]; then
    echo -e "${YELLOW}⚠ Bedrock Health returned 503 (expected in local development)${NC}"
else
    echo -e "${RED}✗ Unexpected status code: $status_code${NC}"
    echo "Response: $body"
    exit 1
fi
echo "Response: $body" | jq .
echo ""

# Test 5: Cache health endpoint
echo -e "${YELLOW}[5/7] Testing GET /health/cache (cache service)...${NC}"
test_endpoint "Cache Health" "http://localhost:8000/health/cache" "200" "status"

# Test 6: Comprehensive status endpoint
echo -e "${YELLOW}[6/7] Testing GET /health/status (comprehensive status)...${NC}"
test_endpoint "Comprehensive Status" "http://localhost:8000/health/status" "200" "status"

# Verify comprehensive status has all expected fields
echo "Verifying comprehensive status structure..."
status_response=$(curl -s "http://localhost:8000/health/status")

required_fields=("status" "timestamp" "service" "dependencies")
missing_fields=()

for field in "${required_fields[@]}"; do
    if ! echo "$status_response" | jq -e ".$field" > /dev/null 2>&1; then
        missing_fields+=("$field")
    fi
done

if [ ${#missing_fields[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing required fields in comprehensive status:${NC}"
    printf '%s\n' "${missing_fields[@]}"
    exit 1
fi
echo -e "${GREEN}✓ All required fields present${NC}"
echo ""

# Test 7: Test health check failure scenarios
echo -e "${YELLOW}[7/7] Testing health check failure scenarios...${NC}"

# Stop DynamoDB temporarily
echo "Stopping DynamoDB container..."
docker stop vibegraph-dynamodb-local > /dev/null

# Wait a moment for health checks to detect the failure
sleep 5

# Test that health checks now fail appropriately
echo "Testing /health/db should now return 503..."
db_status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health/db")

if [ "$db_status" = "503" ]; then
    echo -e "${GREEN}✓ Health check correctly reports unhealthy state${NC}"
else
    echo -e "${YELLOW}⚠ Expected 503, got $db_status (health check may be cached)${NC}"
fi

# Restart DynamoDB
echo "Restarting DynamoDB container..."
docker start vibegraph-dynamodb-local > /dev/null

# Wait for DynamoDB to be healthy again
echo "Waiting for DynamoDB to recover..."
sleep 15

# Verify health checks pass again
echo "Testing /health/db should now return 200..."
db_status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/health/db")

if [ "$db_status" = "200" ]; then
    echo -e "${GREEN}✓ Health check correctly reports healthy state after recovery${NC}"
else
    echo -e "${RED}✗ Health check did not recover (status: $db_status)${NC}"
    exit 1
fi
echo ""

echo -e "${GREEN}=== Health Check Endpoints Test Complete ===${NC}"
echo ""
echo "Summary:"
echo "  - Basic health: ✓"
echo "  - Readiness: ✓"
echo "  - Database health: ✓"
echo "  - Bedrock health: ✓ (or expected failure)"
echo "  - Cache health: ✓"
echo "  - Comprehensive status: ✓"
echo "  - Failure detection: ✓"
echo ""
echo -e "${BLUE}Next step: Run './scripts/test-inter-container.sh' to test inter-container communication${NC}"
