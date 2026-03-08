#!/bin/bash
set -e

echo "=========================================="
echo "Frontend Container Initialization"
echo "=========================================="

# Wait for backend API to be ready
echo "Waiting for backend API to be ready..."
/app/scripts/wait-for-service.sh http://backend-api:8000/health 120

echo "=========================================="
echo "Frontend initialization complete!"
echo "Starting web server..."
echo "=========================================="

# Start the main process (passed as arguments to this script)
exec "$@"
