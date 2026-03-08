# API Documentation

## Overview

The VibeGraph API provides endpoints for adaptive quiz generation, taste profile creation, DNA archetype generation, growth path recommendations, taste matching, and behavioral analytics. All endpoints use RESTful conventions with JSON request/response bodies.

## Base URL

**Development**: `http://localhost:8000`

**Production**: `https://api.vibegraph.com`

## Authentication

Most endpoints require authentication using JWT tokens in the Authorization header:

```http
Authorization: Bearer <jwt_token>
```

### Obtaining a Token

```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "expiresIn": 3600
}
```

## Endpoint Categories

### Quiz Endpoints

Endpoints for adaptive quiz generation and completion:

- [POST /api/quiz/section1/start](#post-apiquizsection1start) - Start quiz and get Section 1 questions
- [POST /api/quiz/section2/generate](#post-apiquizsection2generate) - Generate adaptive Section 2 questions
- [POST /api/quiz/complete](#post-apiquizcomplete) - Complete quiz and generate profile

See [Quiz Endpoints Documentation](./quiz-endpoints.md) for detailed information.

### Profile Endpoints

Endpoints for retrieving user profiles and recommendations:

- [GET /api/profile/dna/:userId](#get-apiprofilednauserid) - Get user's Taste DNA profile
- [GET /api/profile/path/:userId](#get-apiprofilepathuserid) - Get personalized growth path
- [GET /api/profile/matches/:userId](#get-apiprofilematchesuserid) - Find taste matches
- [GET /api/profile/analytics/:userId](#get-apiprofileanalyticsuserid) - Get behavioral analytics

See [Profile Endpoints Documentation](./profile-endpoints.md) for detailed information.

### Health Endpoints

Endpoints for monitoring system health:

- [GET /health](#get-health) - Basic liveness check
- [GET /health/ready](#get-healthready) - Readiness check with dependencies
- [GET /health/db](#get-healthdb) - DynamoDB connection status
- [GET /health/bedrock](#get-healthbedrock) - Bedrock connection status
- [GET /health/status](#get-healthstatus) - Comprehensive status report

## Quick Reference

### Quiz Flow

```
1. POST /api/quiz/section1/start
   → Returns: sessionId, section1Questions

2. POST /api/quiz/section2/generate
   → Body: sessionId, section1Answers
   → Returns: section2Questions

3. POST /api/quiz/complete
   → Body: sessionId, allAnswers
   → Returns: embeddingId, tasteDNA
```

### Profile Retrieval

```
1. GET /api/profile/dna/:userId
   → Returns: tasteDNA profile

2. GET /api/profile/path/:userId
   → Returns: growth path recommendations

3. GET /api/profile/matches/:userId?limit=10
   → Returns: taste matches

4. GET /api/profile/analytics/:userId
   → Returns: behavioral analytics
```

## Common Response Formats

### Success Response

```json
{
  "data": { ... },
  "message": "Success",
  "timestamp": 1699564800
}
```

### Error Response

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "sessionId",
      "issue": "Must be a valid UUID"
    }
  },
  "timestamp": 1699564800
}
```

## Error Codes

### HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error occurred |
| 503 | Service Unavailable | Service temporarily unavailable |

### Application Error Codes

| Code | Description | Resolution |
|------|-------------|------------|
| `VALIDATION_ERROR` | Invalid input parameters | Check request format and values |
| `SESSION_EXPIRED` | Quiz session expired or not found | Start a new quiz session |
| `USER_NOT_FOUND` | User does not exist | Verify userId is correct |
| `PROFILE_NOT_FOUND` | User profile not generated | Complete quiz first |
| `AUTH_TOKEN_INVALID` | Invalid or expired JWT token | Re-authenticate |
| `AUTH_TOKEN_MISSING` | No authentication token provided | Include Authorization header |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Wait before retrying |
| `AI_SERVICE_ERROR` | Claude or Titan API failure | Retry request |
| `DATABASE_ERROR` | DynamoDB operation failed | Retry request |
| `CACHE_ERROR` | Cache service error | Request will proceed without cache |

## Rate Limiting

API requests are rate-limited to prevent abuse:

- **Authenticated users**: 100 requests per minute
- **Unauthenticated endpoints**: 20 requests per minute

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1699564860
```

When rate limit is exceeded:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please try again later.",
    "retryAfter": 60
  }
}
```

## CORS Configuration

### Allowed Origins

**Development**: `http://localhost:3000`, `http://localhost:5173`

**Production**: `https://vibegraph.com`, `https://www.vibegraph.com`

### Allowed Methods

`GET`, `POST`, `PUT`, `DELETE`, `OPTIONS`

### Allowed Headers

`Content-Type`, `Authorization`, `X-Requested-With`

### Exposed Headers

`X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Request/Response Examples

### Start Quiz

**Request**:
```http
POST /api/quiz/section1/start HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{}
```

**Response**:
```json
{
  "sessionId": "550e8400-e29b-41d4-a716-446655440000",
  "questions": [
    {
      "id": "q1",
      "title": "What type of content do you consume most?",
      "category": "content_preferences",
      "options": ["Articles", "Videos", "Podcasts", "Books"],
      "multiSelect": false
    }
  ],
  "expiresAt": 1699568400
}
```

### Get Taste DNA

**Request**:
```http
GET /api/profile/dna/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response**:
```json
{
  "tasteDNA": {
    "archetype": "The Explorer",
    "traits": [
      {
        "name": "Curiosity",
        "score": 9,
        "description": "High drive to discover new content"
      }
    ],
    "categories": [
      {
        "category": "Technology",
        "preferences": ["AI", "Web Development", "Cloud Computing"],
        "intensity": 8
      }
    ],
    "description": "You are an Explorer who thrives on discovering new ideas..."
  }
}
```

## Data Models

### Question

```typescript
interface Question {
  id: string                    // Unique question identifier
  title: string                 // Question text
  category: string              // Question category
  options: string[]             // Available answer options
  multiSelect: boolean          // Allow multiple selections
}
```

### Answer

```typescript
interface Answer {
  questionId: string            // Reference to question
  selectedOptions: string[]     // Selected answer options
}
```

### Taste DNA

```typescript
interface TasteDNA {
  archetype: string             // DNA archetype name
  traits: Trait[]               // Personality traits
  categories: CategoryProfile[] // Category preferences
  description: string           // Archetype description
}

interface Trait {
  name: string                  // Trait name
  score: number                 // Score 0-10
  description: string           // Trait description
}

interface CategoryProfile {
  category: string              // Category name
  preferences: string[]         // Specific preferences
  intensity: number             // Intensity 0-10
}
```

### Growth Path

```typescript
interface GrowthPath {
  absorb: PathItem[]            // Content to consume
  create: PathItem[]            // Content to create
  reflect: PathItem[]           // Reflection activities
  generatedAt: number           // Unix timestamp
}

interface PathItem {
  id: string                    // Unique item identifier
  title: string                 // Item title
  description: string           // Item description
  category: string              // Item category
  estimatedTime: string         // Time estimate
  difficulty: 'beginner' | 'intermediate' | 'advanced'
}
```

### Match

```typescript
interface Match {
  userId: string                // Matched user ID
  username: string              // Matched user name
  similarity: number            // Similarity score 0-1
  sharedTraits: string[]        // Common traits
  archetype: string             // User's archetype
}
```

### Analytics

```typescript
interface Analytics {
  passiveVsIntentionalRatio: number     // Ratio 0-1
  goalAlignment: number                 // Alignment score 0-10
  contentBalance: CategoryBalance[]     // Category distribution
  insights: Insight[]                   // Behavioral insights
  recommendations: string[]             // Recommendations
}

interface CategoryBalance {
  category: string              // Category name
  percentage: number            // Percentage 0-100
  trend: 'increasing' | 'stable' | 'decreasing'
}

interface Insight {
  type: 'strength' | 'opportunity' | 'pattern'
  title: string                 // Insight title
  description: string           // Insight description
}
```

## Pagination

Endpoints that return lists support pagination:

```http
GET /api/profile/matches/:userId?limit=10&offset=0
```

**Parameters**:
- `limit`: Number of items per page (default: 10, max: 50)
- `offset`: Number of items to skip (default: 0)

**Response**:
```json
{
  "data": [...],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 45,
    "hasMore": true
  }
}
```

## Webhooks

VibeGraph supports webhooks for real-time notifications:

### Supported Events

- `quiz.completed` - User completed quiz
- `profile.updated` - User profile updated
- `match.found` - New taste match found

### Webhook Payload

```json
{
  "event": "quiz.completed",
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": 1699564800,
  "data": { ... }
}
```

## SDK and Client Libraries

### JavaScript/TypeScript

```bash
npm install @vibegraph/client
```

```typescript
import { VibeGraphClient } from '@vibegraph/client'

const client = new VibeGraphClient({
  apiUrl: 'http://localhost:8000',
  token: 'your-jwt-token'
})

const response = await client.quiz.startSection1()
```

### Python

```bash
pip install vibegraph-client
```

```python
from vibegraph import VibeGraphClient

client = VibeGraphClient(
    api_url='http://localhost:8000',
    token='your-jwt-token'
)

response = client.quiz.start_section1()
```

## Testing

### Using cURL

```bash
# Start quiz
curl -X POST http://localhost:8000/api/quiz/section1/start \
  -H "Content-Type: application/json" \
  -d '{}'

# Get DNA profile
curl -X GET http://localhost:8000/api/profile/dna/USER_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Using Postman

Import the Postman collection: [Download Collection](./postman_collection.json)

### Using API Documentation UI

Visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## Changelog

### v1.0.0 (2024-01-15)

- Initial API release
- Quiz endpoints
- Profile endpoints
- Health check endpoints

## Support

- **API Issues**: Open an issue on GitHub
- **Documentation**: Check this documentation or ask in discussions
- **Rate Limit Increase**: Contact support@vibegraph.com

## Related Documentation

- [Quiz Endpoints](./quiz-endpoints.md)
- [Profile Endpoints](./profile-endpoints.md)
- [Frontend API Service](../frontend/services/vibegraph-api.md)
- [Backend Handlers](../backend/handlers/)
