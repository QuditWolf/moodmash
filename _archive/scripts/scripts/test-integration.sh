#!/bin/bash
# Comprehensive Integration Testing Script

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║              COMPREHENSIVE INTEGRATION TESTING                               ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASSED=0
FAILED=0

test_endpoint() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "Testing $name... "
    result=$(eval "$command" 2>&1)
    
    if echo "$result" | grep -q "$expected"; then
        echo -e "${GREEN}✅ PASS${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ FAIL${NC}"
        echo "  Expected: $expected"
        echo "  Got: $result"
        ((FAILED++))
        return 1
    fi
}

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "1. Container Health Checks"
echo "═══════════════════════════════════════════════════════════════════════════════"

test_endpoint "Frontend Container" "docker ps --filter name=vibegraph-frontend --format '{{.Status}}'" "healthy"
test_endpoint "Backend API Container" "docker ps --filter name=vibegraph-backend-api --format '{{.Status}}'" "healthy"
test_endpoint "DynamoDB Container" "docker ps --filter name=vibegraph-dynamodb-local --format '{{.Status}}'" "healthy"
test_endpoint "LocalStack Container" "docker ps --filter name=vibegraph-localstack --format '{{.Status}}'" "healthy"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "2. Backend API Endpoints"
echo "═══════════════════════════════════════════════════════════════════════════════"

test_endpoint "Health Endpoint" "curl -s http://localhost:8000/health" "healthy"
test_endpoint "Ready Endpoint" "curl -s http://localhost:8000/health/ready" "ready"
test_endpoint "Quiz Section1 Start" "curl -s -X POST http://localhost:8000/quiz/section1/start -H 'Content-Type: application/json' -d '{}'" "sessionId"
test_endpoint "Profile DNA Endpoint" "curl -s http://localhost:8000/profile/dna/test-user" "tasteDNA"
test_endpoint "Profile Path Endpoint" "curl -s http://localhost:8000/profile/path/test-user" "path"
test_endpoint "Profile Matches Endpoint" "curl -s http://localhost:8000/profile/matches/test-user" "matches"
test_endpoint "Profile Analytics Endpoint" "curl -s http://localhost:8000/profile/analytics/test-user" "analytics"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "3. Frontend"
echo "═══════════════════════════════════════════════════════════════════════════════"

test_endpoint "Frontend Serving" "curl -s http://localhost:3000" "VibeGraph"
test_endpoint "Frontend Title" "curl -s http://localhost:3000" "<title>"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "4. DynamoDB Tables"
echo "═══════════════════════════════════════════════════════════════════════════════"

test_endpoint "Users Table" "docker exec vibegraph-backend-api python3 -c 'import boto3; print(boto3.client(\"dynamodb\", endpoint_url=\"http://dynamodb-local:8000\", region_name=\"us-east-1\").list_tables()[\"TableNames\"])'" "vibegraph-users"
test_endpoint "Sessions Table" "docker exec vibegraph-backend-api python3 -c 'import boto3; print(boto3.client(\"dynamodb\", endpoint_url=\"http://dynamodb-local:8000\", region_name=\"us-east-1\").list_tables()[\"TableNames\"])'" "vibegraph-sessions"
test_endpoint "Cache Table" "docker exec vibegraph-backend-api python3 -c 'import boto3; print(boto3.client(\"dynamodb\", endpoint_url=\"http://dynamodb-local:8000\", region_name=\"us-east-1\").list_tables()[\"TableNames\"])'" "vibegraph-embedding-cache"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "5. Inter-Container Communication"
echo "═══════════════════════════════════════════════════════════════════════════════"

test_endpoint "Backend → DynamoDB" "docker exec vibegraph-backend-api curl -s http://dynamodb-local:8000" "DynamoDB"
test_endpoint "Backend → LocalStack" "docker exec vibegraph-backend-api curl -s http://localstack:4566/_localstack/health" "running"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "6. API Documentation"
echo "═══════════════════════════════════════════════════════════════════════════════"

test_endpoint "Swagger UI" "curl -s http://localhost:8000/docs" "swagger"
test_endpoint "OpenAPI Schema" "curl -s http://localhost:8000/openapi.json" "openapi"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "7. CORS Configuration"
echo "═══════════════════════════════════════════════════════════════════════════════"

test_endpoint "CORS Headers" "curl -s -I -X OPTIONS http://localhost:8000/quiz/section1/start -H 'Origin: http://localhost:3000'" "access-control-allow-origin"

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                            TEST RESULTS                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "  ${GREEN}Passed: $PASSED${NC}"
echo -e "  ${RED}Failed: $FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ ALL TESTS PASSED!${NC}"
    echo ""
    echo "System is fully integrated and working correctly."
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED!${NC}"
    echo ""
    echo "Please check the failed tests above and review logs:"
    echo "  docker logs vibegraph-backend-api"
    echo "  docker logs vibegraph-frontend"
    exit 1
fi
