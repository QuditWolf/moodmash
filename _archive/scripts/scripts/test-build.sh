#!/bin/bash
# Test script for build process validation (Task 21.1)
# This script validates that all Docker images build successfully

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Build Process Validation Test ===${NC}"
echo ""

# Test 1: Check if docker-compose.yml exists
echo -e "${YELLOW}[1/5] Checking docker-compose.yml...${NC}"
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}✗ docker-compose.yml not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ docker-compose.yml found${NC}"
echo ""

# Test 2: Validate docker-compose configuration
echo -e "${YELLOW}[2/5] Validating docker-compose configuration...${NC}"
if ! docker-compose config > /dev/null 2>&1; then
    echo -e "${RED}✗ docker-compose configuration is invalid${NC}"
    docker-compose config
    exit 1
fi
echo -e "${GREEN}✓ docker-compose configuration is valid${NC}"
echo ""

# Test 3: Build all images
echo -e "${YELLOW}[3/5] Building all Docker images...${NC}"
if ! docker-compose build --no-cache 2>&1 | tee /tmp/build.log; then
    echo -e "${RED}✗ Build failed${NC}"
    echo "Check /tmp/build.log for details"
    exit 1
fi
echo -e "${GREEN}✓ All images built successfully${NC}"
echo ""

# Test 4: Check image sizes
echo -e "${YELLOW}[4/5] Checking image sizes...${NC}"
echo "Image sizes:"
docker images | grep vibegraph | awk '{print $1 ":" $2 " - " $7 $8}'
echo ""

# Warn if any image is too large (> 2GB)
large_images=$(docker images | grep vibegraph | awk '$7 ~ /GB/ && $7+0 > 2 {print $1":"$2}')
if [ -n "$large_images" ]; then
    echo -e "${YELLOW}⚠ Warning: Some images are larger than 2GB:${NC}"
    echo "$large_images"
    echo "Consider optimizing these images"
else
    echo -e "${GREEN}✓ All image sizes are reasonable${NC}"
fi
echo ""

# Test 5: Verify all expected images exist
echo -e "${YELLOW}[5/5] Verifying all expected images exist...${NC}"
expected_images=(
    "vibegraph-frontend"
    "vibegraph-backend-api"
    "vibegraph-backend-handlers"
    "vibegraph-backend-services"
    "vibegraph-dynamodb-init"
)

missing_images=()
for img in "${expected_images[@]}"; do
    if ! docker images | grep -q "$img"; then
        missing_images+=("$img")
    fi
done

if [ ${#missing_images[@]} -gt 0 ]; then
    echo -e "${RED}✗ Missing images:${NC}"
    printf '%s\n' "${missing_images[@]}"
    exit 1
fi
echo -e "${GREEN}✓ All expected images exist${NC}"
echo ""

# Test 6: Check build cache effectiveness
echo -e "${YELLOW}[Bonus] Testing build cache effectiveness...${NC}"
echo "Rebuilding with cache..."
start_time=$(date +%s)
docker-compose build > /dev/null 2>&1
end_time=$(date +%s)
cache_build_time=$((end_time - start_time))
echo "Cached build completed in ${cache_build_time}s"
if [ $cache_build_time -lt 30 ]; then
    echo -e "${GREEN}✓ Build cache is effective${NC}"
else
    echo -e "${YELLOW}⚠ Build cache may not be optimal (took ${cache_build_time}s)${NC}"
fi
echo ""

echo -e "${GREEN}=== Build Process Validation Complete ===${NC}"
echo ""
echo "Summary:"
echo "  - Configuration: Valid"
echo "  - All images: Built successfully"
echo "  - Image count: ${#expected_images[@]}"
echo "  - Cached build time: ${cache_build_time}s"
echo ""
echo -e "${BLUE}Next step: Run 'make up' to start containers${NC}"
