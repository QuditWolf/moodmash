#!/bin/bash
# wait-for-service.sh - Wait for a service to be healthy before proceeding
#
# Usage: wait-for-service.sh <url> [timeout]
#   url: The health check URL to poll
#   timeout: Maximum time to wait in seconds (default: 120)
#
# Examples:
#   wait-for-service.sh http://backend-api:8000/health
#   wait-for-service.sh http://dynamodb-local:8001 60

set -e

URL="${1}"
TIMEOUT="${2:-120}"
INTERVAL=5

if [ -z "$URL" ]; then
    echo "Error: URL is required"
    echo "Usage: wait-for-service.sh <url> [timeout]"
    exit 1
fi

echo "Waiting for service at $URL (timeout: ${TIMEOUT}s)..."

START_TIME=$(date +%s)
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
    # Try to reach the service
    if curl -sf "$URL" > /dev/null 2>&1; then
        echo "✓ Service is ready at $URL (took ${ELAPSED}s)"
        exit 0
    fi
    
    # Calculate elapsed time
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    # Show progress
    echo "  Waiting... (${ELAPSED}s / ${TIMEOUT}s)"
    
    # Wait before next attempt
    sleep $INTERVAL
done

# Timeout reached
echo "✗ Timeout: Service at $URL did not become ready within ${TIMEOUT}s"
exit 1
