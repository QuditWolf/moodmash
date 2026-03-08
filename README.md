# VibeGraph - Social Taste & Culture Platform

A modern, AI-powered platform for discovering and connecting through cultural taste. Built with React, FastAPI, and AWS Bedrock, featuring adaptive quizzes, taste DNA profiles, and intelligent matching.

## 🚀 Quick Links

- **[Quick Start Guide](QUICKSTART.md)** - Get running in 5 minutes
- **[Development Setup](SETUP.md)** - Complete setup instructions
- **[API Documentation](docs/api/)** - API endpoints and contracts
- **[Architecture](docs/architecture/)** - System design and requirements
- **[Deployment Guide](docs/deployment/AWS_MIGRATION.md)** - Production deployment

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Documentation](#documentation)
- [Contributing](#contributing)

---

## Overview

VibeGraph is a social platform that helps users discover their cultural taste profile and connect with like-minded individuals through:

- **Adaptive Quiz System**: AI-powered questions that adapt based on your answers
- **Taste DNA**: Unique cultural archetype and trait analysis
- **Smart Matching**: Find users with similar taste profiles (>70% similarity)
- **Growth Paths**: Personalized recommendations for cultural exploration
- **Privacy-First**: Never stores raw quiz answers, only embeddings

### System Architecture

```
┌─────────────────┐
│   Frontend      │  React + Vite + Tailwind
│   Port 3000     │  Premium dark UI
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   Backend API   │  FastAPI + Python 3.11
│   Port 8000     │  Health checks, routing
└────────┬────────┘
         │
         ├─────────────┬──────────────┐
         │             │              │
         ▼             ▼              ▼
┌─────────────┐  ┌──────────┐  ┌──────────┐
│  DynamoDB   │  │ Bedrock  │  │ Handlers │
│   Tables    │  │ Claude   │  │ Services │
│  Port 8001  │  │ Titan    │  │          │
└─────────────┘  └──────────┘  └──────────┘
```

---

## Features

### Core Functionality
- ✅ **Adaptive Quiz System**: Two-phase quiz with AI-generated questions
- ✅ **Taste DNA Generation**: Cultural archetype and trait analysis
- ✅ **Smart Matching**: Find users with >70% taste similarity
- ✅ **Growth Paths**: Personalized Absorb/Create/Reflect recommendations
- ✅ **Behavioral Analytics**: Insights into cultural engagement patterns

### Technical Features
- ✅ **Docker Containerization**: Full local development environment
- ✅ **Health Monitoring**: Comprehensive health checks and startup validation
- ✅ **API Gateway**: FastAPI with automatic OpenAPI documentation
- ✅ **Vector Embeddings**: 1024-dimensional taste vectors with Titan v2
- ✅ **Caching System**: SHA-256 based embedding cache for performance
- ✅ **Privacy-First**: Never stores raw quiz answers

---

## Tech Stack

### Frontend
- **React 18** - Component framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Icon library

### Backend
- **FastAPI** - Modern Python web framework
- **Python 3.11** - Runtime
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **DynamoDB Local** - Local database for development
- **LocalStack** - Mock AWS services

### AWS Services (Production)
- **AWS Bedrock** - AI/ML services
  - Claude 3.5 Sonnet - Question generation, DNA analysis
  - Titan v2 - 1024-dim embedding generation
- **DynamoDB** - NoSQL database
- **Lambda** - Serverless compute
- **API Gateway** - REST API management

---

## Project Structure

```
vibegraph-app/
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API services
│   │   └── styles/            # Global styles
│   ├── Dockerfile
│   └── package.json
│
├── backend/                    # Python backend
│   ├── api/                   # FastAPI gateway
│   │   ├── routes/            # API routes
│   │   │   ├── quiz.py        # Quiz endpoints
│   │   │   └── profile.py     # Profile endpoints
│   │   ├── main.py            # FastAPI app
│   │   ├── startup.py         # Startup checks
│   │   └── health.py          # Health endpoints
│   ├── handlers/              # Lambda handlers
│   ├── services/              # Shared services
│   ├── src/                   # Shared source code
│   │   ├── handlers/          # Handler implementations
│   │   ├── services/          # Service clients
│   │   └── utils/             # Utility functions
│   ├── scripts/               # Backend scripts
│   └── tests/                 # Test suite
│
├── docs/                       # Documentation
│   ├── reapplication/         # Merge guides
│   ├── integration/           # Integration docs
│   ├── deployment/            # Deployment guides
│   ├── architecture/          # System design
│   ├── api/                   # API documentation
│   ├── backend/               # Backend docs
│   ├── frontend/              # Frontend docs
│   ├── infrastructure/        # Docker, deployment
│   ├── tasks/                 # Task summaries
│   └── testing/               # Testing guides
│
├── scripts/                    # Automation scripts
│   ├── reapply-session-changes.sh
│   ├── test-integration.sh
│   └── ...
│
├── docker-compose.yml          # Container orchestration
├── docker-compose.override.yml # Development overrides
├── Makefile                    # Container management
├── README.md                   # This file
├── SETUP.md                    # Development setup
├── QUICKSTART.md               # Quick start guide
└── RESTRUCTURE-DEV.md          # Restructuring docs
```

---

## Getting Started

### Prerequisites

- **Docker** 20.10+ and **Docker Compose** 2.0+
- **Node.js** 20+ (for local frontend development)
- **Python** 3.11+ (for local backend development)
- **Make** (optional, for convenience commands)

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-org/vibegraph-app.git
cd vibegraph-app

# 2. Build all containers
make build

# 3. Start all services
make up

# 4. Wait for health checks
make wait-healthy

# 5. Access the application
open http://localhost:3000
```

That's it! The application is now running with:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

For detailed setup instructions, see [SETUP.md](SETUP.md).

---

## Development

### Container Management

```bash
# Build all images
make build

# Start all containers
make up

# Stop all containers
make down

# View logs
make logs

# Check container health
docker ps

# Restart specific service
docker-compose restart backend-api
```

### Running Tests

```bash
# Run all tests
bash scripts/test-integration.sh

# Test specific endpoint
curl -X POST http://localhost:8000/quiz/section1/start \
  -H "Content-Type: application/json" \
  -d '{}'

# Check health
curl http://localhost:8000/health
```

### Local Development

**Frontend:**
```bash
cd frontend
npm install
npm run dev  # Runs on port 5173
```

**Backend:**
```bash
cd backend/api
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Code Structure

**Adding New API Endpoints:**
1. Create route in `backend/api/routes/`
2. Register in `backend/api/main.py`
3. Add tests in `backend/tests/`
4. Document in `docs/api/`

**Adding New Components:**
1. Create component in `frontend/src/components/`
2. Add styles following design system
3. Document in `docs/frontend/components/`

---

## Testing

### Integration Tests

```bash
# Run comprehensive integration tests
bash scripts/test-integration.sh

# Expected output:
# ✅ 18+ tests passed
# ✅ All containers healthy
# ✅ All API endpoints working
# ✅ Frontend-backend integration verified
```

### Manual Testing

**Quiz Flow:**
```bash
# 1. Start Section 1
curl -X POST http://localhost:8000/quiz/section1/start \
  -H "Content-Type: application/json" -d '{}'

# 2. Generate Section 2
curl -X POST http://localhost:8000/quiz/section2/generate \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "...", "section1Answers": []}'

# 3. Complete Quiz
curl -X POST http://localhost:8000/quiz/complete \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "...", "userId": "test", "allAnswers": {}}'
```

**Profile Endpoints:**
```bash
curl http://localhost:8000/profile/dna/test-user
curl http://localhost:8000/profile/path/test-user
curl http://localhost:8000/profile/matches/test-user
curl http://localhost:8000/profile/analytics/test-user
```

---

## Deployment

### Local Development
- Uses Docker Compose with DynamoDB Local and LocalStack
- No AWS credentials required
- Full feature parity with production

### Production (AWS)
See [AWS_MIGRATION.md](docs/deployment/AWS_MIGRATION.md) for complete deployment guide.

**Key Steps:**
1. Set up AWS account and credentials
2. Deploy DynamoDB tables
3. Deploy Lambda functions
4. Configure API Gateway
5. Enable Bedrock services
6. Deploy frontend to S3 + CloudFront

**AWS Services Used:**
- Lambda (serverless compute)
- API Gateway (REST API)
- DynamoDB (database)
- Bedrock (AI/ML)
- S3 + CloudFront (frontend hosting)

---

## Documentation

### Essential Docs
- **[SETUP.md](SETUP.md)** - Complete development setup
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[RESTRUCTURE-DEV.md](RESTRUCTURE-DEV.md)** - Project restructuring details

### API Documentation
- **[API Overview](docs/api/README.md)** - API architecture
- **[Quiz Endpoints](docs/api/quiz-endpoints.md)** - Quiz API reference
- **[Profile Endpoints](docs/api/profile-endpoints.md)** - Profile API reference

### Architecture
- **[Design](docs/architecture/design.md)** - System design
- **[Requirements](docs/architecture/requirements.md)** - Functional requirements

### Integration
- **[API Integration](docs/integration/API_INTEGRATION_COMPLETE.md)** - API integration details
- **[Docker Integration](docs/integration/DOCKER_INTEGRATION_COMPLETE.md)** - Docker setup

### Deployment
- **[AWS Migration](docs/deployment/AWS_MIGRATION.md)** - Production deployment guide

### Reapplication (After Merge)
- **[Reapplication Guide](docs/reapplication/README_REAPPLICATION.md)** - Merge and reapply changes
- **[Changes to Reapply](docs/reapplication/CHANGES_TO_REAPPLY.md)** - Complete change list

### Frontend
- **[Components](docs/frontend/components/)** - Component documentation
- **[Design System](docs/frontend/PREMIUM_DESIGN_SYSTEM.md)** - UI design system

### Backend
- **[Handlers](docs/backend/handlers/)** - Lambda handler docs
- **[Services](docs/backend/services/)** - Service client docs
- **[Utils](docs/backend/utils/)** - Utility function docs

### Infrastructure
- **[Docker Setup](docs/infrastructure/docker-setup.md)** - Docker configuration
- **[Networking](docs/infrastructure/networking.md)** - Container networking

---

## Building New Features

### Adding New Card Types

1. Define category color in `categoryColors` object
2. Add to `categories` array in feed generator
3. Provide image collection and titles
4. Maintain 4:5 aspect ratio for images

### Creating New Pages

**Follow this structure:**
```jsx
const NewPage = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-white/10">
        {/* Header content */}
      </header>

      {/* Content */}
      <div className="py-6 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Page content */}
        </div>
      </div>
    </div>
  );
};
```

### Adding Interactions

**Hover states:**
```jsx
className="transition-all duration-180 ease-out hover:bg-surface/80"
```

**Image hover:**
```jsx
className="group"  // Parent
className="group-hover:scale-[1.02]"  // Image
```

**Link hover:**
```jsx
className="hover:text-foreground transition-colors duration-160"
```

---

## Design Principles for New UI

### Do's ✓

- Use pure black `#000000` background
- Apply subtle borders `border-white/10`
- Use monospace typography (IBM Plex Mono)
- Keep transitions between 160-200ms
- Use `cubic-bezier(0.16, 1, 0.3, 1)` easing
- Maintain high information density
- Apply subtle hover states (2% lighter, 2px lift)
- Use muted accent colors (50% saturation max)
- Keep rounded corners subtle (`rounded-lg` max)
- Align to 12-column grid system

### Don'ts ✗

- No heavy shadows or elevation
- No gradients (except subtle surface variations)
- No glow effects
- No neon colors
- No bold/heavy font weights (500 max)
- No large gaps (6 = 24px max)
- No floating card feeling
- No dramatic animations
- No border radius on grid layouts
- No approximations (use exact spacing scale)

---

## Accessibility

### Color Contrast
- Text on black: `hsl(0 0% 98%)` meets WCAG AA
- Muted text: `hsl(0 0% 55%)` for secondary content
- Borders: `white/10` visible but subtle

### Interactive Elements
- All clickable elements have hover states
- Focus states inherit from Tailwind defaults
- Sufficient touch targets (44px minimum)

### Images
- All images have `alt` attributes
- Lazy loading for performance
- Fallback backgrounds for missing images

---

## Performance Optimization

### Image Loading
```jsx
loading="lazy"  // Native lazy loading
```

### Transitions
- Use `transform` and `opacity` (GPU accelerated)
- Avoid animating `width`, `height`, `margin`

### Grid Rendering
- Fixed column counts reduce layout shifts
- Gap-based spacing (no margin calculations)

---

## Future Enhancements

### Potential Features
- Infinite scroll / pagination
- Filter by category
- Search functionality
- User preferences (saved items)
- Dark/light mode toggle (currently dark only)
- Keyboard navigation
- Grid/list view toggle

### Maintaining Design Consistency
When adding features, always:
1. Reference this README for design tokens
2. Use existing component patterns
3. Match interaction timing (180ms standard)
4. Test responsive behavior at all breakpoints
5. Maintain monospace typography
6. Keep true black background
7. Use subtle, premium interactions

---

## Quick Reference

### Common Patterns

**Card Grid:**
```jsx
<div className="grid grid-cols-12 gap-6">
  <div className="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3">
    <Card />
  </div>
</div>
```

**Premium Button:**
```jsx
<button className="hover:bg-surface/50 transition-all duration-160">
  Click me
</button>
```

**Category Badge:**
```jsx
<div className="px-2.5 py-1 rounded text-11 uppercase tracking-wide"
     style={{ backgroundColor: '...', color: '...', border: '...' }}>
  Category
</div>
```

**Page Container:**
```jsx
<div className="py-6 px-6">
  <div className="max-w-7xl mx-auto">
    {/* Content */}
  </div>
</div>
```

---

## Support

For questions about design decisions or implementation details, refer to:
- `DESIGN_SYSTEM.md` - Complete design token reference
- `PREMIUM_DESIGN_SYSTEM.md` - Premium interaction patterns
- `STRUCTURAL_SYSTEM.md` - Grid and layout system
- `COMPONENTS.md` - Component API documentation

---

**Built with precision. Designed for developers.**


## Contributing

### Development Workflow

1. **Fork and clone** the repository
2. **Create a branch** for your feature
3. **Make changes** following code style
4. **Test thoroughly** with integration tests
5. **Update documentation** as needed
6. **Submit pull request** with clear description

### Code Style

**Python (Backend):**
- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small

**JavaScript (Frontend):**
- Use functional components
- Follow React best practices
- Use Tailwind for styling
- Keep components focused

### Testing Requirements

- All new features must have tests
- Integration tests for API endpoints
- Component tests for UI changes
- Maintain >80% code coverage

### Documentation

- Update relevant docs in `docs/`
- Add API documentation for new endpoints
- Update README if adding major features
- Include code examples

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/vibegraph-app/issues)
- **Documentation**: [docs/](docs/)
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md)
- **Setup Guide**: [SETUP.md](SETUP.md)

---

## Acknowledgments

Built with:
- React, Vite, Tailwind CSS
- FastAPI, Python
- AWS Bedrock (Claude, Titan)
- Docker, Docker Compose

---

**VibeGraph** - Discover your cultural taste, connect with your tribe.
