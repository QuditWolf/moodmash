# Docker Build Optimization Guide

This document describes the Docker image optimization strategies implemented in the VibeGraph project to reduce build times, minimize image sizes, and improve deployment efficiency.

## Overview

The VibeGraph project uses several optimization techniques:
- Multi-stage builds to separate build and runtime dependencies
- BuildKit for improved build performance and caching
- Layer caching strategies to maximize cache hits
- Minimal base images (alpine, slim) to reduce image size
- Cache mounts for package managers to speed up rebuilds

## Multi-Stage Builds

All Dockerfiles use multi-stage builds to separate the build environment from the runtime environment.

### Frontend (Node.js + nginx)

**Build Stage:**
- Uses `node:20-alpine` as the builder image
- Installs npm dependencies with cache mount
- Builds the Vite production bundle

**Production Stage:**
- Uses `nginx:alpine` as the minimal runtime image
- Only copies the built static assets from the builder stage
- Runs as non-root user for security
- Final image size: ~25-30 MB (vs ~200+ MB without multi-stage)

### Backend (Python)

**Build Stage:**
- Uses `python:3.11-slim` as the builder image
- Installs build dependencies (gcc) needed for compiling Python packages
- Installs Python dependencies with cache mount
- Installs packages to user directory (`--user` flag)

**Production Stage:**
- Uses `python:3.11-slim` as the minimal runtime image
- Only installs runtime dependencies (curl for health checks)
- Copies Python packages from builder stage
- Removes build dependencies from final image
- Final image size: ~150-200 MB (vs ~300+ MB without multi-stage)

## BuildKit Features

BuildKit is Docker's next-generation build system that provides improved performance and new features.

### Enabling BuildKit

Set the environment variable before building:

```bash
export DOCKER_BUILDKIT=1
```

Or use it for a single build:

```bash
DOCKER_BUILDKIT=1 docker-compose build
```

### Cache Mounts

Cache mounts allow build steps to use a persistent cache directory across builds, significantly speeding up dependency installation.

**Frontend (npm):**
```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci --prefer-offline --no-audit
```

**Backend (pip):**
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --user --no-warn-script-location -r requirements.txt
```

### Benefits

- **Faster rebuilds:** Dependencies are cached between builds
- **Reduced network usage:** Packages are downloaded once and reused
- **Parallel builds:** BuildKit can build independent stages in parallel
- **Better layer caching:** Improved cache invalidation logic

## Layer Caching Strategy

Docker caches each layer in a Dockerfile. To maximize cache hits:

### 1. Copy dependency files first

```dockerfile
# Copy package files first (changes infrequently)
COPY package.json package-lock.json ./
RUN npm ci

# Copy source code last (changes frequently)
COPY . .
```

This ensures that dependency installation is cached unless package files change.

### 2. Order commands by change frequency

- Least frequently changed commands first (base image, system packages)
- Dependency installation in the middle
- Source code copy last (changes most frequently)

### 3. Combine related commands

```dockerfile
# Good: Single layer, cleaned up
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

# Bad: Multiple layers, no cleanup
RUN apt-get update
RUN apt-get install -y curl
```

## Image Size Optimization

### Base Image Selection

| Service | Base Image | Size | Rationale |
|---------|-----------|------|-----------|
| Frontend (build) | node:20-alpine | ~180 MB | Minimal Node.js environment |
| Frontend (runtime) | nginx:alpine | ~25 MB | Minimal web server |
| Backend (build) | python:3.11-slim | ~130 MB | Includes build tools |
| Backend (runtime) | python:3.11-slim | ~130 MB | Minimal Python runtime |

### Dependency Management

**Remove build dependencies:**
```dockerfile
# Build stage: Install build dependencies
RUN apt-get install -y gcc

# Production stage: Only runtime dependencies
RUN apt-get install -y curl
```

**Clean package manager caches:**
```dockerfile
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
```

**Use --no-cache-dir for pip:**
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

## Docker Compose Build Configuration

The `docker-compose.yml` file is configured to use BuildKit features:

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      cache_from:
        - vibegraph-frontend:latest
      args:
        BUILDKIT_INLINE_CACHE: 1
```

**cache_from:** Specifies images to use as cache sources
**BUILDKIT_INLINE_CACHE:** Embeds cache metadata in the image for reuse

## Expected Image Sizes

After optimization, expected image sizes are:

| Service | Unoptimized | Optimized | Reduction |
|---------|-------------|-----------|-----------|
| Frontend | ~250 MB | ~30 MB | 88% |
| Backend API | ~350 MB | ~180 MB | 49% |
| Backend Handlers | ~350 MB | ~180 MB | 49% |
| Backend Services | ~350 MB | ~180 MB | 49% |

**Total reduction:** ~1.3 GB → ~570 MB (56% reduction)

## Build Performance

### Without Optimization

- Clean build: ~5-8 minutes
- Rebuild with code changes: ~5-8 minutes (no caching)
- Dependency changes: ~5-8 minutes

### With Optimization

- Clean build: ~5-8 minutes (first time)
- Rebuild with code changes: ~30-60 seconds (cached dependencies)
- Dependency changes: ~2-3 minutes (cached base layers)

**Improvement:** 80-90% faster for typical development rebuilds

## Best Practices

### 1. Use .dockerignore

Exclude unnecessary files from the build context:

```
node_modules
dist
.git
.env
*.log
```

### 2. Minimize layers

Combine related RUN commands to reduce layer count:

```dockerfile
# Good: 1 layer
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Bad: 3 layers
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*
```

### 3. Use specific versions

Pin dependency versions for reproducible builds:

```dockerfile
FROM node:20-alpine  # Good: specific version
FROM node:alpine     # Bad: floating tag
```

### 4. Security considerations

- Use non-root users in production images
- Remove unnecessary packages and files
- Keep base images updated
- Scan images for vulnerabilities

## Makefile Integration

The Makefile includes optimized build commands:

```bash
# Build with BuildKit enabled
make build

# Build with no cache (force rebuild)
make rebuild

# Build specific service
make build-frontend
make build-backend
```

## Monitoring Build Performance

Check build times and cache usage:

```bash
# Build with timing information
time make build

# Check image sizes
docker images | grep vibegraph

# Inspect build cache
docker buildx du
```

## Troubleshooting

### Cache not being used

**Problem:** Builds are slow even with cache mounts

**Solution:**
- Ensure BuildKit is enabled: `export DOCKER_BUILDKIT=1`
- Check that dependency files haven't changed
- Verify cache mount paths are correct

### Large image sizes

**Problem:** Images are larger than expected

**Solution:**
- Verify multi-stage builds are working
- Check that build dependencies are removed
- Use `docker history <image>` to inspect layers
- Ensure .dockerignore is properly configured

### Build failures with cache mounts

**Problem:** Builds fail with cache mount errors

**Solution:**
- Ensure Docker version supports BuildKit (19.03+)
- Check that BuildKit is enabled
- Try building without cache mounts first

## Further Optimization

Potential future optimizations:

1. **Layer caching in CI/CD:** Use registry cache for faster CI builds
2. **Distroless images:** Use Google's distroless images for even smaller sizes
3. **Dependency vendoring:** Pre-download dependencies for offline builds
4. **Build cache warming:** Pre-populate caches in CI/CD pipelines
5. **Image scanning:** Automated vulnerability scanning and updates

## References

- [Docker BuildKit Documentation](https://docs.docker.com/build/buildkit/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Docker Build Cache](https://docs.docker.com/build/cache/)
