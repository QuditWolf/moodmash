# Test Container for Backend Testing
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY tests/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY src /app/src/
COPY api /app/api/

# Copy test files
COPY tests /app/tests/

# Set Python path
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command runs all tests
CMD ["pytest", "-v", "--tb=short", "--color=yes", "/app/tests/unit/"]
