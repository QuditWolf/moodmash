#!/bin/bash
# Integration Test Script for VibeGraph Backend API
# Tests the complete user flow through all endpoints

set -e

API_URL="http://localhost:8000"
TEST_USER_ID="test-user-$(date +%s)"

echo "=========================================="
echo "VibeGraph Backend API Integration Test"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Health Check
echo "Test 1: Health Check"
echo "--------------------"
HEALTH_RESPONSE=$(curl -s "$API_URL/health/ready")
if echo "$HEALTH_RESPONSE" | jq -e '.status == "healthy"' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "Response: $HEALTH_RESPONSE"
fi
echo ""

# Test 2: Start Section 1
echo "Test 2: Start Section 1 Quiz"
echo "-----------------------------"
SECTION1_RESPONSE=$(curl -s -X POST "$API_URL/quiz/section1/start" \
    -H "Content-Type: application/json" \
    -d '{}')

if echo "$SECTION1_RESPONSE" | jq -e '.sessionId' > /dev/null 2>&1; then
    SESSION_ID=$(echo "$SECTION1_RESPONSE" | jq -r '.sessionId')
    echo -e "${GREEN}✓ Section 1 started successfully${NC}"
    echo "Session ID: $SESSION_ID"
    echo "Questions: $(echo "$SECTION1_RESPONSE" | jq '.questions | length')"
else
    echo -e "${RED}✗ Section 1 failed${NC}"
    echo "Response: $SECTION1_RESPONSE"
    echo ""
    echo -e "${YELLOW}NOTE: This requires AWS Bedrock access.${NC}"
    echo -e "${YELLOW}LocalStack free tier does not include Bedrock.${NC}"
    echo -e "${YELLOW}To test with real AWS Bedrock:${NC}"
    echo "  1. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env"
    echo "  2. Remove BEDROCK_ENDPOINT override (use real AWS endpoint)"
    echo "  3. Ensure AWS account has Bedrock access enabled"
    exit 0
fi
echo ""

# Test 3: Generate Section 2
echo "Test 3: Generate Section 2 Questions"
echo "-------------------------------------"
SECTION1_ANSWERS='[
    {"questionId": "q1", "selectedOptions": ["option1", "option2"]},
    {"questionId": "q2", "selectedOptions": ["option3"]},
    {"questionId": "q3", "selectedOptions": ["option1"]},
    {"questionId": "q4", "selectedOptions": ["option2", "option4"]},
    {"questionId": "q5", "selectedOptions": ["option1"]}
]'

SECTION2_RESPONSE=$(curl -s -X POST "$API_URL/quiz/section2/generate" \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\": \"$SESSION_ID\", \"section1Answers\": $SECTION1_ANSWERS}")

if echo "$SECTION2_RESPONSE" | jq -e '.questions' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Section 2 generated successfully${NC}"
    echo "Questions: $(echo "$SECTION2_RESPONSE" | jq '.questions | length')"
else
    echo -e "${RED}✗ Section 2 failed${NC}"
    echo "Response: $SECTION2_RESPONSE"
    exit 1
fi
echo ""

# Test 4: Complete Quiz
echo "Test 4: Complete Quiz and Generate Profile"
echo "-------------------------------------------"
SECTION2_ANSWERS='[
    {"questionId": "q6", "selectedOptions": ["option2"]},
    {"questionId": "q7", "selectedOptions": ["option1", "option3"]},
    {"questionId": "q8", "selectedOptions": ["option4"]},
    {"questionId": "q9", "selectedOptions": ["option2"]},
    {"questionId": "q10", "selectedOptions": ["option1", "option2"]}
]'

ALL_ANSWERS="{\"section1\": $SECTION1_ANSWERS, \"section2\": $SECTION2_ANSWERS}"

COMPLETE_RESPONSE=$(curl -s -X POST "$API_URL/quiz/complete" \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\": \"$SESSION_ID\", \"userId\": \"$TEST_USER_ID\", \"allAnswers\": $ALL_ANSWERS}")

if echo "$COMPLETE_RESPONSE" | jq -e '.embeddingId' > /dev/null 2>&1; then
    EMBEDDING_ID=$(echo "$COMPLETE_RESPONSE" | jq -r '.embeddingId')
    echo -e "${GREEN}✓ Quiz completed successfully${NC}"
    echo "Embedding ID: $EMBEDDING_ID"
    echo "Taste DNA: $(echo "$COMPLETE_RESPONSE" | jq -c '.tasteDNA')"
else
    echo -e "${RED}✗ Quiz completion failed${NC}"
    echo "Response: $COMPLETE_RESPONSE"
    exit 1
fi
echo ""

# Test 5: Get Growth Path
echo "Test 5: Get Growth Path"
echo "------------------------"
PATH_RESPONSE=$(curl -s "$API_URL/profile/path/$TEST_USER_ID")

if echo "$PATH_RESPONSE" | jq -e '.path' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Growth path generated successfully${NC}"
    echo "Path stages: $(echo "$PATH_RESPONSE" | jq '.path | length')"
else
    echo -e "${RED}✗ Growth path failed${NC}"
    echo "Response: $PATH_RESPONSE"
    exit 1
fi
echo ""

# Test 6: Find Matches
echo "Test 6: Find Matches"
echo "--------------------"
MATCHES_RESPONSE=$(curl -s "$API_URL/profile/matches/$TEST_USER_ID?limit=5")

if echo "$MATCHES_RESPONSE" | jq -e '.matches' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Matches found successfully${NC}"
    echo "Matches: $(echo "$MATCHES_RESPONSE" | jq '.matches | length')"
else
    echo -e "${RED}✗ Find matches failed${NC}"
    echo "Response: $MATCHES_RESPONSE"
    exit 1
fi
echo ""

# Test 7: Get Analytics
echo "Test 7: Get Analytics"
echo "---------------------"
ANALYTICS_RESPONSE=$(curl -s "$API_URL/profile/analytics/$TEST_USER_ID")

if echo "$ANALYTICS_RESPONSE" | jq -e '.analytics' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Analytics generated successfully${NC}"
    echo "Analytics: $(echo "$ANALYTICS_RESPONSE" | jq -c '.analytics')"
else
    echo -e "${RED}✗ Analytics failed${NC}"
    echo "Response: $ANALYTICS_RESPONSE"
    exit 1
fi
echo ""

echo "=========================================="
echo -e "${GREEN}All tests passed!${NC}"
echo "=========================================="
