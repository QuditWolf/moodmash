# Implementation Plan: VibeGraph Backend Integration

## Overview

This implementation plan integrates the VibeGraph backend with the existing React frontend using Docker containerization. The system is organized into separate containers for frontend, backend services, and supporting infrastructure. Each container is self-contained with its own dependencies and build process. The implementation focuses on getting everything working with proper API communication between containers, with comprehensive modular documentation in the docs/ directory.

## Architecture Changes

- **Containerization**: Frontend, backend handlers, and services run in separate Docker containers
- **No Session Expiration**: Removed 1-hour session TTL requirement for MVP
- **Docker Compose**: Orchestrates all containers with proper networking
- **Makefile**: Provides convenient commands for building, running, and managing containers
- **Modular Documentation**: All .md files organized in docs/ by component (frontend/, backend/, infrastructure/)

## Tasks

- [x] 1. Plan Docker architecture and container structure
  - Define container boundaries: frontend, backend-api, backend-services, database
  - Plan network communication between containers
  - Design volume mounts for development and production
  - Document container dependencies and startup order
  - Create architecture diagram for containerized system

- [ ] 2. Set up project structure and documentation organization
  - [x] 2.1 Create modular docs/ directory structure
    - Create docs/frontend/ for frontend documentation
    - Create docs/backend/ for backend documentation
    - Create docs/infrastructure/ for Docker and deployment docs
    - Create docs/api/ for API contracts and specifications
    - Move existing .md files to appropriate docs/ subdirectories

  - [x] 2.2 Create backend documentation structure
    - Create docs/backend/handlers/ for Lambda handler documentation
    - Create docs/backend/services/ for service layer documentation
    - Create docs/backend/utils/ for utility function documentation
    - Create docs/backend/README.md as backend overview
    - Document each backend component with purpose, inputs, outputs, and examples

  - [x] 2.3 Create frontend documentation structure
    - Create docs/frontend/components/ for component documentation
    - Create docs/frontend/services/ for API service documentation
    - Create docs/frontend/README.md as frontend overview
    - Document component props, state, and usage examples

  - [x] 2.4 Create infrastructure documentation
    - Create docs/infrastructure/docker.md for Docker setup
    - Create docs/infrastructure/docker-compose.md for orchestration
    - Create docs/infrastructure/makefile.md for build commands
    - Create docs/infrastructure/networking.md for container communication

- [x] 3. Create Docker configuration for frontend
  - [x] 3.1 Create frontend/Dockerfile
    - Use Node.js 20 Alpine as base image
    - Copy package.json and package-lock.json
    - Install dependencies in Docker layer (npm ci)
    - Copy source code
    - Build Vite production bundle
    - Use nginx to serve static files
    - Expose port 3000

  - [x] 3.2 Create frontend/.dockerignore
    - Exclude node_modules, dist, .env files
    - Exclude development files and caches

  - [x] 3.3 Create frontend environment configuration
    - Create frontend/.env.docker with API_URL pointing to backend container
    - Document environment variables in docs/frontend/configuration.md

- [x] 4. Create Docker configuration for backend API gateway
  - [x] 4.1 Create backend/api/Dockerfile
    - Use Python 3.11 slim as base image
    - Copy requirements.txt
    - Install Python dependencies in Docker layer (pip install)
    - Copy API gateway source code
    - Expose port 8000
    - Set up FastAPI or Flask as API gateway

  - [x] 4.2 Create backend/api/.dockerignore
    - Exclude __pycache__, .pytest_cache, .env files
    - Exclude virtual environments

  - [x] 4.3 Create backend/api/requirements.txt
    - Add FastAPI or Flask
    - Add uvicorn for ASGI server
    - Add boto3 for AWS SDK
    - Add python-jose for JWT handling
    - Add pydantic for validation

  - [x] 4.4 Create API gateway entry point
    - Create backend/api/main.py with FastAPI app
    - Set up CORS middleware for frontend communication
    - Define health check endpoint
    - Set up request logging

- [x] 5. Create Docker configuration for backend handlers
  - [x] 5.1 Create backend/handlers/Dockerfile
    - Use Python 3.11 slim as base image
    - Copy requirements.txt
    - Install dependencies in Docker layer
    - Copy handler source code
    - Set up handler execution environment

  - [x] 5.2 Create backend/handlers/requirements.txt
    - Add boto3 for AWS Bedrock
    - Add numpy for vector operations
    - Add pydantic for validation
    - Add python-dotenv for environment variables

- [x] 6. Create Docker configuration for backend services
  - [x] 6.1 Create backend/services/Dockerfile
    - Use Python 3.11 slim as base image
    - Copy requirements.txt
    - Install dependencies in Docker layer
    - Copy service source code

  - [x] 6.2 Create backend/services/requirements.txt
    - Add boto3 for DynamoDB and Bedrock
    - Add cryptography for hashing
    - Add pydantic for data models

- [x] 7. Set up DynamoDB Local container
  - [x] 7.1 Configure DynamoDB Local in docker-compose
    - Use amazon/dynamodb-local image
    - Expose port 8001
    - Configure data persistence with volume mount

  - [x] 7.2 Create DynamoDB initialization script
    - Create backend/scripts/init-dynamodb.py
    - Define Users table schema (no TTL for sessions)
    - Define Sessions table schema (removed expiresAt requirement)
    - Define EmbeddingCache table schema
    - Auto-create tables on container startup

- [x] 8. Create docker-compose.yml
  - [ ] 8.1 Define all services
    - frontend: React app with nginx
    - backend-api: API gateway (FastAPI/Flask)
    - backend-handlers: Handler services
    - backend-services: Shared services
    - dynamodb-local: Local DynamoDB
    - localstack: Mock AWS services (Bedrock)

  - [ ] 8.2 Configure networking
    - Create vibegraph-network bridge network
    - Assign service names for DNS resolution
    - Configure port mappings (frontend:3000, api:8000, dynamodb:8001, localstack:4566)
    - Set network aliases for service discovery

  - [ ] 8.3 Configure volumes
    - Mount frontend/src for hot reload in development
    - Mount backend code for development
    - Persist DynamoDB data with named volume
    - Share logs directory across containers
    - Mount configuration files

  - [ ] 8.4 Configure environment variables
    - Set API_URL for frontend (http://backend-api:8000)
    - Set AWS_ENDPOINT for backend (http://dynamodb-local:8001)
    - Set BEDROCK_ENDPOINT for backend (http://localstack:4566)
    - Set DATABASE_URL for backend services
    - Set LOG_LEVEL for all services

  - [ ] 8.5 Define service dependencies and startup order
    - frontend depends_on backend-api (condition: service_healthy)
    - backend-api depends_on dynamodb-local (condition: service_healthy)
    - backend-api depends_on localstack (condition: service_healthy)
    - backend-handlers depends_on backend-services (condition: service_started)
    - Use depends_on with health check conditions for proper startup

  - [ ] 8.6 Configure health checks for all services
    - frontend: test: ["CMD", "curl", "-f", "http://localhost:3000"]
    - backend-api: test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    - dynamodb-local: test: ["CMD-SHELL", "aws dynamodb list-tables --endpoint-url http://localhost:8001"]
    - localstack: test: ["CMD", "curl", "-f", "http://localhost:4566/_localstack/health"]
    - Set interval: 30s, timeout: 10s, retries: 3, start_period: 40s

  - [ ] 8.7 Configure restart policies
    - Set restart: unless-stopped for all services
    - Ensure containers restart on failure
    - Document restart behavior in docs/infrastructure/docker-compose.md

- [x] 9. Create Makefile for container management
  - [ ] 9.1 Create root Makefile with targets
    - `make build`: Build all Docker images
    - `make up`: Start all containers with docker-compose up
    - `make down`: Stop all containers
    - `make restart`: Restart all containers
    - `make logs`: View logs from all containers
    - `make logs-frontend`: View frontend logs only
    - `make logs-backend`: View backend logs only
    - `make clean`: Remove all containers, volumes, and images
    - `make shell-frontend`: Open shell in frontend container
    - `make shell-backend`: Open shell in backend container
    - `make test`: Run all tests in containers
    - `make init-db`: Initialize DynamoDB tables
    - `make health`: Check health of all containers
    - `make monitor`: Continuously monitor health status
    - `make ps`: Show container status with health checks

  - [ ] 9.2 Add development convenience targets
    - `make dev`: Start containers in development mode with hot reload
    - `make prod`: Start containers in production mode
    - `make rebuild`: Clean and rebuild all images
    - `make reset`: Stop containers, clean volumes, rebuild, and start fresh

  - [ ] 9.3 Add health check and validation targets
    - `make wait-healthy`: Wait for all containers to be healthy (timeout 120s)
    - `make check-connections`: Verify all inter-service connections
    - `make validate`: Run health checks and connection tests
    - `make diagnose`: Run diagnostic checks and output detailed status

  - [ ] 9.4 Document Makefile usage
    - Create docs/infrastructure/makefile.md
    - Document each target with description and usage examples
    - Include troubleshooting section for common issues

- [ ] 10. Implement backend API gateway routes
  - [ ] 10.1 Create quiz endpoints in backend/api/routes/quiz.py
    - POST /api/quiz/section1/start - Start Section 1 (no session expiration)
    - POST /api/quiz/section2/generate - Generate Section 2
    - POST /api/quiz/complete - Complete quiz and generate embedding

  - [ ] 10.2 Create profile endpoints in backend/api/routes/profile.py
    - GET /api/profile/dna/:userId - Get taste DNA
    - GET /api/profile/path/:userId - Get growth path
    - GET /api/profile/matches/:userId - Get taste matches
    - GET /api/profile/analytics/:userId - Get analytics

  - [ ] 10.3 Set up route registration in main.py
    - Register quiz routes with /api/quiz prefix
    - Register profile routes with /api/profile prefix
    - Add request/response logging middleware

  - [ ] 10.4 Create API documentation
    - Document all endpoints in docs/api/endpoints.md
    - Include request/response examples
    - Document error codes and messages

- [x] 11. Implement core backend utilities
  - [ ] 11.1 Create vector operations in backend/utils/vector_ops.py
    - Implement normalize_vector() function
    - Implement cosine_similarity() function
    - Add input validation for vector dimensions

  - [ ] 11.2 Create embedding builder in backend/utils/embedding_builder.py
    - Implement build_embedding_document() function
    - Format quiz answers into semantic text
    - Ensure consistent formatting for caching

  - [ ] 11.3 Create validation utilities in backend/utils/validation.py
    - Implement validate_quiz_answers() function
    - Implement validate_uuid() function
    - Implement validate_vector() function
    - Remove session expiration validation

  - [ ] 11.4 Document utilities
    - Create docs/backend/utils/vector-operations.md
    - Create docs/backend/utils/embedding-builder.md
    - Create docs/backend/utils/validation.md

- [x] 12. Implement backend service clients
  - [ ] 12.1 Create DynamoDB client in backend/services/dynamodb_client.py
    - Implement get(), put(), update(), scan() methods
    - Configure endpoint for DynamoDB Local in Docker
    - Add retry logic with exponential backoff

  - [ ] 12.2 Create Bedrock client in backend/services/bedrock_client.py
    - Implement Claude service for text generation
    - Implement Titan service for embeddings
    - Configure endpoint for LocalStack in Docker
    - Add retry logic for API failures

  - [ ] 12.3 Create cache service in backend/services/cache_service.py
    - Implement get() and put() methods for embedding cache
    - Use SHA-256 hashing for cache keys
    - Track hit count and last accessed timestamp

  - [ ] 12.4 Document services
    - Create docs/backend/services/dynamodb.md
    - Create docs/backend/services/bedrock.md
    - Create docs/backend/services/cache.md

- [x] 13. Implement backend handlers
  - [ ] 13.1 Create generateSection1 handler in backend/handlers/generate_section1.py
    - Generate sessionId (no expiration tracking)
    - Call Claude to generate 5 foundational questions
    - Store session in DynamoDB (removed expiresAt field)
    - Return sessionId and questions

  - [ ] 13.2 Create generateSection2 handler in backend/handlers/generate_section2.py
    - Retrieve session from DynamoDB (no expiration check)
    - Generate adaptive questions based on Section 1 answers
    - Update session with Section 2 data

  - [ ] 13.3 Create generateEmbedding handler in backend/handlers/generate_embedding.py
    - Build embedding document from quiz answers
    - Check cache for existing embedding
    - Call Titan v2 to generate 1024-dim vector
    - Normalize vector and store in Users table

  - [ ] 13.4 Create generateDNA handler in backend/handlers/generate_dna.py
    - Call Claude to generate taste DNA archetype
    - Parse traits, categories, and description
    - Store DNA profile in Users table

  - [ ] 13.5 Create generatePath handler in backend/handlers/generate_path.py
    - Retrieve user DNA profile
    - Call Claude to generate Absorb/Create/Reflect recommendations
    - Store growth path in Users table

  - [ ] 13.6 Create findMatches handler in backend/handlers/find_matches.py
    - Retrieve user embedding vector
    - Calculate cosine similarity with all users
    - Filter matches with similarity > 0.7
    - Sort and return top matches

  - [ ] 13.7 Create generateAnalytics handler in backend/handlers/generate_analytics.py
    - Retrieve user DNA and growth path
    - Call Claude to generate behavioral insights
    - Store analytics in Users table

  - [ ] 13.8 Document handlers
    - Create docs/backend/handlers/ with individual handler docs
    - Document inputs, outputs, and error handling for each

- [x] 14. Implement frontend API service
  - [ ] 14.1 Create frontend/src/services/vibeGraphAPI.js
    - Implement apiRequest() wrapper with fetch
    - Add authentication token handling
    - Configure API base URL from environment variable

  - [ ] 14.2 Implement quiz API methods
    - startSection1() - POST /api/quiz/section1/start
    - generateSection2() - POST /api/quiz/section2/generate
    - completeQuiz() - POST /api/quiz/complete

  - [ ] 14.3 Implement profile API methods
    - getTasteDNA() - GET /api/profile/dna/:userId
    - getGrowthPath() - GET /api/profile/path/:userId
    - getMatches() - GET /api/profile/matches/:userId
    - getAnalytics() - GET /api/profile/analytics/:userId

  - [ ] 14.4 Document API service
    - Create docs/frontend/services/vibegraph-api.md
    - Document all methods with examples

- [x] 15. Update OnboardingPage component
  - [ ] 15.1 Integrate API service into OnboardingPage
    - Replace static questions with API calls
    - Add sessionId state management (no expiration handling)
    - Implement multi-phase flow (section1 → section2 → processing → complete)

  - [ ] 15.2 Add error handling
    - Display error messages for API failures
    - Add retry buttons for failed requests
    - Handle network errors gracefully

  - [ ] 15.3 Document component changes
    - Update docs/frontend/components/onboarding-page.md
    - Document state management and API integration

- [x] 16. Set up container networking and communication
  - [ ] 16.1 Configure CORS in backend API
    - Allow requests from frontend container
    - Set appropriate CORS headers (Access-Control-Allow-Origin, Methods, Headers)
    - Configure preflight OPTIONS handling
    - Document CORS configuration in docs/infrastructure/networking.md

  - [ ] 16.2 Implement comprehensive health check system
    - Create backend/api/health.py with health check logic
    - Implement /health endpoint for basic liveness check
    - Implement /health/ready endpoint for readiness check
    - Implement /health/db endpoint to verify DynamoDB connection
    - Implement /health/bedrock endpoint to verify Bedrock connection
    - Implement /health/cache endpoint to verify cache service
    - Return detailed status with timestamps and response times
    - Return 200 for healthy, 503 for unhealthy

  - [ ] 16.3 Add Docker health checks to docker-compose.yml
    - Add healthcheck for frontend container (curl http://localhost:3000)
    - Add healthcheck for backend-api (curl http://localhost:8000/health)
    - Add healthcheck for dynamodb-local (aws dynamodb list-tables)
    - Configure interval: 30s, timeout: 10s, retries: 3
    - Set start_period: 40s for initialization time

  - [ ] 16.4 Create connection validation utilities
    - Create backend/utils/connection_check.py
    - Implement check_dynamodb_connection() with table list verification
    - Implement check_bedrock_connection() with model availability check
    - Implement check_network_connectivity() for inter-service communication
    - Add retry logic with exponential backoff for transient failures
    - Log connection status and errors

  - [ ] 16.5 Implement startup dependency checks
    - Create backend/api/startup.py with initialization checks
    - Verify DynamoDB tables exist before accepting requests
    - Verify Bedrock models are accessible
    - Verify cache service is operational
    - Fail fast with clear error messages if dependencies unavailable
    - Add startup timeout (60 seconds) with retry logic

  - [ ] 16.6 Test inter-container communication
    - Verify frontend can reach backend-api via service name
    - Verify backend-api can reach dynamodb-local via service name
    - Verify backend-api can reach localstack via service name
    - Test DNS resolution between containers
    - Test network latency between services
    - Document network topology in docs/infrastructure/networking.md

  - [ ] 16.7 Create connection monitoring dashboard
    - Add /health/status endpoint returning all service statuses
    - Include response times for each dependency
    - Include last successful connection timestamp
    - Include error counts and last error message
    - Format as JSON for programmatic access
    - Document in docs/api/health-endpoints.md

- [x] 17. Create environment configuration files
  - [ ] 17.1 Create .env.example files
    - Create frontend/.env.example with VITE_API_URL
    - Create backend/.env.example with AWS endpoints and credentials
    - Document all environment variables

  - [ ] 17.2 Create docker-compose.override.yml for local development
    - Override environment variables for local development
    - Enable hot reload for frontend and backend
    - Mount source code as volumes

  - [ ] 17.3 Document environment setup
    - Create docs/infrastructure/environment.md
    - Document required environment variables
    - Provide setup instructions for development and production

- [x] 18. Implement logging and monitoring
  - [ ] 18.1 Set up structured logging in backend
    - Configure Python logging with JSON formatter
    - Log all API requests and responses
    - Log handler execution times

  - [ ] 18.2 Set up frontend logging
    - Configure console logging for development
    - Add error boundary for React components
    - Log API errors with context

  - [ ] 18.3 Create log aggregation
    - Mount logs directory as volume in docker-compose
    - Configure log rotation
    - Document logging in docs/infrastructure/logging.md

- [x] 19. Create initialization and setup scripts
  - [ ] 19.1 Create backend/scripts/init-dynamodb.py
    - Create Users table with userId as partition key
    - Create Sessions table with sessionId as partition key (no TTL)
    - Create EmbeddingCache table with docHash as partition key
    - Add retry logic for table creation (wait for DynamoDB ready)
    - Verify tables exist after creation
    - Run automatically on container startup

  - [ ] 19.2 Create backend/scripts/seed-data.py
    - Create sample users for testing
    - Create sample embeddings for matching tests
    - Create sample DNA profiles
    - Add --reset flag to clear existing data
    - Document seeding in docs/backend/scripts.md

  - [ ] 19.3 Create docker-entrypoint.sh scripts
    - Create frontend/docker-entrypoint.sh for frontend initialization
    - Create backend/docker-entrypoint.sh for backend initialization
    - Add wait-for-it.sh logic to wait for dependencies
    - Run health checks before starting main process
    - Make scripts executable (chmod +x)

  - [ ] 19.4 Create wait-for-service utility
    - Create scripts/wait-for-service.sh
    - Wait for service to be healthy before proceeding
    - Support timeout parameter (default 120s)
    - Poll health endpoint every 5 seconds
    - Exit with error if timeout exceeded
    - Use in docker-entrypoint.sh scripts

  - [ ] 19.5 Create connection validation script
    - Create backend/scripts/validate-connections.py
    - Check DynamoDB connection and list tables
    - Check Bedrock connection and list models
    - Check cache service availability
    - Print detailed status report
    - Exit with non-zero code if any check fails
    - Run as part of container startup

- [x] 20. Create comprehensive documentation
  - [ ] 20.1 Create main README files
    - Create docs/README.md as documentation index
    - Create docs/frontend/README.md with frontend overview
    - Create docs/backend/README.md with backend overview
    - Create docs/infrastructure/README.md with setup guide

  - [ ] 20.2 Create API documentation
    - Create docs/api/README.md with API overview
    - Create docs/api/quiz-endpoints.md
    - Create docs/api/profile-endpoints.md
    - Include request/response examples and error codes

  - [ ] 20.3 Create Docker documentation
    - Create docs/infrastructure/docker-setup.md
    - Document Dockerfile for each container
    - Document docker-compose configuration
    - Include troubleshooting guide

  - [ ] 20.4 Create development guide
    - Create docs/DEVELOPMENT.md with setup instructions
    - Document how to run containers locally
    - Document how to run tests
    - Include common issues and solutions

  - [ ] 20.5 Move existing documentation
    - Move design.md to docs/architecture/design.md
    - Move requirements.md to docs/architecture/requirements.md
    - Update references in all documentation

- [x] 21. Test container orchestration and health
  - [ ] 21.1 Test build process
    - Run `make build` and verify all images build successfully
    - Check for build errors and dependency issues
    - Verify image sizes are reasonable
    - Test build cache effectiveness

  - [ ] 21.2 Test container startup and health checks
    - Run `make up` and verify all containers start
    - Wait for all health checks to pass (check docker ps)
    - Verify containers reach healthy state within timeout
    - Check container logs for startup errors
    - Test automatic restart on failure

  - [ ] 21.3 Test health check endpoints
    - Test GET /health returns 200 with status "healthy"
    - Test GET /health/ready returns 200 when all dependencies ready
    - Test GET /health/db returns 200 with DynamoDB connection status
    - Test GET /health/bedrock returns 200 with Bedrock connection status
    - Test GET /health/cache returns 200 with cache service status
    - Test GET /health/status returns comprehensive status JSON
    - Verify health checks fail appropriately when services down

  - [ ] 21.4 Test inter-container communication
    - Test frontend can reach backend API at http://backend-api:8000
    - Test backend can reach DynamoDB Local at http://dynamodb-local:8001
    - Test backend can reach LocalStack at http://localstack:4566
    - Verify DNS resolution works for all service names
    - Test network latency is acceptable (<100ms)
    - Verify network isolation between containers

  - [ ] 21.5 Test connection resilience
    - Stop DynamoDB container and verify backend health check fails
    - Restart DynamoDB and verify backend recovers automatically
    - Test retry logic for transient connection failures
    - Verify error messages are clear and actionable
    - Test graceful degradation when optional services unavailable

  - [ ] 21.6 Test API endpoints end-to-end
    - Test quiz flow: Section 1 → Section 2 → Complete
    - Test profile endpoints: DNA, Path, Matches, Analytics
    - Verify responses are correct and well-formed
    - Test error handling for invalid requests
    - Verify CORS headers are present in responses
    - Test authentication token flow

  - [ ] 21.7 Create health check monitoring script
    - Create scripts/monitor-health.sh
    - Poll all health endpoints every 10 seconds
    - Display status in terminal with colors (green/red)
    - Alert on status changes
    - Log health check history
    - Add to Makefile as `make monitor`

- [x] 22. Create testing infrastructure
  - [ ] 22.1 Set up backend unit tests
    - Create backend/tests/ directory structure
    - Add pytest configuration
    - Create test fixtures for mocking AWS services
    - Add tests to Makefile (`make test-backend`)

  - [ ] 22.2 Set up frontend unit tests
    - Create frontend/tests/ directory structure
    - Configure Jest and React Testing Library
    - Create test fixtures for API mocking
    - Add tests to Makefile (`make test-frontend`)

  - [ ] 22.3 Set up integration tests
    - Create tests/integration/ directory
    - Write end-to-end flow tests
    - Test complete quiz flow in containers
    - Add integration tests to Makefile (`make test-integration`)

  - [ ] 22.4 Document testing
    - Create docs/testing/README.md
    - Document how to run tests
    - Document test coverage requirements

- [x] 23. Optimize Docker images and builds
  - [ ] 23.1 Optimize frontend Dockerfile
    - Use multi-stage build to reduce image size
    - Cache npm dependencies layer
    - Minimize final image with nginx alpine

  - [ ] 23.2 Optimize backend Dockerfiles
    - Use multi-stage builds for Python images
    - Cache pip dependencies layer
    - Remove unnecessary build dependencies

  - [ ] 23.3 Configure Docker build cache
    - Use BuildKit for faster builds
    - Configure cache mounts in docker-compose
    - Document build optimization in docs/infrastructure/optimization.md

- [x] 24. Final validation and documentation review
  - [ ] 24.1 Validate complete system
    - Run `make clean && make build && make up`
    - Test complete onboarding flow
    - Test all API endpoints
    - Verify all containers are healthy

  - [ ] 24.2 Review and update documentation
    - Verify all docs/ files are accurate
    - Check for broken links and references
    - Ensure examples are up-to-date
    - Add troubleshooting sections

  - [ ] 24.3 Create quick start guide
    - Create docs/QUICKSTART.md
    - Document minimal steps to get system running
    - Include prerequisites (Docker, Docker Compose)
    - Document health check verification steps
    - Include common issues and solutions
    - Add troubleshooting section for connection issues

  - [ ] 24.4 Create deployment guide
    - Create docs/DEPLOYMENT.md
    - Document production deployment steps
    - Include security considerations
    - Document environment variable configuration
    - Include health check monitoring setup
    - Document backup and recovery procedures

  - [ ] 24.5 Create troubleshooting guide
    - Create docs/TROUBLESHOOTING.md
    - Document common container startup issues
    - Document health check failure scenarios
    - Document connection timeout issues
    - Include diagnostic commands (docker logs, docker inspect)
    - Add solutions for common problems
    - Include contact information for support

## Notes

- All containers are self-contained with dependencies installed in Docker layers
- Session expiration (1-hour TTL) has been removed per requirements
- Frontend runs in separate container with nginx
- Backend is split into multiple containers: api, handlers, services
- DynamoDB Local used for development (no AWS required)
- LocalStack used to mock AWS Bedrock services
- Makefile provides convenient commands for all operations
- Documentation is modular and organized in docs/ directory
- Each component has its own README and detailed documentation
- Docker Compose orchestrates all containers with proper networking
- Hot reload enabled for development mode
- Production mode uses optimized builds

  - Create Python project structure for Lambda functions
  - Set up shared utilities module for vector operations
  - Configure AWS SAM template with Lambda functions and API Gateway
  - Set up DynamoDB tables (Users, Sessions, EmbeddingCache)
  - Configure environment variables and secrets management
  - _Requirements: 3.1, 10.1, 16.1_

- [ ] 2. Implement core vector operations utilities
  - [ ] 2.1 Implement vector normalization function
    - Create `normalize_vector()` function that calculates magnitude and normalizes to unit length
    - Ensure magnitude calculation uses square root of sum of squared elements
    - Validate output vector has magnitude approximately 1.0 within 0.0001 tolerance
    - _Requirements: 11.1, 11.2, 11.3_

  - [ ] 2.2 Write property test for vector normalization
    - **Property 2: Embedding Vector Normalization**
    - **Validates: Requirements 3.7, 11.3, 12.8, 12.9**

  - [ ] 2.3 Implement cosine similarity function
    - Create `cosine_similarity()` function that computes dot product of normalized vectors
    - Ensure result is always between -1 and 1
    - Handle edge cases (identical vectors return 1.0, negated vectors return -1.0)
    - _Requirements: 11.4, 11.5, 11.6, 11.7_

  - [ ] 2.4 Write property test for cosine similarity bounds
    - **Property 3: Cosine Similarity Bounds**
    - **Validates: Requirements 11.5, 11.6, 11.7**


- [ ] 3. Implement embedding document builder and weighting engine
  - [ ] 3.1 Create embedding document builder
    - Implement `build_embedding_document()` function that structures quiz answers into semantic text
    - Ensure document length is between 500-2000 characters
    - Format consistently for caching purposes
    - _Requirements: 3.1_

  - [ ] 3.2 Write unit tests for embedding document builder
    - Test document structure with various answer patterns
    - Test document length constraints
    - Test consistent formatting for identical answers
    - _Requirements: 3.1_

  - [ ] 3.3 Implement weighting engine
    - Create `apply_weights()` function that adjusts vector dimensions based on answer patterns
    - Load weighting rules from configuration
    - Apply weights without normalizing (normalization happens separately)
    - _Requirements: 3.6_

  - [ ] 3.4 Write unit tests for weighting engine
    - Test weight application with known vectors
    - Test that weighted values remain valid numbers
    - Test weighting rules are applied consistently
    - _Requirements: 3.6_

- [ ] 4. Implement AWS service clients and helpers
  - [ ] 4.1 Create Claude service client
    - Implement `ClaudeService` class with `invoke()` method
    - Configure Bedrock runtime client for Claude 3.5 Sonnet
    - Add retry logic with exponential backoff (3 attempts)
    - Handle API errors and timeouts gracefully
    - _Requirements: 13.1, 13.2_

  - [ ] 4.2 Create Titan embedding service client
    - Implement `TitanService` class with `generate_embedding()` method
    - Configure Bedrock runtime client for Titan v2
    - Add retry logic (2 attempts)
    - Validate embedding dimensions (must be 1024)
    - _Requirements: 13.3, 13.4_

  - [ ] 4.3 Create DynamoDB client wrapper
    - Implement `DynamoClient` class with put, get, update, scan methods
    - Add retry logic with exponential backoff (100ms, 200ms, 400ms)
    - Handle throttling and service errors
    - _Requirements: 13.5, 13.6_

  - [ ] 4.4 Create embedding cache service
    - Implement `CacheService` class with get/put methods
    - Use SHA-256 hashing for cache keys
    - Track hit count and last accessed timestamp
    - _Requirements: 16.1, 16.2, 16.3, 16.4_

  - [ ] 4.5 Write unit tests for service clients
    - Mock AWS SDK calls and test retry logic
    - Test error handling for various failure scenarios
    - Test cache hit/miss behavior
    - _Requirements: 13.1-13.6, 16.1-16.4_


- [ ] 5. Implement input validation utilities
  - [ ] 5.1 Create quiz answer validation functions
    - Implement `validate_section1_answers()` to check exactly 5 answers
    - Implement `validate_answer_structure()` to check questionId and selectedOptions
    - Validate each answer has at least one selected option
    - Validate option strings are at most 500 characters
    - _Requirements: 12.1, 12.2, 12.3, 12.4_

  - [ ] 5.2 Create ID validation functions
    - Implement `validate_uuid()` for sessionId and userId validation
    - Implement `validate_vector()` to check 1024 dimensions and value bounds
    - _Requirements: 12.5, 12.6, 12.8, 12.9_

  - [ ] 5.3 Write property test for input validation
    - **Property 14: Input Validation Bounds**
    - **Validates: Requirements 12.4, 12.5, 12.6**

  - [ ] 5.4 Write unit tests for validation functions
    - Test validation with valid and invalid inputs
    - Test error messages are descriptive
    - Test edge cases (empty arrays, null values, boundary lengths)
    - _Requirements: 12.1-12.9_

- [ ] 6. Implement generateSection1 Lambda function
  - [ ] 6.1 Create Lambda handler for Section 1 generation
    - Implement handler that generates sessionId and timestamp
    - Load adaptive quiz prompt from file
    - Call Claude service to generate 5 foundational questions
    - Parse questions from Claude response
    - Store session in DynamoDB with 1-hour TTL
    - Return sessionId, questions, and expiresAt
    - _Requirements: 1.1, 1.2, 1.3, 1.4_

  - [ ] 6.2 Add error handling and logging
    - Catch Claude API failures and return 500 error
    - Log session creation to CloudWatch
    - Implement retry logic for Claude calls
    - _Requirements: 1.5, 13.1, 13.2, 18.1_

  - [ ] 6.3 Write property test for session lifecycle
    - **Property 1: Session Lifecycle Integrity**
    - **Validates: Requirements 1.2, 2.4, 2.5, 10.1, 10.4, 10.5**

  - [ ] 6.4 Write unit tests for generateSection1
    - Mock Claude service and DynamoDB client
    - Test successful question generation
    - Test error handling for Claude failures
    - Test session storage with correct TTL
    - _Requirements: 1.1-1.5_


- [ ] 7. Implement generateSection2 Lambda function
  - [ ] 7.1 Create Lambda handler for Section 2 generation
    - Implement handler that retrieves session from DynamoDB
    - Validate session exists and has not expired
    - Build context from Section 1 answers
    - Call Claude service to generate 5 adaptive questions
    - Update session with Section 1 answers and Section 2 questions
    - Update session status to "section2_complete"
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_

  - [ ] 7.2 Add error handling and logging
    - Return 404 for expired or missing sessions
    - Catch Claude API failures and return 500 error
    - Log Section 2 generation to CloudWatch
    - _Requirements: 2.2, 13.1, 13.2_

  - [ ] 7.3 Write unit tests for generateSection2
    - Mock session retrieval and Claude service
    - Test adaptive question generation based on Section 1
    - Test session expiration handling
    - Test session update with correct status
    - _Requirements: 2.1-2.5_

- [ ] 8. Checkpoint - Ensure quiz generation works end-to-end
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Implement generateEmbedding Lambda function
  - [ ] 9.1 Create Lambda handler for embedding generation
    - Implement handler that builds embedding document from quiz answers
    - Compute SHA-256 hash of document
    - Check embedding cache for existing vector
    - On cache miss, call Titan service to generate 1024-dim vector
    - On cache hit, retrieve cached vector and increment hit count
    - Apply weighting engine to vector
    - Normalize weighted vector to unit length
    - Store vector in Users table (NOT raw answers)
    - Update cache with new embeddings
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9_

  - [ ] 9.2 Add error handling and logging
    - Return 500 for Titan failures after retries
    - Do NOT store partial data on failure
    - Log cache hits and Titan API calls
    - Ensure no raw quiz answers are logged
    - _Requirements: 3.10, 13.3, 13.4, 18.3, 18.4, 18.5_

  - [ ] 9.3 Write property test for embedding vector normalization
    - **Property 2: Embedding Vector Normalization**
    - **Validates: Requirements 3.7, 11.3, 12.8, 12.9**

  - [ ] 9.4 Write property test for cache consistency
    - **Property 6: Embedding Cache Consistency**
    - **Validates: Requirements 3.2, 3.3, 16.1, 16.2**

  - [ ] 9.5 Write property test for privacy-first storage
    - **Property 7: Privacy-First Data Storage**
    - **Validates: Requirements 3.9, 15.1, 15.2, 15.3**

  - [ ] 9.6 Write unit tests for generateEmbedding
    - Mock Titan service and cache service
    - Test cache hit and miss scenarios
    - Test vector normalization
    - Test that raw answers are never stored
    - _Requirements: 3.1-3.10_


- [ ] 10. Implement generateDNA Lambda function
  - [ ] 10.1 Create Lambda handler for DNA generation
    - Implement handler that summarizes quiz answers
    - Load DNA generation prompt from file
    - Call Claude service to generate DNA profile
    - Parse archetype, traits, categories, and description from response
    - Store DNA profile in Users table
    - _Requirements: 4.1, 4.2, 4.5_

  - [ ] 10.2 Add validation and error handling
    - Validate DNA structure has all required fields
    - Validate trait scores are between 0-10
    - Return 500 for Claude failures
    - Log DNA generation completion
    - _Requirements: 4.3, 4.4, 4.6_

  - [ ] 10.3 Write property test for DNA structure completeness
    - **Property 9: DNA Profile Structure Completeness**
    - **Validates: Requirements 4.2, 4.3, 4.4**

  - [ ] 10.4 Write unit tests for generateDNA
    - Mock Claude service and DynamoDB client
    - Test DNA profile parsing
    - Test trait and category validation
    - Test error handling
    - _Requirements: 4.1-4.6_

- [ ] 11. Implement generatePath Lambda function
  - [ ] 11.1 Create Lambda handler for growth path generation
    - Implement handler that retrieves user DNA profile
    - Return 404 if user or DNA not found
    - Build context from DNA archetype and traits
    - Load path generation prompt from file
    - Call Claude service to generate growth path
    - Parse Absorb, Create, and Reflect categories
    - Store path in Users table with timestamp
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.7_

  - [ ] 11.2 Add validation and error handling
    - Validate each category contains 3-5 recommendations
    - Validate each recommendation has all required fields
    - Return 500 for Claude failures
    - _Requirements: 5.5, 5.6_

  - [ ] 11.3 Write property test for growth path structure
    - **Property 10: Growth Path Structure Completeness**
    - **Validates: Requirements 5.4, 5.5, 5.6**

  - [ ] 11.4 Write unit tests for generatePath
    - Mock user retrieval and Claude service
    - Test path generation with various DNA profiles
    - Test recommendation validation
    - Test error handling for missing users
    - _Requirements: 5.1-5.7_


- [ ] 12. Implement findMatches Lambda function
  - [ ] 12.1 Create Lambda handler for taste matching
    - Implement handler that retrieves user's embedding vector
    - Return 404 if user or embedding not found
    - Scan all users from DynamoDB (exclude requesting user)
    - Calculate cosine similarity for each user with valid embedding
    - Filter matches with similarity > 0.7
    - Identify shared traits between users
    - Sort matches by similarity descending
    - Limit results to requested limit (max 50)
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9_

  - [ ] 12.2 Add error handling and logging
    - Return 404 for missing users or embeddings
    - Handle empty match results gracefully
    - Log match count and similarity scores
    - _Requirements: 6.2_

  - [ ] 12.3 Write property test for match similarity threshold
    - **Property 4: Match Similarity Threshold and Exclusion**
    - **Validates: Requirements 6.4, 6.5**

  - [ ] 12.4 Write property test for match results ordering
    - **Property 11: Match Results Ordering**
    - **Validates: Requirements 6.7, 6.8, 6.9**

  - [ ] 12.5 Write unit tests for findMatches
    - Mock user embeddings with known similarity scores
    - Test similarity calculation accuracy
    - Test filtering by threshold
    - Test sorting and limiting
    - Test self-exclusion
    - _Requirements: 6.1-6.9_

- [ ] 13. Implement generateAnalytics Lambda function
  - [ ] 13.1 Create Lambda handler for analytics generation
    - Implement handler that retrieves user DNA and growth path
    - Return 404 if user not found
    - Build analytics context from user data
    - Load analytics prompt from file
    - Call Claude service to generate analytics
    - Parse passive/intentional ratio, goal alignment, content balance, insights, recommendations
    - Store analytics in Users table with timestamp
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.7_

  - [ ] 13.2 Add validation and error handling
    - Validate analytics structure has all required fields
    - Validate insight types are valid (strength, opportunity, pattern)
    - Validate content balance trends are valid
    - Return 500 for Claude failures
    - _Requirements: 7.5, 7.6_

  - [ ] 13.3 Write unit tests for generateAnalytics
    - Mock user retrieval and Claude service
    - Test analytics parsing
    - Test insight and content balance validation
    - Test error handling
    - _Requirements: 7.1-7.7_

- [ ] 14. Checkpoint - Ensure all Lambda functions work independently
  - Ensure all tests pass, ask the user if questions arise.


- [ ] 15. Implement frontend API service layer
  - [ ] 15.1 Create vibeGraphAPI.js service module
    - Create base `apiRequest()` function with fetch wrapper
    - Add authentication token handling from localStorage
    - Set Content-Type header to "application/json"
    - Parse JSON responses and handle errors
    - Construct URLs using API base URL from environment variables
    - _Requirements: 8.3, 8.4, 8.5, 8.6, 8.7_

  - [ ] 15.2 Implement quiz API methods
    - Create `startSection1()` method for POST /quiz/section1/start
    - Create `generateSection2()` method for POST /quiz/section2/generate
    - Create `completeQuiz()` method for POST /quiz/complete
    - _Requirements: 8.1_

  - [ ] 15.3 Implement profile API methods
    - Create `getTasteDNA()` method for GET /profile/dna/:userId
    - Create `getGrowthPath()` method for GET /profile/path/:userId
    - Create `getMatches()` method for GET /profile/matches/:userId
    - Create `getAnalytics()` method for GET /profile/analytics/:userId
    - _Requirements: 8.2_

  - [ ] 15.4 Write property test for authentication token inclusion
    - **Property 12: API Authentication Token Inclusion**
    - **Validates: Requirements 8.3**

  - [ ] 15.5 Write unit tests for API service
    - Mock fetch calls and test request/response handling
    - Test authentication token inclusion
    - Test error parsing and throwing
    - Test URL construction
    - _Requirements: 8.1-8.7_

- [ ] 16. Enhance OnboardingPage component
  - [ ] 16.1 Update OnboardingPage state management
    - Add phase state: 'section1' | 'section2' | 'processing' | 'complete'
    - Add sessionId state for tracking quiz session
    - Add section1Questions and section2Questions states
    - Add section1Answers and section2Answers states
    - Add tasteDNA state for completed profile
    - Add loading and error states
    - _Requirements: 9.5, 9.6, 9.7_

  - [ ] 16.2 Implement Section 1 flow
    - Call vibeGraphAPI.quiz.startSection1() on component mount
    - Store sessionId from response
    - Display Section 1 questions from API
    - Collect Section 1 answers
    - Transition to Section 2 phase on completion
    - _Requirements: 9.1, 9.2_

  - [ ] 16.3 Implement Section 2 flow
    - Call vibeGraphAPI.quiz.generateSection2() with sessionId and Section 1 answers
    - Display Section 2 questions from API
    - Collect Section 2 answers
    - Transition to processing phase on completion
    - _Requirements: 9.2_

  - [ ] 16.4 Implement quiz completion flow
    - Call vibeGraphAPI.quiz.completeQuiz() with all answers
    - Show loading indicator during processing phase
    - Store tasteDNA from response
    - Transition to complete phase
    - Display TasteDNACard with DNA profile
    - _Requirements: 9.3, 9.4_

  - [ ] 16.5 Add error handling and retry logic
    - Display error messages for API failures
    - Add retry button for 500/503 errors
    - Redirect to onboarding start for 404 session errors
    - _Requirements: 9.5, 13.7, 13.8_

  - [ ] 16.6 Write property test for session ID persistence
    - **Property 13: Session ID Persistence**
    - **Validates: Requirements 9.6**

  - [ ] 16.7 Write unit tests for OnboardingPage
    - Mock API service calls
    - Test phase transitions
    - Test answer collection
    - Test error handling
    - Test sessionId persistence
    - _Requirements: 9.1-9.7_


- [ ] 17. Implement authentication and authorization
  - [ ] 17.1 Create JWT validation Lambda authorizer
    - Implement authorizer that extracts JWT from Authorization header
    - Validate JWT signature and expiration
    - Extract userId from token
    - Generate IAM policy for API Gateway
    - Return 401 for missing or invalid tokens
    - _Requirements: 14.1, 14.2, 14.3, 14.4_

  - [ ] 17.2 Add user-scoped access control
    - Validate requesting user matches resource userId in Lambda functions
    - Return 403 for unauthorized access attempts
    - _Requirements: 14.5, 14.6_

  - [ ] 17.3 Implement rate limiting
    - Configure API Gateway rate limiting to 100 requests per minute per user
    - _Requirements: 14.7_

  - [ ] 17.4 Write unit tests for authentication
    - Test JWT validation with valid and invalid tokens
    - Test user-scoped access control
    - Test 401 and 403 error responses
    - _Requirements: 14.1-14.6_

- [ ] 18. Implement logging and monitoring
  - [ ] 18.1 Add CloudWatch logging to all Lambda functions
    - Log session creation with sessionId and question count
    - Log API errors with message, stack trace, and request context
    - Log cache hit events
    - Log Titan API calls with timestamp and response time
    - Log Lambda cold starts with duration
    - Log authentication failures with userId and timestamp
    - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.6, 18.7_

  - [ ] 18.2 Implement sensitive data filtering
    - Ensure JWT tokens are never logged
    - Ensure raw quiz answers are never logged
    - Ensure embedding vectors are never logged
    - _Requirements: 18.5_

  - [ ] 18.3 Write property test for sensitive data logging exclusion
    - **Property 16: Sensitive Data Logging Exclusion**
    - **Validates: Requirements 18.5**

  - [ ] 18.4 Write unit tests for logging
    - Test log entries contain required fields
    - Test sensitive data is filtered
    - Test error logging includes context
    - _Requirements: 18.1-18.7_


- [ ] 19. Configure AWS infrastructure with SAM
  - [ ] 19.1 Create SAM template for Lambda functions
    - Define all 7 Lambda functions (generateSection1, generateSection2, generateEmbedding, generateDNA, generatePath, findMatches, generateAnalytics)
    - Configure Python 3.11 runtime
    - Set memory and timeout configurations
    - Configure IAM roles with Bedrock and DynamoDB permissions
    - Add environment variables for table names and Bedrock region
    - _Requirements: 1.1-7.7_

  - [ ] 19.2 Configure API Gateway REST API
    - Define API Gateway REST API resource
    - Create routes for all endpoints (quiz and profile)
    - Attach Lambda authorizer to protected endpoints
    - Configure CORS headers
    - Set up rate limiting
    - _Requirements: 8.1, 8.2, 14.7, 17.9_

  - [ ] 19.3 Create DynamoDB table definitions
    - Define Users table with userId as partition key
    - Define Sessions table with sessionId as partition key and TTL attribute
    - Define EmbeddingCache table with docHash as partition key
    - Configure encryption at rest
    - _Requirements: 3.8, 10.1, 15.4, 16.1_

  - [ ] 19.4 Configure Lambda provisioned concurrency
    - Set provisioned concurrency for generateSection1 and generateEmbedding
    - Configure warm-up schedule (every 5 minutes)
    - _Requirements: 16.7_

  - [ ] 19.5 Write integration tests for infrastructure
    - Test Lambda function deployment
    - Test API Gateway endpoint accessibility
    - Test DynamoDB table creation
    - _Requirements: 1.1-7.7_

- [ ] 20. Create AI prompt templates
  - [ ] 20.1 Create adaptive quiz prompt template
    - Write prompt for Section 1 foundational questions
    - Write prompt for Section 2 adaptive questions with context injection
    - Store prompts in backend/prompts/ directory
    - _Requirements: 1.1, 2.3_

  - [ ] 20.2 Create DNA generation prompt template
    - Write prompt for taste archetype generation
    - Include instructions for trait scoring and category profiling
    - _Requirements: 4.1_

  - [ ] 20.3 Create growth path prompt template
    - Write prompt for Absorb/Create/Reflect recommendations
    - Include instructions for personalization based on DNA
    - _Requirements: 5.3_

  - [ ] 20.4 Create analytics prompt template
    - Write prompt for behavioral insights generation
    - Include instructions for passive/intentional ratio and goal alignment
    - _Requirements: 7.3_


- [ ] 21. Implement end-to-end integration tests
  - [ ] 21.1 Write integration test for complete onboarding flow
    - Test Section 1 generation → Section 2 generation → Quiz completion
    - Verify DNA profile and embedding are stored correctly
    - Verify session lifecycle and expiration
    - _Requirements: 1.1-4.6, 9.1-9.7_

  - [ ] 21.2 Write integration test for matching flow
    - Create test users with known embeddings
    - Calculate expected similarity scores
    - Call findMatches endpoint
    - Verify matches are sorted and filtered correctly
    - _Requirements: 6.1-6.9_

  - [ ] 21.3 Write integration test for growth path generation
    - Complete quiz for test user
    - Call generatePath endpoint
    - Verify path structure and personalization
    - _Requirements: 5.1-5.7_

  - [ ] 21.4 Write integration test for analytics generation
    - Complete quiz for test user
    - Call generateAnalytics endpoint
    - Verify analytics structure and insights
    - _Requirements: 7.1-7.7_

  - [ ] 21.5 Write integration test for error scenarios
    - Test session expiration handling
    - Test Claude API failure recovery
    - Test Titan API failure recovery
    - Test DynamoDB failure recovery
    - _Requirements: 13.1-13.8_

- [ ] 22. Implement property-based tests for correctness properties
  - [ ] 22.1 Write property test for session lifecycle integrity
    - **Property 1: Session Lifecycle Integrity**
    - **Validates: Requirements 1.2, 2.4, 2.5, 10.1, 10.4, 10.5**

  - [ ] 22.2 Write property test for embedding vector normalization
    - **Property 2: Embedding Vector Normalization**
    - **Validates: Requirements 3.7, 11.3, 12.8, 12.9**

  - [ ] 22.3 Write property test for cosine similarity bounds
    - **Property 3: Cosine Similarity Bounds**
    - **Validates: Requirements 11.5, 11.6, 11.7**

  - [ ] 22.4 Write property test for match similarity threshold
    - **Property 4: Match Similarity Threshold and Exclusion**
    - **Validates: Requirements 6.4, 6.5**

  - [ ] 22.5 Write property test for quiz answer completeness
    - **Property 5: Quiz Answer Completeness**
    - **Validates: Requirements 12.1, 12.2, 12.3**

  - [ ] 22.6 Write property test for embedding cache consistency
    - **Property 6: Embedding Cache Consistency**
    - **Validates: Requirements 3.2, 3.3, 16.1, 16.2**

  - [ ] 22.7 Write property test for privacy-first data storage
    - **Property 7: Privacy-First Data Storage**
    - **Validates: Requirements 3.9, 15.1, 15.2, 15.3**

  - [ ] 22.8 Write property test for question structure completeness
    - **Property 8: Question Structure Completeness**
    - **Validates: Requirements 1.4**

  - [ ] 22.9 Write property test for DNA profile structure
    - **Property 9: DNA Profile Structure Completeness**
    - **Validates: Requirements 4.2, 4.3, 4.4**

  - [ ] 22.10 Write property test for growth path structure
    - **Property 10: Growth Path Structure Completeness**
    - **Validates: Requirements 5.4, 5.5, 5.6**

  - [ ] 22.11 Write property test for match results ordering
    - **Property 11: Match Results Ordering**
    - **Validates: Requirements 6.7, 6.8, 6.9**

  - [ ] 22.12 Write property test for API authentication token inclusion
    - **Property 12: API Authentication Token Inclusion**
    - **Validates: Requirements 8.3**

  - [ ] 22.13 Write property test for session ID persistence
    - **Property 13: Session ID Persistence**
    - **Validates: Requirements 9.6**

  - [ ] 22.14 Write property test for input validation bounds
    - **Property 14: Input Validation Bounds**
    - **Validates: Requirements 12.4, 12.5, 12.6**

  - [ ] 22.15 Write property test for cache hit behavior
    - **Property 15: Cache Hit Behavior**
    - **Validates: Requirements 3.3, 16.3, 16.4**

  - [ ] 22.16 Write property test for sensitive data logging exclusion
    - **Property 16: Sensitive Data Logging Exclusion**
    - **Validates: Requirements 18.5**


- [ ] 23. Configure environment and deployment
  - [ ] 23.1 Set up environment variables
    - Configure VITE_VIBEGRAPH_API_URL for frontend
    - Configure AWS region and table names for Lambda functions
    - Configure Bedrock model IDs
    - _Requirements: 8.7_

  - [ ] 23.2 Set up secrets management
    - Store JWT_SECRET in AWS Secrets Manager
    - Configure Lambda functions to retrieve secrets
    - Set up secret rotation schedule (90 days)
    - _Requirements: 14.1_

  - [ ] 23.3 Configure DynamoDB encryption
    - Enable encryption at rest for all tables
    - Configure KMS keys for encryption
    - _Requirements: 15.4_

  - [ ] 23.4 Configure API Gateway TLS
    - Ensure TLS 1.3 is enabled
    - Configure custom domain with SSL certificate
    - _Requirements: 15.5_

  - [ ] 23.5 Write deployment validation tests
    - Test environment variables are set correctly
    - Test secrets are accessible
    - Test encryption is enabled
    - _Requirements: 8.7, 14.1, 15.4, 15.5_

- [ ] 24. Final checkpoint - End-to-end system validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All containers are self-contained with dependencies installed in Docker layers
- Session expiration (1-hour TTL) has been removed per requirements
- Frontend runs in separate container with nginx
- Backend is split into multiple containers: api, handlers, services
- DynamoDB Local used for development (no AWS required)
- LocalStack used to mock AWS Bedrock services
- Makefile provides convenient commands for all operations
- Documentation is modular and organized in docs/ directory
- Each component has its own README and detailed documentation
- Docker Compose orchestrates all containers with proper networking
- Hot reload enabled for development mode
- Production mode uses optimized builds
- Tasks are ordered sequentially to minimize conflicts
- Each task builds on previous tasks for smooth implementation
- Testing happens incrementally at checkpoints
