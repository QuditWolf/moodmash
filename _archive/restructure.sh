#!/bin/bash

echo "Starting safe restructure..."

# 1. Create required root folders
mkdir -p frontend
mkdir -p backend
mkdir -p knowledge-base
mkdir -p prompts
mkdir -p docs

echo "Moving existing React app into /frontend..."

# Move frontend files safely
for item in index.html vite.config.js package.json package-lock.json src node_modules dist QUICKSTART.md README.md STRUCTURE.md; do
    if [ -e "$item" ]; then
        mv "$item" frontend/
    fi
done

echo "Creating backend internal structure..."

mkdir -p backend/src/{handlers,services,embedding,matching,utils}
mkdir -p backend/infrastructure
mkdir -p backend/scripts

echo "Creating knowledge base scaffolding..."

touch knowledge-base/{music.json,films.json,books.json,creators.json}

echo "Creating prompt templates..."

touch prompts/{adaptiveQuiz.prompt.md,dna.prompt.md,path.prompt.md,analytics.prompt.md}

echo "Creating documentation files..."

touch docs/{ARCHITECTURE.md,API_CONTRACTS.md,DATA_FLOW.md,DEPLOYMENT.md}

echo "Restructure complete."