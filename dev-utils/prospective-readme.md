# README-alpha.md  
VibeGraph — Alpha Architecture & Execution Plan  

---

# 1. Vision

VibeGraph is an AI-powered personal taste engine that transforms digital consumption into structured growth.

Most platforms optimize for attention retention.  
VibeGraph optimizes for identity clarity and directional growth.

The system:

- Understands user taste across domains
- Converts it into a unified embedding
- Generates structured growth paths
- Provides analytics insight into digital behavior
- Enables privacy-first taste matching

Core philosophy:

> Your taste is your compass.

---

# 2. Architectural Overview

This repository is a monorepo.

Git root: vibegraph-app/

It contains:

- React frontend
- Serverless backend
- Infrastructure as Code
- AI prompt layer
- Embedding pipeline
- Matching engine

---

# 3. System Architecture (High-Level)

User  
→ React (Vite)  
→ API Gateway  
→ Lambda  
→ Bedrock (Claude / Titan v2)  
→ DynamoDB  
→ Response  
→ React render  

Matching:
Lambda → Fetch embeddings → Cosine similarity → Top N

Analytics:
Lambda → Process structured data → Claude insight generation

All compute is serverless.

No persistent servers.  
No EC2.  
No RDS.  
No containers.

---

# 4. Repository Structure

vibegraph-app/
│
├── src/                   # React frontend
├── backend/               # Lambda source
├── infrastructure/        # AWS SAM templates
├── scripts/               # Dev + deployment automation
├── docs/                  # System documentation
├── README.md
├── README-alpha.md
└── package.json

---

# 5. Frontend Architecture

Location: src/

Responsibilities:

- Render Section 1 + Section 2 quiz
- Collect MSQ + comments
- Call backend APIs
- Render DNA card
- Render growth paths
- Render analytics dashboard
- Render match suggestions

No embedding logic in frontend.  
No AWS SDK in frontend.  
No secrets in frontend.

All AI calls happen server-side.

---

# 6. Backend Architecture

Location: backend/

Serverless Lambda functions:

- generateSection1
- generateSection2
- generateEmbedding
- generateDNA
- generatePath
- generateAnalytics
- findMatches
- healthCheck

Each function is stateless.

---

# 7. AI Layer

## 7.1 Claude (Bedrock)

Used for:

- Adaptive Section 2 generation
- DNA archetype generation
- Growth path creation
- Analytics insight generation

Claude is used only for reasoning tasks.

---

## 7.2 Titan Text Embeddings v2

Used for:

- Taste vector construction
- Goal vector modeling
- Matching
- Alignment scoring

Vector dimension: 1024  
Embedding normalized to unit length.  
Similarity metric: cosine similarity.

---

# 8. Embedding Pipeline

1. User completes quiz
2. Backend constructs structured embedding document
3. Titan v2 invoked
4. 1024-dimension vector returned
5. Normalize vector
6. Store in DynamoDB
7. Use for:
   - Matching
   - Ranking
   - Path personalization
   - Goal alignment scoring

We do NOT store raw quiz responses long-term.

---

# 9. Database Design (DynamoDB)

## UsersTable

Partition Key: userId

Attributes:
- tasteVector
- goalVector
- dnaSummary
- createdAt

---

## SessionsTable

Partition Key: sessionId

Stores temporary onboarding state.

---

## EmbeddingCacheTable

Partition Key: inputHash  
Used to skip repeated LLM calls.

---

# 10. Matching Engine

Located in:

backend/src/matching/

Algorithm:

1. Fetch candidate embeddings
2. Compute cosine similarity
3. Rank
4. Return top 3–5

No vector database required at MVP scale.

---

# 11. Growth Path Engine

Inputs:
- Taste vector
- Goal
- Mood
- Time available

Claude generates structured output:

Absorb  
Create  
Reflect  

Each step aligned with:
- Taste embedding
- Goal alignment bias

---

# 12. Analytics Engine

Inputs:
- Self-reported consumption
- Completion history

Outputs:
- Passive vs intentional ratio
- Goal alignment score
- Pattern insights
- Behavioral shift detection

Insight generation is Claude-based but structured.

---

# 13. Infrastructure

Location: infrastructure/

Uses AWS SAM.

Resources defined:

- API Gateway
- Lambda functions
- DynamoDB tables
- IAM roles
- Bedrock access policy

Deployment:

sam build  
sam deploy --guided  

Frontend can be deployed via:
- AWS Amplify
- S3 static hosting
- Vercel (temporary)

---

# 14. Privacy Design

Principles:

- Raw quiz responses not stored permanently
- Only embeddings + derived metadata stored
- User can request deletion
- Matching uses anonymized vectors
- No ad monetization model

Data minimization by default.

---

# 15. Cost Model (MVP)

Embedding cost:
~$0.0001 per user

Claude generation:
Higher but bounded via caching

Lambda:
Free tier friendly

DynamoDB:
Free tier friendly

At 10,000 users:
Infrastructure cost remains minimal.

---

# 16. Roadmap

## Phase 1 — Core MVP

- Section 1 + Section 2
- Titan embedding
- DNA generation
- Basic path
- Basic matching

## Phase 2 — Analytics

- Time map
- Dopamine audit
- Goal alignment scoring

## Phase 3 — Progressive Paths

- 7-day journey
- 30-day journey
- Adaptive reinforcement

## Phase 4 — Buddy Circles

- Small group matching
- Shared growth tracking

---

# 17. Why This Architecture

Serverless:
- Scales to zero
- No idle cost
- Clean hackathon deploy

Titan embeddings:
- Cheap
- High dimensional
- Reliable for similarity

Claude:
- Strong reasoning
- Structured JSON generation

DynamoDB:
- Simple
- Auto-scaling
- Low operational overhead

Monorepo:
- Fast iteration
- Clean deployment
- Shared versioning

---

# 18. Technical Depth Highlights

- Adaptive LLM question generation
- Structured embedding document design
- Weighted signal aggregation
- Vector normalization
- Cosine similarity matching
- Goal prototype vector comparison
- AI-assisted behavioral analytics

This is not a chatbot wrapper.
AI is load-bearing.

---

# 19. Demo Day Narrative

Problem:
Youth digital consumption lacks direction.

Solution:
AI-powered taste graph → growth path engine.

Technical Proof:
Live embedding generation.
Live matching.
Live path generation.
Deployed on AWS.

---

# 20. Future Extensions

- Spotify ingestion
- YouTube ingestion
- Goodreads integration
- Regional taste modeling
- Federated embedding storage
- On-device vector storage
- Vector compression
- Hybrid recommenders (Personalize + embeddings)

---

# 21. Risks & Mitigations

LLM hallucination:
→ Strict structured prompts.

Embedding drift:
→ Version embedding schema.

Cold start:
→ Seed archetype prototypes.

Scaling matching:
→ Move to vector index if >50k users.

---

# 22. Alpha Status

This document describes:

- Architectural intent
- Execution strategy
- Deployment model
- AI pipeline design

Alpha does not include:
- Progressive journeys
- Full analytics depth
- Production security hardening

---

# 23. Conclusion

VibeGraph is not a recommendation engine.

It is:

- A taste identity layer
- A vectorized growth compass
- A privacy-first algorithm
- A structured digital redirection system

This architecture is designed for:

- Hackathon execution
- MVP scalability
- Production evolution