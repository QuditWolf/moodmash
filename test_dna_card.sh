#!/bin/bash

USER_ID="test-user-image-$(date +%s)"

echo "Creating user with quiz completion..."
SESSION_ID=$(curl -s -X POST http://localhost:8000/quiz/section1/start -H "Content-Type: application/json" -d '{}' | jq -r '.sessionId')

curl -s -X POST http://localhost:8000/quiz/complete \
  -H "Content-Type: application/json" \
  -d "{
    \"sessionId\": \"$SESSION_ID\",
    \"userId\": \"$USER_ID\",
    \"allAnswers\": {
      \"section1\": [
        {\"questionId\": \"q1\", \"selectedOptions\": [\"Music\"], \"category\": \"content\"},
        {\"questionId\": \"q2\", \"selectedOptions\": [\"Exploring\"], \"category\": \"discovery\"},
        {\"questionId\": \"q3\", \"selectedOptions\": [\"Energetic\"], \"category\": \"mood\"},
        {\"questionId\": \"q4\", \"selectedOptions\": [\"Create\"], \"category\": \"engagement\"},
        {\"questionId\": \"q5\", \"selectedOptions\": [\"Novelty\"], \"category\": \"attraction\"}
      ],
      \"section2\": [
        {\"questionId\": \"q6\", \"selectedOptions\": [\"Bold\"], \"category\": \"visual\"},
        {\"questionId\": \"q7\", \"selectedOptions\": [\"Adventure\"], \"category\": \"narrative\"},
        {\"questionId\": \"q8\", \"selectedOptions\": [\"Creating\"], \"category\": \"activity\"},
        {\"questionId\": \"q9\", \"selectedOptions\": [\"Global\"], \"category\": \"cultural\"},
        {\"questionId\": \"q10\", \"selectedOptions\": [\"Innovation\"], \"category\": \"identity\"}
      ]
    }
  }" > /dev/null

echo ""
echo "Testing DNA card with Titan v2..."
curl -s -X POST "http://localhost:8000/profile/dna-card/$USER_ID?model=titan" \
  -H "Content-Type: application/json" | jq '{imageId, format, width, height, model, archetype, imageSize: (.imageData | length)}'

echo ""
echo "Testing DNA card with Nova Canvas..."
curl -s -X POST "http://localhost:8000/profile/dna-card/$USER_ID?model=nova" \
  -H "Content-Type: application/json" | jq '{imageId, format, width, height, model, archetype, imageSize: (.imageData | length)}'
