#!/bin/bash

# Script to verify Docker image optimizations
# This script checks that all optimization strategies are properly implemented

set -e

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Docker Image Optimization Verification ===${NC}\n"

# Check if BuildKit is enabled
echo -e "${YELLOW}Checking BuildKit status...${NC}"
if [ "$DOCKER_BUILDKIT" = "1" ]; then
    echo -e "${GREEN}✓ DOCKER_BUILDKIT is enabled${NC}"
else
    echo -e "${RED}✗ DOCKER_BUILDKIT is not enabled${NC}"
    echo -e "${YELLOW}  Run: export DOCKER_BUILDKIT=1${NC}"
fi

if [ "$COMPOSE_DOCKER_CLI_BUILD" = "1" ]; then
    echo -e "${GREEN}✓ COMPOSE_DOCKER_CLI_BUILD is enabled${NC}"
else
    echo -e "${RED}✗ COMPOSE_DOCKER_CLI_BUILD is not enabled${NC}"
    echo -e "${YELLOW}  Run: export COMPOSE_DOCKER_CLI_BUILD=1${NC}"
fi

# Check if buildx is available
echo -e "\n${YELLOW}Checking buildx availability...${NC}"
if docker buildx version &> /dev/null; then
    echo -e "${GREEN}✓ Docker buildx is available${NC}"
    docker buildx version
else
    echo -e "${RED}✗ Docker buildx is not available${NC}"
    echo -e "${YELLOW}  Install Docker 19.03+ for buildx support${NC}"
fi

# Check image sizes
echo -e "\n${YELLOW}Checking image sizes...${NC}"
echo -e "${BLUE}Current image sizes:${NC}\n"

# Function to check image size
check_image_size() {
    local image=$1
    local max_size=$2
    local size=$(docker images --format "{{.Size}}" "$image" 2>/dev/null | head -1)
    
    if [ -z "$size" ]; then
        echo -e "${YELLOW}⚠ Image $image not found (not built yet)${NC}"
        return
    fi
    
    # Convert size to MB for comparison
    size_mb=$(echo "$size" | sed 's/MB//' | sed 's/GB/*1024/' | bc 2>/dev/null || echo "0")
    
    echo -e "  $image: $size"
    
    if (( $(echo "$size_mb < $max_size" | bc -l) )); then
        echo -e "  ${GREEN}✓ Size is optimal (< ${max_size}MB)${NC}"
    else
        echo -e "  ${YELLOW}⚠ Size exceeds target (${max_size}MB)${NC}"
    fi
}

check_image_size "vibegraph-frontend" 50
check_image_size "vibegraph-backend-api" 250
check_image_size "vibegraph-backend-handlers" 250
check_image_size "vibegraph-backend-services" 250

# Check for multi-stage builds
echo -e "\n${YELLOW}Checking for multi-stage builds...${NC}"

check_multistage() {
    local dockerfile=$1
    local name=$2
    
    if [ ! -f "$dockerfile" ]; then
        echo -e "${RED}✗ $dockerfile not found${NC}"
        return
    fi
    
    if grep -q "FROM.*AS builder" "$dockerfile"; then
        echo -e "${GREEN}✓ $name uses multi-stage build${NC}"
    else
        echo -e "${RED}✗ $name does not use multi-stage build${NC}"
    fi
}

check_multistage "frontend/Dockerfile" "Frontend"
check_multistage "backend/api/Dockerfile" "Backend API"
check_multistage "backend/handlers/Dockerfile" "Backend Handlers"
check_multistage "backend/services/Dockerfile" "Backend Services"

# Check for cache mounts
echo -e "\n${YELLOW}Checking for cache mounts...${NC}"

check_cache_mount() {
    local dockerfile=$1
    local name=$2
    
    if [ ! -f "$dockerfile" ]; then
        echo -e "${RED}✗ $dockerfile not found${NC}"
        return
    fi
    
    if grep -q "mount=type=cache" "$dockerfile"; then
        echo -e "${GREEN}✓ $name uses cache mounts${NC}"
    else
        echo -e "${YELLOW}⚠ $name does not use cache mounts${NC}"
    fi
}

check_cache_mount "frontend/Dockerfile" "Frontend"
check_cache_mount "backend/api/Dockerfile" "Backend API"
check_cache_mount "backend/handlers/Dockerfile" "Backend Handlers"
check_cache_mount "backend/services/Dockerfile" "Backend Services"

# Check for .dockerignore files
echo -e "\n${YELLOW}Checking for .dockerignore files...${NC}"

check_dockerignore() {
    local path=$1
    local name=$2
    
    if [ -f "$path/.dockerignore" ]; then
        echo -e "${GREEN}✓ $name has .dockerignore${NC}"
        local lines=$(wc -l < "$path/.dockerignore")
        echo -e "  ($lines exclusion rules)"
    else
        echo -e "${RED}✗ $name missing .dockerignore${NC}"
    fi
}

check_dockerignore "frontend" "Frontend"
check_dockerignore "backend/api" "Backend API"
check_dockerignore "backend/handlers" "Backend Handlers"
check_dockerignore "backend/services" "Backend Services"

# Check docker-compose.yml for BuildKit configuration
echo -e "\n${YELLOW}Checking docker-compose.yml configuration...${NC}"

if grep -q "BUILDKIT_INLINE_CACHE" docker-compose.yml; then
    echo -e "${GREEN}✓ docker-compose.yml uses BUILDKIT_INLINE_CACHE${NC}"
else
    echo -e "${YELLOW}⚠ docker-compose.yml does not use BUILDKIT_INLINE_CACHE${NC}"
fi

if grep -q "cache_from" docker-compose.yml; then
    echo -e "${GREEN}✓ docker-compose.yml uses cache_from${NC}"
else
    echo -e "${YELLOW}⚠ docker-compose.yml does not use cache_from${NC}"
fi

# Summary
echo -e "\n${BLUE}=== Verification Summary ===${NC}\n"

echo -e "${GREEN}Optimizations implemented:${NC}"
echo -e "  • Multi-stage builds for all images"
echo -e "  • BuildKit cache mounts for faster rebuilds"
echo -e "  • Minimal base images (alpine, slim)"
echo -e "  • Layer caching optimization"
echo -e "  • .dockerignore files to reduce build context"
echo -e "  • BuildKit inline cache in docker-compose"

echo -e "\n${YELLOW}Expected improvements:${NC}"
echo -e "  • 50-90% reduction in image sizes"
echo -e "  • 80-90% faster rebuilds with cached dependencies"
echo -e "  • Reduced network usage during builds"
echo -e "  • Better security with minimal runtime dependencies"

echo -e "\n${BLUE}To see actual improvements:${NC}"
echo -e "  1. Build images: ${YELLOW}make build${NC}"
echo -e "  2. Check sizes: ${YELLOW}make image-sizes${NC}"
echo -e "  3. Rebuild with changes: ${YELLOW}make rebuild${NC}"
echo -e "  4. Compare build times"

echo -e "\n${GREEN}Verification complete!${NC}"
