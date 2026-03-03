#!/bin/bash

echo "Cleaning root to strict 5-folder structure..."

# Move infrastructure into backend
if [ -d "infrastructure" ]; then
    mv infrastructure/* backend/infrastructure/ 2>/dev/null
    rmdir infrastructure 2>/dev/null
fi

# Move scripts into backend
if [ -d "scripts" ]; then
    mv scripts/* backend/scripts/ 2>/dev/null
    rmdir scripts 2>/dev/null
fi

# Move dev-utils into docs
if [ -d "dev-utils" ]; then
    mkdir -p docs/dev-utils
    mv dev-utils/* docs/dev-utils/ 2>/dev/null
    rmdir dev-utils 2>/dev/null
fi

# Move restructure script into backend scripts
if [ -f "restructure.sh" ]; then
    mv restructure.sh backend/scripts/
fi

echo "Root cleaned."