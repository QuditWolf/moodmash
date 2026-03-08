# Profile Endpoints

## Overview

Profile endpoints provide access to user taste profiles, growth paths, taste matches, and behavioral analytics.

## Endpoints

### GET /api/profile/dna/:userId

Retrieve a user's Taste DNA profile.

**Authentication**: Required

**Request**:
```http
GET /api/profile/dna/550e8400-e29b-41d4-a716-446655440000 HTTP/1.1
Host: localhost:8000
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| userId | string (UUID) | User ID |

**Response** (200 OK):
```json
{
  "tasteDNA": {
    "archetype": "The Thoughtful Explorer",
    "traits": [
      {
        "name": "Intellectual Curiosity",
        "score": 9,
        "description": "Strong drive to understand complex ideas"
      }
    ],
    "categories": [
      {
        "category": "Technology",
        "preferences": ["AI", "Web Development"],
        "intensity": 9
      }
    ],
    "description": "You are a Thoughtful Explorer..."
  }
}
```

**Error Responses**:

**401 Unauthorized**:
```json
{
  "error": {
    "code": "AUTH_TOKEN_MISSING",
    "message": "Authentication required"
  }
}
```

**404 Not Found**:
```json
{
  "error": {
    "code": "PROFILE_NOT_FOUND",
    "message": "User profile not found. Complete quiz first."
  }
}
```

---

### GET /api/profile/path/:userId

Retrieve a user's personalized growth path.

**Authentication**: Required

**Response** (200 OK):
```json
{
  "path": {
    "absorb": [
      {
        "id": "abs_1",
        "title": "Deep Dive into AI Ethics",
        "description": "Explore ethical implications of AI",
        "category": "Technology",
        "estimatedTime": "2 hours",
        "difficulty": "intermediate"
      }
    ],
    "create": [
      {
        "id": "cre_1",
        "title": "Build a Personal AI Project",
        "description": "Create your own AI application",
        "category": "Technology",
        "estimatedTime": "10 hours",
        "difficulty": "advanced"
      }
    ],
    "reflect": [
      {
        "id": "ref_1",
        "title": "Journal Your Learning Journey",
        "description": "Reflect on your AI learning",
        "category": "Personal Growth",
        "estimatedTime": "30 minutes",
        "difficulty": "beginner"
      }
    ],
    "generatedAt": 1699564800
  }
}
```

---

### GET /api/profile/matches/:userId

Find taste matches for a user.

**Authentication**: Required

**Query Parameters**:
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | number | 10 | Max matches (max: 50) |

**Response** (200 OK):
```json
{
  "matches": [
    {
      "userId": "660e8400-e29b-41d4-a716-446655440001",
      "username": "alex_explorer",
      "similarity": 0.87,
      "sharedTraits": ["Intellectual Curiosity", "Analytical Thinking"],
      "archetype": "The Analytical Thinker"
    }
  ]
}
```

---

### GET /api/profile/analytics/:userId

Get behavioral analytics for a user.

**Authentication**: Required

**Response** (200 OK):
```json
{
  "analytics": {
    "passiveVsIntentionalRatio": 0.65,
    "goalAlignment": 8,
    "contentBalance": [
      {
        "category": "Technology",
        "percentage": 45,
        "trend": "increasing"
      }
    ],
    "insights": [
      {
        "type": "strength",
        "title": "Consistent Learning",
        "description": "You maintain regular engagement"
      }
    ],
    "recommendations": [
      "Explore more creative content",
      "Balance passive consumption with creation"
    ]
  }
}
```

## Related Documentation

- [Quiz Endpoints](./quiz-endpoints.md)
- [API Overview](./README.md)
