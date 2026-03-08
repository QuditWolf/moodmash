#!/bin/bash
set -e

echo "=========================================="
echo "Backend Container Initialization"
echo "=========================================="

# Wait for DynamoDB to be ready
echo "Waiting for DynamoDB to be ready..."
/app/scripts/wait-for-service.sh http://dynamodb-local:8001 120

# Wait for LocalStack (Bedrock mock) to be ready
echo "Waiting for LocalStack to be ready..."
/app/scripts/wait-for-service.sh http://localstack:4566/_localstack/health 120

# Initialize DynamoDB tables
echo "Initializing DynamoDB tables..."
python /app/scripts/init-dynamodb.py

# Validate all service connections
echo "Validating service connections..."
python /app/scripts/validate-connections.py

echo "=========================================="
echo "Backend initialization complete!"
echo "Starting API server..."
echo "=========================================="

# Start the main process (passed as arguments to this script)
exec "$@"
