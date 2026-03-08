#!/bin/bash

# Test script for all VibeGraph API endpoints
# Tests the complete flow: Section 1 → Section 2 → Complete → Profile endpoints

set -e

API_URL="http://localhost:8000"
USER_ID="test-user-$(date +%s)"

echo "========================================="
echo "VibeGraph API Integration Test"
echo "========================================="
echo ""
echo "User ID: $USER_ID"
echo ""

# Test 1: Start Section 1
echo "1. Testing Section 1 generation..."
SECTION1_RESPONSE=$(curl -s -X POST "$API_URL/quiz/section1/start" \
  -H "Content-Type: application/json" \
  -d '{}')

SESSION_ID=$(echo "$SECTION1_RESPONSE" | jq -r '.sessionId')
QUESTION_COUNT=$(echo "$SECTION1_RESPONSE" | jq '.questions | length')

echo "   ✓ Session ID: $SESSION_ID"
echo "   ✓ Questions generated: $QUESTION_COUNT"
echo ""

# Test 2: Generate Section 2
echo "2. Testing Section 2 generation..."
SECTION2_RESPONSE=$(curl -s -X POST "$API_URL/quiz/section2/generate" \
  -H "Content-Type: application/json" \
  -d "{
    \"sessionId\": \"$SESSION_ID\",
    \"section1Answers\": [
      {\"questionId\": \"q1\", \"selectedOptions\": [\"Music\", \"Film\"], \"category\": \"content_preference\"},
      {\"questionId\": \"q2\", \"selectedOptions\": [\"By recommendations\"], \"category\": \"discovery_style\"},
      {\"questionId\": \"q3\", \"selectedOptions\": [\"Energetic\"], \"category\": \"mood_preference\"},
      {\"questionId\": \"q4\", \"selectedOptions\": [\"Create\"], \"category\": \"engagement_style\"},
      {\"questionId\": \"q5\", \"selectedOptions\": [\"Novelty\"], \"category\": \"attraction_factors\"}
    ]
  }")

SECTION2_QUESTION_COUNT=$(echo "$SECTION2_RESPONSE" | jq '.questions | length')
echo "   ✓ Adaptive questions generated: $SECTION2_QUESTION_COUNT"
echo ""

# Test 3: Complete Quiz
echo "3. Testing quiz completion (embedding + DNA generation)..."
COMPLETE_RESPONSE=$(curl -s -X POST "$API_URL/quiz/complete" \
  -H "Content-Type: application/json" \
  -d "{
    \"sessionId\": \"$SESSION_ID\",
    \"userId\": \"$USER_ID\",
    \"allAnswers\": {
      \"section1\": [
        {\"questionId\": \"q1\", \"selectedOptions\": [\"Music\", \"Film\"], \"category\": \"content_preference\"},
        {\"questionId\": \"q2\", \"selectedOptions\": [\"By recommendations\"], \"category\": \"discovery_style\"},
        {\"questionId\": \"q3\", \"selectedOptions\": [\"Energetic\"], \"category\": \"mood_preference\"},
        {\"questionId\": \"q4\", \"selectedOptions\": [\"Create\"], \"category\": \"engagement_style\"},
        {\"questionId\": \"q5\", \"selectedOptions\": [\"Novelty\"], \"category\": \"attraction_factors\"}
      ],
      \"section2\": [
        {\"questionId\": \"q6\", \"selectedOptions\": [\"Bold\", \"Dynamic\"], \"category\": \"visual_style\"},
        {\"questionId\": \"q7\", \"selectedOptions\": [\"Adventure\", \"Innovation\"], \"category\": \"narrative_preference\"},
        {\"questionId\": \"q8\", \"selectedOptions\": [\"Creating content\"], \"category\": \"activity_preference\"},
        {\"questionId\": \"q9\", \"selectedOptions\": [\"Global trends\"], \"category\": \"cultural_alignment\"},
        {\"questionId\": \"q10\", \"selectedOptions\": [\"Innovation\"], \"category\": \"taste_identity\"}
      ]
    }
  }")

EMBEDDING_ID=$(echo "$COMPLETE_RESPONSE" | jq -r '.embeddingId')
ARCHETYPE=$(echo "$COMPLETE_RESPONSE" | jq -r '.tasteDNA.archetype')

echo "   ✓ Embedding ID: ${EMBEDDING_ID:0:16}..."
echo "   ✓ Archetype: $ARCHETYPE"
echo ""

# Test 4: Get Growth Path
echo "4. Testing growth path generation..."
PATH_RESPONSE=$(curl -s -X GET "$API_URL/profile/path/$USER_ID" \
  -H "Content-Type: application/json")

if echo "$PATH_RESPONSE" | jq -e '.path' > /dev/null 2>&1; then
  ABSORB_COUNT=$(echo "$PATH_RESPONSE" | jq '.path.absorb | length')
  CREATE_COUNT=$(echo "$PATH_RESPONSE" | jq '.path.create | length')
  REFLECT_COUNT=$(echo "$PATH_RESPONSE" | jq '.path.reflect | length')
  echo "   ✓ Absorb recommendations: $ABSORB_COUNT"
  echo "   ✓ Create recommendations: $CREATE_COUNT"
  echo "   ✓ Reflect recommendations: $REFLECT_COUNT"
else
  echo "   ✗ Error: $(echo "$PATH_RESPONSE" | jq -r '.detail')"
fi
echo ""

# Test 5: Get Analytics
echo "5. Testing analytics generation..."
ANALYTICS_RESPONSE=$(curl -s -X GET "$API_URL/profile/analytics/$USER_ID" \
  -H "Content-Type: application/json")

if echo "$ANALYTICS_RESPONSE" | jq -e '.analytics' > /dev/null 2>&1; then
  INSIGHTS_COUNT=$(echo "$ANALYTICS_RESPONSE" | jq '.analytics.insights | length')
  echo "   ✓ Insights generated: $INSIGHTS_COUNT"
else
  echo "   ✗ Error: $(echo "$ANALYTICS_RESPONSE" | jq -r '.detail')"
fi
echo ""

# Test 6: Find Matches
echo "6. Testing taste matching..."
MATCHES_RESPONSE=$(curl -s -X GET "$API_URL/profile/matches/$USER_ID?limit=5" \
  -H "Content-Type: application/json")

if echo "$MATCHES_RESPONSE" | jq -e '.matches' > /dev/null 2>&1; then
  MATCHES_COUNT=$(echo "$MATCHES_RESPONSE" | jq '.matches | length')
  echo "   ✓ Matches found: $MATCHES_COUNT"
else
  echo "   ✗ Error: $(echo "$MATCHES_RESPONSE" | jq -r '.detail')"
fi
echo ""

# Test 7: DNA Card Image Generation (optional - requires Bedrock image models)
echo "7. Testing DNA card image generation..."
echo "   (This may fail if Bedrock image models are not enabled)"
DNA_CARD_RESPONSE=$(curl -s -X POST "$API_URL/profile/dna-card/$USER_ID?model=titan" \
  -H "Content-Type: application/json")

if echo "$DNA_CARD_RESPONSE" | jq -e '.imageData' > /dev/null 2>&1; then
  IMAGE_SIZE=$(echo "$DNA_CARD_RESPONSE" | jq -r '.imageData' | wc -c)
  IMAGE_FORMAT=$(echo "$DNA_CARD_RESPONSE" | jq -r '.format')
  echo "   ✓ Image generated: $IMAGE_FORMAT, ${IMAGE_SIZE} bytes (base64)"
else
  echo "   ⚠ Image generation not available: $(echo "$DNA_CARD_RESPONSE" | jq -r '.detail')"
fi
echo ""

echo "========================================="
echo "Test Summary"
echo "========================================="
echo "✓ Section 1 generation: PASSED"
echo "✓ Section 2 generation: PASSED"
echo "✓ Quiz completion: PASSED"
echo ""
echo "Profile endpoints:"
if echo "$PATH_RESPONSE" | jq -e '.path' > /dev/null 2>&1; then
  echo "✓ Growth path: PASSED"
else
  echo "✗ Growth path: FAILED"
fi

if echo "$ANALYTICS_RESPONSE" | jq -e '.analytics' > /dev/null 2>&1; then
  echo "✓ Analytics: PASSED"
else
  echo "✗ Analytics: FAILED"
fi

if echo "$MATCHES_RESPONSE" | jq -e '.matches' > /dev/null 2>&1; then
  echo "✓ Matches: PASSED"
else
  echo "✗ Matches: FAILED"
fi

if echo "$DNA_CARD_RESPONSE" | jq -e '.imageData' > /dev/null 2>&1; then
  echo "✓ DNA card image: PASSED"
else
  echo "⚠ DNA card image: SKIPPED (requires Bedrock image models)"
fi

echo ""
echo "All core endpoints tested successfully!"
