#!/bin/bash

echo "Creating new architecture structure..."

# Create main folders
mkdir -p frontend
mkdir -p backend/src/{handlers,services,embedding,matching,utils}
mkdir -p knowledge-base
mkdir -p prompts
mkdir -p docs
mkdir -p infrastructure
mkdir -p scripts

echo "Moving existing React app into /frontend..."

# Move frontend files safely
mv index.html frontend/ 2>/dev/null
mv vite.config.js frontend/ 2>/dev/null
mv package.json frontend/ 2>/dev/null
mv package-lock.json frontend/ 2>/dev/null
mv node_modules frontend/ 2>/dev/null
mv dist frontend/ 2>/dev/null
mv src frontend/ 2>/dev/null

echo "Creating backend boilerplate..."

touch backend/package.json

touch backend/src/handlers/{generateSection1.js,generateSection2.js,generateEmbedding.js,generateDNA.js,generatePath.js,generateAnalytics.js,findMatches.js}

touch backend/src/services/{bedrockClient.js,titanEmbeddingService.js,claudeService.js,dynamoClient.js,userService.js}

touch backend/src/embedding/{embeddingBuilder.js,normalizeVector.js}

touch backend/src/matching/{cosineSimilarity.js,matchEngine.js}

touch backend/src/utils/{hash.js,logger.js}

echo "Creating knowledge base scaffolding..."

touch knowledge-base/{music.json,films.json,books.json,creators.json,catalog.schema.json}

echo "Creating prompt templates..."

touch prompts/{adaptiveQuiz.prompt.md,dna.prompt.md,path.prompt.md,analytics.prompt.md}

echo "Creating documentation files..."

touch docs/{ARCHITECTURE.md,API_CONTRACTS.md,DATA_FLOW.md,DEPLOYMENT.md}

echo "Creating infrastructure template..."

touch infrastructure/template.yaml

echo "Structure initialized successfully."