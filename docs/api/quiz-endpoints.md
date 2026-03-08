# Quiz Endpoints

## Overview

Quiz endpoints handle the adaptive quiz flow, including Section 1 generation, Section 2 adaptive questions, and quiz completion with profile generation.

## Endpoints

### POST /api/quiz/section1/start

Start a new quiz session and generate Section 1 foundational questions.

**Authentication**: Not required (anonymous quiz supported)

**Request**:
```http
POST /api/quiz/section1/start HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "userId": "550e8400-e29b-41d4-a716-446655440000"  // Optional
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| userId | string (UUID) | No | User ID for authenticated users |

**Response** (200 OK):
```json
{
  "sessionId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "questions": [
    {
      "id": "q1_foundation_1",
      "title": "What type of content do you consume most frequently?",
      "category": "content_preferences",
      "options": [
        "Long-form articles and essays",
        "Short videos and clips",
        "Podcasts and audio content",
        "Books and in-depth reading",
        "Visual content (photos, art, design)"
      ],
      "multiSelect": false
    },
    {
      "id": "q1_foundation_2",
      "title": "How do you prefer to discover new content?",
      "category": "discovery_style",
      "options": [
        "Algorithmic recommendations",
        "Curated collections",
        "Social recommendations from friends",
        "Expert recommendations",
        "Random exploration"
      ],
      "multiSelect": true
    }
  ],
  "expiresAt": 1699568400
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| sessionId | string (UUID) | Unique session identifier for this quiz |
| questions | Question[] | Array of 5 foundational questions |
| expiresAt | number | Unix timestamp when session expires (1 hour) |

**Question Object**:
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique question identifier |
| title | string | Question text |
| category | string | Question category (e.g., "content_preferences") |
| options | string[] | Available answer options |
| multiSelect | boolean | Whether multiple options can be selected |

**Error Responses**:

**500 Internal Server Error** - AI service failure:
```json
{
  "error": {
    "code": "AI_SERVICE_ERROR",
    "message": "Failed to generate quiz questions. Please try again.",
    "details": {
      "service": "claude",
      "retryable": true
    }
  }
}
```

**503 Service Unavailable** - Service temporarily unavailable:
```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "Service temporarily unavailable. Please try again later.",
    "retryAfter": 30
  }
}
```

**Example Usage**:

```bash
curl -X POST http://localhost:8000/api/quiz/section1/start \
  -H "Content-Type: application/json" \
  -d '{}'
```

```javascript
const response = await fetch('http://localhost:8000/api/quiz/section1/start', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({})
})

const data = await response.json()
console.log('Session ID:', data.sessionId)
console.log('Questions:', data.questions)
```

---

### POST /api/quiz/section2/generate

Generate adaptive Section 2 questions based on Section 1 answers.

**Authentication**: Not required

**Request**:
```http
POST /api/quiz/section2/generate HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "sessionId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "section1Answers": [
    {
      "questionId": "q1_foundation_1",
      "selectedOptions": ["Long-form articles and essays"]
    },
    {
      "questionId": "q1_foundation_2",
      "selectedOptions": ["Curated collections", "Expert recommendations"]
    }
  ]
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sessionId | string (UUID) | Yes | Session ID from Section 1 start |
| section1Answers | Answer[] | Yes | Array of exactly 5 answers |

**Answer Object**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| questionId | string | Yes | Question ID being answered |
| selectedOptions | string[] | Yes | Selected answer options (min 1) |

**Response** (200 OK):
```json
{
  "questions": [
    {
      "id": "q2_adaptive_1",
      "title": "Since you enjoy long-form content, which topics interest you most?",
      "category": "content_depth",
      "options": [
        "Technology and innovation",
        "Philosophy and ideas",
        "Science and research",
        "Arts and culture",
        "Business and economics"
      ],
      "multiSelect": true
    },
    {
      "id": "q2_adaptive_2",
      "title": "How do you engage with curated collections?",
      "category": "engagement_style",
      "options": [
        "I consume them immediately",
        "I save them for later",
        "I share them with others",
        "I use them as inspiration",
        "I critically analyze them"
      ],
      "multiSelect": false
    }
  ]
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| questions | Question[] | Array of 5 adaptive questions |

**Error Responses**:

**400 Bad Request** - Invalid request:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "section1Answers",
      "issue": "Must contain exactly 5 answers"
    }
  }
}
```

**404 Not Found** - Session not found or expired:
```json
{
  "error": {
    "code": "SESSION_EXPIRED",
    "message": "Session expired or not found",
    "details": {
      "sessionId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
      "action": "Start a new quiz session"
    }
  }
}
```

**500 Internal Server Error** - AI service failure:
```json
{
  "error": {
    "code": "AI_SERVICE_ERROR",
    "message": "Failed to generate adaptive questions. Please try again.",
    "details": {
      "service": "claude",
      "retryable": true
    }
  }
}
```

**Example Usage**:

```bash
curl -X POST http://localhost:8000/api/quiz/section2/generate \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "section1Answers": [
      {"questionId": "q1_foundation_1", "selectedOptions": ["Long-form articles and essays"]},
      {"questionId": "q1_foundation_2", "selectedOptions": ["Curated collections"]},
      {"questionId": "q1_foundation_3", "selectedOptions": ["Technology"]},
      {"questionId": "q1_foundation_4", "selectedOptions": ["Deep analysis"]},
      {"questionId": "q1_foundation_5", "selectedOptions": ["Morning"]}
    ]
  }'
```

```javascript
const response = await fetch('http://localhost:8000/api/quiz/section2/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    sessionId: sessionId,
    section1Answers: answers
  })
})

const data = await response.json()
console.log('Section 2 Questions:', data.questions)
```

---

### POST /api/quiz/complete

Complete the quiz and generate taste profile, embedding, and DNA archetype.

**Authentication**: Required (for authenticated users) or Optional (anonymous)

**Request**:
```http
POST /api/quiz/complete HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

{
  "sessionId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "userId": "550e8400-e29b-41d4-a716-446655440000",
  "allAnswers": {
    "section1": [
      {
        "questionId": "q1_foundation_1",
        "selectedOptions": ["Long-form articles and essays"]
      }
    ],
    "section2": [
      {
        "questionId": "q2_adaptive_1",
        "selectedOptions": ["Technology and innovation", "Philosophy and ideas"]
      }
    ]
  }
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| sessionId | string (UUID) | Yes | Session ID from quiz start |
| userId | string (UUID) | Yes | User ID (from auth token or provided) |
| allAnswers | QuizAnswers | Yes | All quiz answers |

**QuizAnswers Object**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| section1 | Answer[] | Yes | Section 1 answers (exactly 5) |
| section2 | Answer[] | Yes | Section 2 answers (exactly 5) |

**Response** (200 OK):
```json
{
  "embeddingId": "emb_7c9e6679-7425-40de-944b-e07fc1f90ae7",
  "tasteDNA": {
    "archetype": "The Thoughtful Explorer",
    "traits": [
      {
        "name": "Intellectual Curiosity",
        "score": 9,
        "description": "Strong drive to understand complex ideas and explore new concepts"
      },
      {
        "name": "Analytical Thinking",
        "score": 8,
        "description": "Preference for deep analysis and critical evaluation"
      },
      {
        "name": "Openness to Experience",
        "score": 9,
        "description": "High receptivity to new ideas and perspectives"
      }
    ],
    "categories": [
      {
        "category": "Technology",
        "preferences": ["AI and Machine Learning", "Web Development", "Cloud Computing"],
        "intensity": 9
      },
      {
        "category": "Philosophy",
        "preferences": ["Ethics", "Epistemology", "Philosophy of Mind"],
        "intensity": 7
      }
    ],
    "description": "You are a Thoughtful Explorer who thrives on intellectual discovery and deep understanding. You prefer long-form content that allows for nuanced exploration of complex topics, particularly in technology and philosophy. Your analytical nature drives you to critically evaluate ideas while remaining open to new perspectives."
  }
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| embeddingId | string | Unique identifier for the generated embedding |
| tasteDNA | TasteDNA | Complete taste DNA profile |

**TasteDNA Object**:
| Field | Type | Description |
|-------|------|-------------|
| archetype | string | DNA archetype name |
| traits | Trait[] | Personality traits (3-5 traits) |
| categories | CategoryProfile[] | Category preferences |
| description | string | Detailed archetype description |

**Trait Object**:
| Field | Type | Description |
|-------|------|-------------|
| name | string | Trait name |
| score | number | Score 0-10 |
| description | string | Trait description |

**CategoryProfile Object**:
| Field | Type | Description |
|-------|------|-------------|
| category | string | Category name |
| preferences | string[] | Specific preferences within category |
| intensity | number | Intensity score 0-10 |

**Error Responses**:

**400 Bad Request** - Invalid request:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid quiz answers",
    "details": {
      "field": "allAnswers.section1",
      "issue": "Must contain exactly 5 answers"
    }
  }
}
```

**404 Not Found** - Session not found:
```json
{
  "error": {
    "code": "SESSION_NOT_FOUND",
    "message": "Quiz session not found",
    "details": {
      "sessionId": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
    }
  }
}
```

**500 Internal Server Error** - Processing failure:
```json
{
  "error": {
    "code": "PROFILE_GENERATION_ERROR",
    "message": "Failed to generate taste profile. Please try again.",
    "details": {
      "stage": "embedding_generation",
      "retryable": true
    }
  }
}
```

**Example Usage**:

```bash
curl -X POST http://localhost:8000/api/quiz/complete \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "sessionId": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "allAnswers": {
      "section1": [...],
      "section2": [...]
    }
  }'
```

```javascript
const response = await fetch('http://localhost:8000/api/quiz/complete', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    sessionId: sessionId,
    userId: userId,
    allAnswers: {
      section1: section1Answers,
      section2: section2Answers
    }
  })
})

const data = await response.json()
console.log('Taste DNA:', data.tasteDNA)
console.log('Archetype:', data.tasteDNA.archetype)
```

---

## Quiz Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Quiz Flow                             │
└─────────────────────────────────────────────────────────┘

1. Start Quiz
   POST /api/quiz/section1/start
   ↓
   Returns: sessionId, section1Questions

2. Answer Section 1
   User selects answers
   ↓
   POST /api/quiz/section2/generate
   Body: sessionId, section1Answers
   ↓
   Returns: section2Questions (adaptive)

3. Answer Section 2
   User selects answers
   ↓
   POST /api/quiz/complete
   Body: sessionId, userId, allAnswers
   ↓
   Processing:
   - Generate 1024-dim embedding (Titan v2)
   - Generate DNA archetype (Claude)
   - Store profile in database
   ↓
   Returns: embeddingId, tasteDNA

4. View Results
   Display TasteDNA to user
```

## Privacy Considerations

**Important**: Raw quiz answers are NEVER stored in the database. Only the following are persisted:

- 1024-dimensional embedding vector (mathematically irreversible)
- Generated DNA archetype and traits
- Session data (temporary, expires after 1 hour)

This ensures user privacy while enabling taste matching and recommendations.

## Rate Limiting

Quiz endpoints have specific rate limits:

- **Section 1 Start**: 10 requests per minute per IP
- **Section 2 Generate**: 10 requests per minute per session
- **Quiz Complete**: 5 requests per minute per user

## Caching

The embedding generation process uses intelligent caching:

- Embedding documents are hashed using SHA-256
- Cache hit rate target: 40%
- Cache reduces Titan API calls and improves response time
- Cache entries include hit count and last accessed timestamp

## Testing

### Test Data

Use these test session IDs for development:

- `test-session-001` - Valid session with Section 1 complete
- `test-session-002` - Valid session with Section 2 complete
- `test-session-expired` - Expired session (returns 404)

### Mock Responses

In development mode, the API can return mock responses:

```bash
# Enable mock mode
export MOCK_MODE=true

# Start quiz with mock data
curl -X POST http://localhost:8000/api/quiz/section1/start?mock=true
```

## Related Documentation

- [Profile Endpoints](./profile-endpoints.md)
- [API Overview](./README.md)
- [Frontend Quiz Integration](../frontend/components/onboarding-page.md)
- [Backend Quiz Handlers](../backend/handlers/)
