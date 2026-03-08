# VibeGraph Documentation

Welcome to the VibeGraph documentation. This guide provides comprehensive information about the VibeGraph adaptive quiz system, taste profiling, and personalized recommendations platform.

## Quick Links

- [Getting Started](#getting-started)
- [Development Guide](./DEVELOPMENT.md)
- [API Documentation](./api/README.md)
- [Frontend Documentation](./frontend/README.md)
- [Backend Documentation](./backend/README.md)
- [Infrastructure Documentation](./infrastructure/README.md)
- [Architecture Overview](./architecture/design.md)

## Overview

VibeGraph is a privacy-first adaptive quiz platform that generates AI-powered taste profiles, DNA archetypes, personalized growth paths, and taste-based matching. The system uses AWS Bedrock (Claude 3.5 Sonnet and Titan v2) for AI processing while maintaining strict privacy by storing only embeddings rather than raw quiz responses.

### Key Features

- **Adaptive Quiz System**: Multi-phase quiz with AI-generated questions that adapt to user responses
- **Taste DNA Profiles**: Personalized archetypes with trait scores and category preferences
- **Growth Paths**: Curated recommendations organized into Absorb, Create, and Reflect categories
- **Taste Matching**: Find like-minded users based on embedding similarity
- **Behavioral Analytics**: AI-powered insights about content consumption patterns
- **Privacy-First**: Raw quiz answers are never stored, only mathematical embeddings

## Architecture

VibeGraph uses a containerized microservices architecture:

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│  Backend API │────▶│  DynamoDB   │
│   (React)   │     │   (FastAPI)  │     │   Local     │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ AWS Bedrock  │
                    │ Claude+Titan │
                    └──────────────┘
```

### Technology Stack

**Frontend:**
- React 18 with Vite
- Tailwind CSS for styling
- Framer Motion for animations
- Redux Toolkit for state management

**Backend:**
- Python 3.11 with FastAPI
- AWS Bedrock for AI processing
- DynamoDB for data persistence
- Docker for containerization

**Infrastructure:**
- Docker Compose for orchestration
- DynamoDB Local for development
- LocalStack for AWS service mocking
- Makefile for build automation

## Getting Started

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 8 GB RAM minimum (16 GB recommended)
- 10 GB free disk space

### Quick Start

1. Clone the repository:
```bash
git clone https://github.com/your-org/vibegraph.git
cd vibegraph
```

2. Start all services:
```bash
make up
```

3. Wait for health checks to pass:
```bash
make wait-healthy
```

4. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

For detailed setup instructions, see the [Development Guide](./DEVELOPMENT.md).

## Documentation Structure

### Frontend Documentation
- [Frontend Overview](./frontend/README.md)
- [Component Documentation](./frontend/components/)
- [API Service Layer](./frontend/services/)
- [Design System](./frontend/DESIGN_SYSTEM.md)

### Backend Documentation
- [Backend Overview](./backend/README.md)
- [Handler Documentation](./backend/handlers/)
- [Service Layer](./backend/services/)
- [Utility Functions](./backend/utils/)
- [Architecture](./backend/ARCHITECTURE.md)
- [Data Flow](./backend/DATA_FLOW.md)
- [Embedding Strategy](./backend/EMBEDDING_STRATEGY.md)

### API Documentation
- [API Overview](./api/README.md)
- [Quiz Endpoints](./api/quiz-endpoints.md)
- [Profile Endpoints](./api/profile-endpoints.md)
- [Error Codes](./api/README.md#error-codes)

### Infrastructure Documentation
- [Infrastructure Overview](./infrastructure/README.md)
- [Docker Setup](./infrastructure/docker-setup.md)
- [Docker Compose](./infrastructure/docker-compose.md)
- [Makefile Commands](./infrastructure/makefile.md)
- [Networking](./infrastructure/networking.md)
- [Environment Configuration](./infrastructure/environment.md)
- [Logging](./infrastructure/logging.md)
- [Deployment](./infrastructure/DEPLOYMENT.md)

### Architecture Documentation
- [Design Document](./architecture/design.md)
- [Requirements](./architecture/requirements.md)

## Development Workflow

### Running Locally

```bash
# Start all containers
make up

# View logs
make logs

# Run tests
make test

# Stop containers
make down
```

### Making Changes

1. **Frontend changes**: Edit files in `frontend/src/` - hot reload is enabled
2. **Backend changes**: Edit files in `backend/` - auto-reload is enabled
3. **Run tests**: `make test` to verify changes
4. **Check health**: `make health` to verify all services are healthy

### Testing

```bash
# Run all tests
make test

# Run frontend tests only
make test-frontend

# Run backend tests only
make test-backend

# Run integration tests
make test-integration
```

## Key Concepts

### Adaptive Quiz Flow

1. **Section 1**: User answers 5 foundational questions about taste preferences
2. **Section 2**: AI generates 5 adaptive questions based on Section 1 responses
3. **Processing**: System generates embedding, DNA profile, and growth path
4. **Results**: User sees their Taste DNA archetype and recommendations

### Embedding System

- Quiz answers are converted to a 1024-dimensional vector using Titan v2
- Vectors are normalized to unit length for consistent comparison
- Embeddings are cached using SHA-256 hashing to reduce API costs
- Raw quiz answers are NEVER stored (privacy-first design)

### Taste Matching

- Users are matched based on cosine similarity of embedding vectors
- Similarity threshold: 0.7 (70% match)
- Matches include shared traits and archetype information
- Maximum 50 matches returned per request

### DNA Archetypes

AI-generated personality profiles that include:
- Archetype name (e.g., "The Explorer", "The Minimalist")
- Trait scores (0-10 scale)
- Category preferences with intensity values
- Descriptive summary

## API Overview

### Quiz Endpoints

- `POST /api/quiz/section1/start` - Start quiz and get Section 1 questions
- `POST /api/quiz/section2/generate` - Generate adaptive Section 2 questions
- `POST /api/quiz/complete` - Complete quiz and generate profile

### Profile Endpoints

- `GET /api/profile/dna/:userId` - Get user's Taste DNA profile
- `GET /api/profile/path/:userId` - Get personalized growth path
- `GET /api/profile/matches/:userId` - Find taste matches
- `GET /api/profile/analytics/:userId` - Get behavioral analytics

See [API Documentation](./api/README.md) for complete reference.

## Troubleshooting

### Common Issues

**Containers won't start:**
```bash
# Check logs
make logs

# Rebuild containers
make rebuild
```

**Health checks failing:**
```bash
# Check health status
make health

# Validate connections
make check-connections
```

**Port conflicts:**
```bash
# Check what's using the port
lsof -i :8000

# Kill the process or change ports in docker-compose.yml
```

For more troubleshooting tips, see the [Development Guide](./DEVELOPMENT.md#troubleshooting).

## Contributing

When contributing to VibeGraph:

1. Read the [Development Guide](./DEVELOPMENT.md)
2. Follow the coding standards in each component's documentation
3. Write tests for new features
4. Update documentation for any changes
5. Ensure all health checks pass before submitting

## Support

- **Documentation Issues**: Open an issue on GitHub
- **Bug Reports**: Use the bug report template
- **Feature Requests**: Use the feature request template
- **Questions**: Check existing documentation or ask in discussions

## License

[Your License Here]

## Additional Resources

- [Project Summary](./PROJECT_SUMMARY.md)
- [Folder Structure](./FOLDER_STRUCTURE.md)
- [Development Utilities](./dev-utils/)
