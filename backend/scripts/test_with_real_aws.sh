#!/bin/bash
# Test VibeGraph Backend with Real AWS Bedrock
# This script helps you test all endpoints with real AWS credentials

set -e

echo "=========================================="
echo "VibeGraph Real AWS Bedrock Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}✗ .env file not found${NC}"
    echo ""
    echo "Please create a .env file with your AWS credentials:"
    echo "  cp .env.example .env"
    echo "  # Edit .env and add your AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY"
    echo ""
    echo "See AWS_BEDROCK_SETUP.md for detailed instructions."
    exit 1
fi

# Check if AWS credentials are set
source .env
if [ "$AWS_ACCESS_KEY_ID" == "test" ] || [ -z "$AWS_ACCESS_KEY_ID" ]; then
    echo -e "${RED}✗ AWS credentials not configured${NC}"
    echo ""
    echo "Please update .env file with your real AWS credentials:"
    echo "  AWS_ACCESS_KEY_ID=your_key_here"
    echo "  AWS_SECRET_ACCESS_KEY=your_secret_here"
    echo ""
    echo "See AWS_BEDROCK_SETUP.md for detailed instructions."
    exit 1
fi

echo -e "${GREEN}✓ AWS credentials found${NC}"
echo "  Region: $AWS_REGION"
echo ""

# Check if docker-compose.override.yml has BEDROCK_ENDPOINT commented out
if grep -q "BEDROCK_ENDPOINT=http://localstack" docker-compose.override.yml 2>/dev/null; then
    echo -e "${YELLOW}⚠ Warning: LocalStack endpoint is still configured${NC}"
    echo ""
    echo "To use real AWS Bedrock, comment out this line in docker-compose.override.yml:"
    echo "  # - BEDROCK_ENDPOINT=http://localstack:4566"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo -e "${BLUE}Starting containers...${NC}"
docker-compose up -d backend-api dynamodb-local

echo ""
echo "Waiting for services to be healthy..."
sleep 10

# Check health
echo ""
echo -e "${BLUE}Test 1: Health Check${NC}"
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health/ready)
if echo "$HEALTH_RESPONSE" | jq -e '.status == "ready"' > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Health check passed${NC}"
    
    # Check Bedrock status
    BEDROCK_STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.dependencies.bedrock.status')
    if [ "$BEDROCK_STATUS" == "healthy" ]; then
        echo -e "${GREEN}✓ Bedrock connection healthy${NC}"
    elif [ "$BEDROCK_STATUS" == "error" ]; then
        echo -e "${YELLOW}⚠ Bedrock connection has issues (this is expected with LocalStack)${NC}"
        BEDROCK_ERROR=$(echo "$HEALTH_RESPONSE" | jq -r '.dependencies.bedrock.error')
        echo "  Error: $BEDROCK_ERROR"
    fi
else
    echo -e "${RED}✗ Health check failed${NC}"
    echo "Response: $HEALTH_RESPONSE"
    exit 1
fi

echo ""
echo -e "${BLUE}Test 2: Generate Section 1 Questions (Claude)${NC}"
SECTION1_RESPONSE=$(curl -s -X POST http://localhost:8000/quiz/section1/start \
    -H "Content-Type: application/json" \
    -d '{}')

if echo "$SECTION1_RESPONSE" | jq -e '.sessionId' > /dev/null 2>&1; then
    SESSION_ID=$(echo "$SECTION1_RESPONSE" | jq -r '.sessionId')
    QUESTION_COUNT=$(echo "$SECTION1_RESPONSE" | jq '.questions | length')
    echo -e "${GREEN}✓ Section 1 generated successfully${NC}"
    echo "  Session ID: $SESSION_ID"
    echo "  Questions: $QUESTION_COUNT"
    
    # Show first question
    FIRST_QUESTION=$(echo "$SECTION1_RESPONSE" | jq -r '.questions[0].text')
    echo "  First question: ${FIRST_QUESTION:0:60}..."
else
    echo -e "${RED}✗ Section 1 generation failed${NC}"
    echo "Response: $SECTION1_RESPONSE"
    
    # Check if it's a Bedrock access error
    if echo "$SECTION1_RESPONSE" | grep -q "bedrock"; then
        echo ""
        echo -e "${YELLOW}This looks like a Bedrock access issue.${NC}"
        echo "Please check:"
        echo "  1. AWS credentials are correct in .env"
        echo "  2. Bedrock models are enabled in your AWS account"
        echo "  3. IAM user has Bedrock permissions"
        echo ""
        echo "See AWS_BEDROCK_SETUP.md for detailed instructions."
    fi
    exit 1
fi

echo ""
echo -e "${BLUE}Test 3: Generate Section 2 Questions (Claude)${NC}"
SECTION1_ANSWERS='[
    {"questionId": "q1", "selectedOptions": ["option1"]},
    {"questionId": "q2", "selectedOptions": ["option2"]},
    {"questionId": "q3", "selectedOptions": ["option1"]},
    {"questionId": "q4", "selectedOptions": ["option3"]},
    {"questionId": "q5", "selectedOptions": ["option2"]}
]'

SECTION2_RESPONSE=$(curl -s -X POST http://localhost:8000/quiz/section2/generate \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\": \"$SESSION_ID\", \"section1Answers\": $SECTION1_ANSWERS}")

if echo "$SECTION2_RESPONSE" | jq -e '.questions' > /dev/null 2>&1; then
    QUESTION_COUNT=$(echo "$SECTION2_RESPONSE" | jq '.questions | length')
    echo -e "${GREEN}✓ Section 2 generated successfully${NC}"
    echo "  Questions: $QUESTION_COUNT"
else
    echo -e "${RED}✗ Section 2 generation failed${NC}"
    echo "Response: $SECTION2_RESPONSE"
    exit 1
fi

echo ""
echo -e "${BLUE}Test 4: Complete Quiz (Titan + Claude)${NC}"
TEST_USER_ID="test-user-$(date +%s)"
SECTION2_ANSWERS='[
    {"questionId": "q6", "selectedOptions": ["option1"]},
    {"questionId": "q7", "selectedOptions": ["option2"]},
    {"questionId": "q8", "selectedOptions": ["option3"]},
    {"questionId": "q9", "selectedOptions": ["option1"]},
    {"questionId": "q10", "selectedOptions": ["option2"]}
]'

ALL_ANSWERS="{\"section1\": $SECTION1_ANSWERS, \"section2\": $SECTION2_ANSWERS}"

COMPLETE_RESPONSE=$(curl -s -X POST http://localhost:8000/quiz/complete \
    -H "Content-Type: application/json" \
    -d "{\"sessionId\": \"$SESSION_ID\", \"userId\": \"$TEST_USER_ID\", \"allAnswers\": $ALL_ANSWERS}")

if echo "$COMPLETE_RESPONSE" | jq -e '.embeddingId' > /dev/null 2>&1; then
    EMBEDDING_ID=$(echo "$COMPLETE_RESPONSE" | jq -r '.embeddingId')
    ARCHETYPE=$(echo "$COMPLETE_RESPONSE" | jq -r '.tasteDNA.archetype')
    echo -e "${GREEN}✓ Quiz completed successfully${NC}"
    echo "  User ID: $TEST_USER_ID"
    echo "  Embedding ID: $EMBEDDING_ID"
    echo "  Archetype: $ARCHETYPE"
else
    echo -e "${RED}✗ Quiz completion failed${NC}"
    echo "Response: $COMPLETE_RESPONSE"
    exit 1
fi

echo ""
echo -e "${BLUE}Test 5: Generate DNA Card Image (Titan Image)${NC}"
echo "This may take 10-30 seconds..."

DNA_CARD_RESPONSE=$(curl -s -X POST "http://localhost:8000/profile/dna-card/$TEST_USER_ID?model=titan" \
    -H "Content-Type: application/json")

if echo "$DNA_CARD_RESPONSE" | jq -e '.imageId' > /dev/null 2>&1; then
    IMAGE_ID=$(echo "$DNA_CARD_RESPONSE" | jq -r '.imageId')
    IMAGE_SIZE=$(echo "$DNA_CARD_RESPONSE" | jq -r '.imageData' | wc -c)
    IMAGE_MODEL=$(echo "$DNA_CARD_RESPONSE" | jq -r '.model')
    echo -e "${GREEN}✓ DNA card image generated successfully${NC}"
    echo "  Image ID: $IMAGE_ID"
    echo "  Model: $IMAGE_MODEL"
    echo "  Size: $IMAGE_SIZE bytes (base64)"
    echo "  Dimensions: 1024x1024"
    
    # Save image to file
    IMAGE_FILE="dna-card-${TEST_USER_ID}.png"
    echo "$DNA_CARD_RESPONSE" | jq -r '.imageData' | base64 -d > "$IMAGE_FILE"
    echo -e "${GREEN}✓ Image saved to: $IMAGE_FILE${NC}"
else
    echo -e "${YELLOW}⚠ DNA card generation failed (this is optional)${NC}"
    echo "Response: $DNA_CARD_RESPONSE"
    echo ""
    echo "This might be because:"
    echo "  1. Titan Image Generator is not enabled in your AWS account"
    echo "  2. You don't have permissions for image generation"
    echo "  3. The model is not available in your region"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}All core tests passed!${NC}"
echo "=========================================="
echo ""
echo "Your VibeGraph backend is working with real AWS Bedrock!"
echo ""
echo "Next steps:"
echo "  1. Test other endpoints (matches, analytics, growth path)"
echo "  2. Integrate with frontend"
echo "  3. Monitor costs in AWS Billing Dashboard"
echo ""
echo "Cost estimate for this test:"
echo "  - Claude calls: ~$0.02"
echo "  - Titan embedding: ~$0.0001"
echo "  - Titan image: ~$0.008"
echo "  Total: ~$0.03"
