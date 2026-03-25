#!/bin/bash
# Automated script to reapply session changes after pulling from main
# Run this after: git checkout punyak && git merge main

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║              Reapplying Session Changes After Main Merge                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo -e "${RED}❌ Error: docker-compose.yml not found. Run this from project root.${NC}"
    exit 1
fi

echo -e "${YELLOW}📋 Reading CHANGES_TO_REAPPLY.md for instructions...${NC}"
if [ ! -f "CHANGES_TO_REAPPLY.md" ]; then
    echo -e "${RED}❌ Error: CHANGES_TO_REAPPLY.md not found!${NC}"
    echo "This file contains all the changes to reapply."
    exit 1
fi

echo ""
echo "This script will:"
echo "  1. Create backend API route files"
echo "  2. Fix frontend API URL"
echo "  3. Update Docker configurations"
echo "  4. Fix backend utils structure"
echo "  5. Update Dockerfiles"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Step 1: Creating Backend API Routes"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Create routes directory
mkdir -p backend/api/routes
echo -e "${GREEN}✅ Created backend/api/routes directory${NC}"

# Check if route files exist
if [ -f "backend/api/routes/quiz.py" ] && [ -f "backend/api/routes/profile.py" ]; then
    echo -e "${GREEN}✅ Route files already exist (quiz.py, profile.py)${NC}"
else
    echo -e "${YELLOW}⚠️  Route files need to be created manually${NC}"
    echo "   Copy content from CHANGES_TO_REAPPLY.md sections:"
    echo "   - Quiz Routes Full Code → backend/api/routes/quiz.py"
    echo "   - Profile Routes Full Code → backend/api/routes/profile.py"
    echo ""
    read -p "Press Enter when files are created..."
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Step 2: Fixing Frontend API URL"
echo "═══════════════════════════════════════════════════════════════════════════════"

if grep -q "VITE_VIBEGRAPH_API_URL" frontend/src/services/vibeGraphAPI.js 2>/dev/null; then
    echo "Updating API_BASE_URL..."
    sed -i.bak "s|VITE_VIBEGRAPH_API_URL.*'http://localhost:3000'|VITE_API_URL || 'http://localhost:8000'|g" frontend/src/services/vibeGraphAPI.js
    echo -e "${GREEN}✅ Fixed frontend API URL${NC}"
elif grep -q "VITE_API_URL.*8000" frontend/src/services/vibeGraphAPI.js 2>/dev/null; then
    echo -e "${GREEN}✅ Frontend API URL already correct${NC}"
else
    echo -e "${YELLOW}⚠️  Could not automatically fix API URL${NC}"
    echo "   Manually change in frontend/src/services/vibeGraphAPI.js:"
    echo "   const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Step 3: Docker Configuration Updates"
echo "═══════════════════════════════════════════════════════════════════════════════"

echo -e "${YELLOW}⚠️  Docker configs need manual updates${NC}"
echo "   See CHANGES_TO_REAPPLY.md section 'Docker Configuration Fixes'"
echo "   Key changes:"
echo "   - docker-compose.yml: DynamoDB command, frontend healthcheck, remove LocalStack volumes"
echo "   - docker-compose.override.yml: Remove volume mounts, fix commands"
echo ""
read -p "Press Enter when Docker configs are updated..."

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Step 4: Backend Utils Structure"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Check if connection_check.py is in the right place
if [ -f "backend/utils/connection_check.py" ] && [ ! -f "backend/src/utils/connection_check.py" ]; then
    echo "Moving connection_check.py to correct location..."
    mkdir -p backend/src/utils
    mv backend/utils/connection_check.py backend/src/utils/
    echo -e "${GREEN}✅ Moved connection_check.py to backend/src/utils/${NC}"
elif [ -f "backend/src/utils/connection_check.py" ]; then
    echo -e "${GREEN}✅ connection_check.py already in correct location${NC}"
fi

# Ensure __init__.py exists
if [ ! -f "backend/src/utils/__init__.py" ]; then
    echo '"""' > backend/src/utils/__init__.py
    echo 'Utility modules for VibeGraph backend.' >> backend/src/utils/__init__.py
    echo '"""' >> backend/src/utils/__init__.py
    echo -e "${GREEN}✅ Created backend/src/utils/__init__.py${NC}"
fi

# Update startup.py import
if grep -q "from utils.connection_check import" backend/api/startup.py 2>/dev/null; then
    echo "Updating startup.py import..."
    sed -i.bak "s|from utils.connection_check import|from src.utils.connection_check import|g" backend/api/startup.py
    echo -e "${GREEN}✅ Updated startup.py import${NC}"
elif grep -q "from src.utils.connection_check import" backend/api/startup.py 2>/dev/null; then
    echo -e "${GREEN}✅ startup.py import already correct${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Step 5: Dockerfile CMD Updates"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Update handlers Dockerfile
if grep -q 'CMD \["python", "-m", "handlers"\]' backend/handlers/Dockerfile 2>/dev/null; then
    echo "Updating handlers Dockerfile..."
    sed -i.bak 's|CMD \["python", "-m", "handlers"\]|CMD ["tail", "-f", "/dev/null"]|g' backend/handlers/Dockerfile
    echo -e "${GREEN}✅ Updated handlers Dockerfile${NC}"
elif grep -q 'CMD \["tail"' backend/handlers/Dockerfile 2>/dev/null; then
    echo -e "${GREEN}✅ handlers Dockerfile already correct${NC}"
fi

# Update services Dockerfile
if grep -q 'CMD \["python", "-m", "services"\]' backend/services/Dockerfile 2>/dev/null; then
    echo "Updating services Dockerfile..."
    sed -i.bak 's|CMD \["python", "-m", "services"\]|CMD ["tail", "-f", "/dev/null"]|g' backend/services/Dockerfile
    echo -e "${GREEN}✅ Updated services Dockerfile${NC}"
elif grep -q 'CMD \["tail"' backend/services/Dockerfile 2>/dev/null; then
    echo -e "${GREEN}✅ services Dockerfile already correct${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Step 6: Verification"
echo "═══════════════════════════════════════════════════════════════════════════════"

echo ""
echo "Running verification checks..."
echo ""

# Check if route files exist
if [ -f "backend/api/routes/quiz.py" ] && [ -f "backend/api/routes/profile.py" ]; then
    echo -e "${GREEN}✅ Backend route files exist${NC}"
else
    echo -e "${RED}❌ Backend route files missing${NC}"
fi

# Check frontend API URL
if grep -q "VITE_API_URL.*8000" frontend/src/services/vibeGraphAPI.js 2>/dev/null; then
    echo -e "${GREEN}✅ Frontend API URL configured${NC}"
else
    echo -e "${RED}❌ Frontend API URL not configured${NC}"
fi

# Check utils location
if [ -f "backend/src/utils/connection_check.py" ]; then
    echo -e "${GREEN}✅ Backend utils in correct location${NC}"
else
    echo -e "${RED}❌ Backend utils not in correct location${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Step 7: Build and Test"
echo "═══════════════════════════════════════════════════════════════════════════════"

echo ""
read -p "Build and start containers now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Building containers..."
    make build
    
    echo ""
    echo "Starting containers..."
    make down
    make up
    
    echo ""
    echo "Waiting for containers to be healthy..."
    sleep 10
    
    echo ""
    echo "Container status:"
    docker ps --format "  {{.Names}}: {{.Status}}" | grep vibegraph
    
    echo ""
    echo "Testing API..."
    if curl -s http://localhost:8000/health | grep -q "healthy"; then
        echo -e "${GREEN}✅ Backend API is healthy${NC}"
    else
        echo -e "${RED}❌ Backend API not responding${NC}"
    fi
    
    if curl -s -X POST http://localhost:8000/quiz/section1/start -H "Content-Type: application/json" -d '{}' | grep -q "sessionId"; then
        echo -e "${GREEN}✅ Quiz API is working${NC}"
    else
        echo -e "${RED}❌ Quiz API not working${NC}"
    fi
    
    if curl -s http://localhost:3000 | grep -q "VibeGraph"; then
        echo -e "${GREEN}✅ Frontend is serving${NC}"
    else
        echo -e "${RED}❌ Frontend not serving${NC}"
    fi
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                            Reapplication Complete!                           ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Review CHANGES_TO_REAPPLY.md for any manual changes needed"
echo "  2. Test the application: http://localhost:3000"
echo "  3. Check API docs: http://localhost:8000/docs"
echo "  4. Commit changes: git add . && git commit -m 'Reapplied session changes'"
echo ""
echo "Documentation:"
echo "  - SETUP.md - Development setup"
echo "  - API_INTEGRATION_COMPLETE.md - API integration details"
echo "  - DOCKER_INTEGRATION_COMPLETE.md - Docker setup details"
echo ""
