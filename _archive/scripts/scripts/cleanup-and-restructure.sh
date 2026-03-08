#!/bin/bash
# Cleanup and Restructure Script

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                  CLEANUP AND RESTRUCTURE PROJECT                             ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "1. Removing Backup Files"
echo "═══════════════════════════════════════════════════════════════════════════════"

find . -type f \( -name "*.bak" -o -name "*.tmp" -o -name "*.swp" -o -name "*~" \) -print -delete
echo -e "${GREEN}✅ Removed backup files${NC}"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "2. Organizing Documentation"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Create docs directory structure
mkdir -p docs/{reapplication,integration,deployment,architecture}

# Move reapplication docs
mv -f README_REAPPLICATION.md docs/reapplication/ 2>/dev/null || true
mv -f REAPPLY_INSTRUCTIONS.md docs/reapplication/ 2>/dev/null || true
mv -f CHANGES_TO_REAPPLY.md docs/reapplication/ 2>/dev/null || true
mv -f SESSION_CHANGES_SUMMARY.md docs/reapplication/ 2>/dev/null || true
mv -f MERGE_AND_REAPPLY_GUIDE.md docs/reapplication/ 2>/dev/null || true
mv -f QUICK_REAPPLY_COMMANDS.md docs/reapplication/ 2>/dev/null || true
mv -f .reapplication-checklist.md docs/reapplication/ 2>/dev/null || true

# Move integration docs
mv -f API_INTEGRATION_COMPLETE.md docs/integration/ 2>/dev/null || true
mv -f DOCKER_INTEGRATION_COMPLETE.md docs/integration/ 2>/dev/null || true

# Move deployment docs
mv -f AWS_MIGRATION.md docs/deployment/ 2>/dev/null || true

# Move architecture docs (if they exist)
mv -f docker-architecture*.md docs/architecture/ 2>/dev/null || true

echo -e "${GREEN}✅ Organized documentation into docs/ directory${NC}"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "3. Organizing Scripts"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Create scripts directory
mkdir -p scripts

# Move scripts
mv -f reapply-session-changes.sh scripts/ 2>/dev/null || true
mv -f test-integration.sh scripts/ 2>/dev/null || true
mv -f cleanup-and-restructure.sh scripts/ 2>/dev/null || true

# Keep these in root for convenience
cp scripts/test-integration.sh . 2>/dev/null || true

echo -e "${GREEN}✅ Organized scripts into scripts/ directory${NC}"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "4. Cleaning Up Task Summary Files"
echo "═══════════════════════════════════════════════════════════════════════════════"

# Move task summaries to docs
mkdir -p docs/tasks
mv -f TASK_*_*.md docs/tasks/ 2>/dev/null || true
mv -f TESTING_*.md docs/tasks/ 2>/dev/null || true

echo -e "${GREEN}✅ Moved task summaries to docs/tasks/${NC}"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "5. Project Structure Summary"
echo "═══════════════════════════════════════════════════════════════════════════════"

echo ""
echo "Root Directory:"
ls -1 *.md 2>/dev/null | sed 's/^/  /'

echo ""
echo "docs/ Directory:"
find docs -type f -name "*.md" | sort | sed 's/^/  /'

echo ""
echo "scripts/ Directory:"
ls -1 scripts/*.sh 2>/dev/null | sed 's/^/  /'

echo ""
echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                         CLEANUP COMPLETE                                     ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Project is now organized with:"
echo "  • docs/ - All documentation"
echo "  • scripts/ - All automation scripts"
echo "  • Root - Essential files only (README, SETUP, QUICKSTART)"
echo ""

