# Build stage - install dependencies
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install dependencies with cache mount for faster rebuilds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-warn-script-location -r requirements.txt

# Production stage - minimal runtime image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Remove unnecessary packages and clean up
RUN apt-get update && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy service source code
COPY . .

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Default command (can be overridden)
# Services are imported by other containers, so just keep container running
CMD ["tail", "-f", "/dev/null"]
