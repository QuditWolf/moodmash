#!/bin/bash

# Create backend structure
mkdir -p backend/src/{handlers,services,embedding,matching,prompts,utils}
mkdir -p backend/events

# Create infrastructure
mkdir -p infrastructure/dynamodb
mkdir -p infrastructure/policies

# Create scripts and docs
mkdir -p scripts
mkdir -p docs

# Touch backend files
touch backend/src/handlers/{generateSection1.js,generateSection2.js,generateEmbedding.js,generateDNA.js,generatePath.js,generateAnalytics.js,findMatches.js,healthCheck.js}

touch backend/src/services/{bedrockClient.js,titanEmbeddingService.js,claudeService.js,dynamoClient.js,userService.js,cacheService.js}

touch backend/src/embedding/{embeddingBuilder.js,weightingEngine.js,normalizeVector.js}

touch backend/src/matching/{cosineSimilarity.js,matchEngine.js}

touch backend/src/prompts/{adaptiveQuizPrompt.txt,dnaPrompt.txt,pathPrompt.txt,analyticsPrompt.txt}

touch backend/src/utils/{hash.js,logger.js,validator.js}

touch backend/events/{section1.json,embedding.json}

touch infrastructure/template.yaml
touch infrastructure/dynamodb/{usersTable.json,sessionsTable.json,cacheTable.json}
touch infrastructure/policies/{bedrockPolicy.json,dynamoPolicy.json}

touch scripts/{init-architecture.sh,deploy-backend.sh,local-dev.sh}

touch docs/{ARCHITECTURE.md,DATA_FLOW.md,EMBEDDING_STRATEGY.md}

echo "Monorepo backend architecture scaffolded safely."
