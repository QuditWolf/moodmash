# VibeGraph API Service

## Overview

The VibeGraph API service (`frontend/src/services/vibeGraphAPI.js`) provides a centralized interface for all communication with the VibeGraph serverless backend. It handles adaptive quiz generation, taste profile creation, growth path recommendations, taste matching, and behavioral analytics.

## Architecture

The service is organized into two main API groups:

- **Quiz API**: Handles the adaptive quiz flow (Section 1, Section 2, completion)
- **Profile API**: Handles user profile operations (DNA, growth path, matches, analytics)

All API calls use the `apiRequest()` helper function which:
- Constructs full URLs using the configured API base URL
- Automatically includes authentication tokens from localStorage
- Sets appropriate headers (Content-Type: application/json)
- Handles errors and parses JSON responses

## Configuration

### Environment Variables

The service requires the following environment variable:

```bash
VITE_VIBEGRAPH_API_URL=https://api.vibegraph.example.com
```

If not set, it defaults to `http://localhost:3000` for local development.

### Authentication

The service automatically includes JWT authentication tokens in all requests:

```javascript
const token = localStorage.getItem('authToken');
if (token) {
  config.headers['Authorization'] = `Bearer ${token}`;
}
```

## API Reference

### Quiz API

#### `startSection1(userId)`

Starts the adaptive quiz and generates Section 1 foundational questions.

**Parameters:**
- `userId` (string, optional): User ID for authenticated users

**Returns:**
```javascript
{
  sessionId: string,        // Unique session identifier (UUID)
  questions: [              // Array of 5 foundational questions
    {
      id: string,
      title: string,
      category: string,
      options: string[],
      multiSelect: boolean
    }
  ],
  expiresAt: number        // Unix timestamp (session expires in 1 hour)
}
```

**Example:**
```javascript
import { vibeGraphAPI } from '../services/vibeGraphAPI';

const response = await vibeGraphAPI.quiz.startSection1();
console.log(response.sessionId);  // "550e8400-e29b-41d4-a716-446655440000"
console.log(response.questions.length);  // 5
```

**Error Handling:**
- `500`: AI service temporarily unavailable
- `503`: Service temporarily unavailable

---

#### `generateSection2(sessionId, section1Answers)`

Generates adaptive Section 2 questions based on Section 1 answers.

**Parameters:**
- `sessionId` (string, required): Session ID from Section 1
- `section1Answers` (array, required): Array of answer objects

**Answer Format:**
```javascript
{
  questionId: string,
  selectedOptions: string[]  // At least one option required
}
```

**Returns:**
```javascript
{
  questions: [              // Array of 5 adaptive questions
    {
      id: string,
      title: string,
      category: string,
      options: string[],
      multiSelect: boolean
    }
  ]
}
```

**Example:**
```javascript
const section1Answers = [
  { questionId: 'q1', selectedOptions: ['Option A', 'Option B'] },
  { questionId: 'q2', selectedOptions: ['Option C'] },
  // ... 3 more answers
];

const response = await vibeGraphAPI.quiz.generateSection2(
  sessionId,
  section1Answers
);
```

**Error Handling:**
- `400`: Invalid sessionId or answers
- `404`: Session not found or expired
- `500`: AI service temporarily unavailable

---

#### `completeQuiz(sessionId, userId, allAnswers)`

Completes the quiz and generates the user's taste profile (embedding + DNA).

**Parameters:**
- `sessionId` (string, required): Session ID
- `userId` (string, required): User ID
- `allAnswers` (object, required): Complete quiz answers

**Answer Format:**
```javascript
{
  section1: [
    { questionId: string, selectedOptions: string[] }
  ],
  section2: [
    { questionId: string, selectedOptions: string[] }
  ]
}
```

**Returns:**
```javascript
{
  embeddingId: string,      // Unique embedding identifier
  tasteDNA: {
    archetype: string,      // e.g., "The Minimalist", "The Explorer"
    traits: [
      {
        name: string,
        score: number,      // 0-10 scale
        description: string
      }
    ],
    categories: [
      {
        category: string,
        preferences: string[],
        intensity: number
      }
    ],
    description: string
  }
}
```

**Example:**
```javascript
const allAnswers = {
  section1: section1Answers,
  section2: section2Answers
};

const response = await vibeGraphAPI.quiz.completeQuiz(
  sessionId,
  userId,
  allAnswers
);

console.log(response.tasteDNA.archetype);  // "The Minimalist"
```

**Error Handling:**
- `400`: Invalid sessionId, userId, or answers
- `404`: Session not found
- `500`: Embedding or DNA generation failed

---

### Profile API

#### `getTasteDNA(userId)`

Retrieves the user's taste DNA profile.

**Parameters:**
- `userId` (string, required): User ID

**Returns:**
```javascript
{
  tasteDNA: {
    archetype: string,
    traits: [
      {
        name: string,
        score: number,
        description: string
      }
    ],
    categories: [
      {
        category: string,
        preferences: string[],
        intensity: number
      }
    ],
    description: string
  }
}
```

**Example:**
```javascript
const response = await vibeGraphAPI.profile.getTasteDNA(userId);
console.log(response.tasteDNA.archetype);
```

**Error Handling:**
- `401`: Unauthorized
- `404`: User not found or DNA not generated

---

#### `getGrowthPath(userId)`

Retrieves the user's personalized growth path with Absorb/Create/Reflect recommendations.

**Parameters:**
- `userId` (string, required): User ID

**Returns:**
```javascript
{
  path: {
    absorb: [              // 3-5 recommendations
      {
        id: string,
        title: string,
        description: string,
        category: string,
        estimatedTime: string,
        difficulty: 'beginner' | 'intermediate' | 'advanced'
      }
    ],
    create: [...],         // 3-5 recommendations
    reflect: [...],        // 3-5 recommendations
    generatedAt: number    // Unix timestamp
  }
}
```

**Example:**
```javascript
const response = await vibeGraphAPI.profile.getGrowthPath(userId);
console.log(response.path.absorb.length);  // 3-5
```

**Error Handling:**
- `401`: Unauthorized
- `404`: User not found or path not generated

---

#### `getMatches(userId, limit)`

Finds taste matches using cosine similarity on embedding vectors.

**Parameters:**
- `userId` (string, required): User ID
- `limit` (number, optional): Maximum matches to return (default: 10, max: 50)

**Returns:**
```javascript
{
  matches: [
    {
      userId: string,
      username: string,
      similarity: number,      // 0.7 to 1.0
      sharedTraits: string[],
      archetype: string
    }
  ]
}
```

**Example:**
```javascript
const response = await vibeGraphAPI.profile.getMatches(userId, 20);
console.log(response.matches[0].similarity);  // 0.87
```

**Error Handling:**
- `401`: Unauthorized
- `404`: User not found or embedding not generated

---

#### `getAnalytics(userId)`

Retrieves behavioral analytics and insights for the user.

**Parameters:**
- `userId` (string, required): User ID

**Returns:**
```javascript
{
  analytics: {
    passiveVsIntentionalRatio: number,
    goalAlignment: number,
    contentBalance: [
      {
        category: string,
        percentage: number,
        trend: 'increasing' | 'stable' | 'decreasing'
      }
    ],
    insights: [
      {
        type: 'strength' | 'opportunity' | 'pattern',
        title: string,
        description: string
      }
    ],
    recommendations: string[]
  }
}
```

**Example:**
```javascript
const response = await vibeGraphAPI.profile.getAnalytics(userId);
console.log(response.analytics.goalAlignment);  // 0.85
```

**Error Handling:**
- `401`: Unauthorized
- `404`: User not found or analytics not generated

---

## Usage Patterns

### Complete Onboarding Flow

```javascript
import { vibeGraphAPI } from '../services/vibeGraphAPI';

// 1. Start Section 1
const { sessionId, questions: section1Questions } = 
  await vibeGraphAPI.quiz.startSection1();

// 2. User answers Section 1
const section1Answers = [
  { questionId: section1Questions[0].id, selectedOptions: ['Option A'] },
  // ... collect all 5 answers
];

// 3. Generate Section 2
const { questions: section2Questions } = 
  await vibeGraphAPI.quiz.generateSection2(sessionId, section1Answers);

// 4. User answers Section 2
const section2Answers = [
  { questionId: section2Questions[0].id, selectedOptions: ['Option B'] },
  // ... collect all 5 answers
];

// 5. Complete quiz
const { tasteDNA } = await vibeGraphAPI.quiz.completeQuiz(
  sessionId,
  userId,
  { section1: section1Answers, section2: section2Answers }
);

console.log('Quiz complete! Archetype:', tasteDNA.archetype);
```

### Error Handling Pattern

```javascript
try {
  const response = await vibeGraphAPI.quiz.startSection1();
  setQuestions(response.questions);
  setSessionId(response.sessionId);
} catch (error) {
  if (error.message.includes('expired')) {
    // Redirect to start
    navigate('/onboarding');
  } else if (error.message.includes('temporarily unavailable')) {
    // Show retry button
    setError('Service temporarily unavailable. Please try again.');
  } else {
    // Generic error
    setError('Something went wrong. Please try again.');
  }
}
```

### Loading States

```javascript
const [loading, setLoading] = useState(false);

const handleStartQuiz = async () => {
  setLoading(true);
  try {
    const response = await vibeGraphAPI.quiz.startSection1();
    // Handle success
  } catch (error) {
    // Handle error
  } finally {
    setLoading(false);
  }
};
```

## Privacy and Security

### Data Privacy

The VibeGraph backend implements a **privacy-first architecture**:

- **Raw quiz answers are NEVER stored** in the database
- Only 1024-dimensional embedding vectors are persisted
- Embeddings are semantically meaningful but not reversible
- Users can request full data deletion at any time

### Authentication

All API endpoints require JWT authentication:

```javascript
// Token is automatically included from localStorage
localStorage.setItem('authToken', 'your-jwt-token');

// All subsequent API calls will include:
// Authorization: Bearer your-jwt-token
```

### Session Management

Quiz sessions expire after 1 hour:

- Sessions are created with `expiresAt` timestamp
- Expired sessions return 404 error
- Users must restart the quiz if session expires

## Testing

### Unit Tests

```javascript
import { vibeGraphAPI } from './vibeGraphAPI';

describe('vibeGraphAPI.quiz', () => {
  it('should start Section 1 and return questions', async () => {
    const response = await vibeGraphAPI.quiz.startSection1();
    
    expect(response.sessionId).toBeDefined();
    expect(response.questions).toHaveLength(5);
    expect(response.expiresAt).toBeGreaterThan(Date.now());
  });
  
  it('should handle session expiration', async () => {
    await expect(
      vibeGraphAPI.quiz.generateSection2('invalid-session', [])
    ).rejects.toThrow('Session expired or not found');
  });
});
```

### Integration Tests

```javascript
describe('Complete Quiz Flow', () => {
  it('should complete full onboarding flow', async () => {
    // Start Section 1
    const { sessionId, questions: q1 } = 
      await vibeGraphAPI.quiz.startSection1();
    
    // Generate Section 2
    const section1Answers = q1.map(q => ({
      questionId: q.id,
      selectedOptions: [q.options[0]]
    }));
    
    const { questions: q2 } = 
      await vibeGraphAPI.quiz.generateSection2(sessionId, section1Answers);
    
    // Complete quiz
    const section2Answers = q2.map(q => ({
      questionId: q.id,
      selectedOptions: [q.options[0]]
    }));
    
    const { tasteDNA } = await vibeGraphAPI.quiz.completeQuiz(
      sessionId,
      'test-user-id',
      { section1: section1Answers, section2: section2Answers }
    );
    
    expect(tasteDNA.archetype).toBeDefined();
    expect(tasteDNA.traits.length).toBeGreaterThan(0);
  });
});
```

## Performance Considerations

### Caching Strategy

The backend implements embedding caching to minimize API costs:

- Embedding documents are hashed using SHA-256
- Cache hit rate target: 40%
- Cache hits return in ~50ms vs ~500-800ms for Titan calls

### Response Times

Expected response times:

- `startSection1`: 2-4 seconds (Claude generation)
- `generateSection2`: 2-4 seconds (Claude generation)
- `completeQuiz`: 3-6 seconds (Titan embedding + Claude DNA)
- `getTasteDNA`: 10-20ms (DynamoDB lookup)
- `getGrowthPath`: 2-4 seconds (Claude generation)
- `getMatches`: 200-300ms (similarity calculation)
- `getAnalytics`: 2-4 seconds (Claude generation)

### Optimization Tips

1. **Show loading states** during AI generation (2-4 seconds)
2. **Cache profile data** in frontend state to avoid repeated calls
3. **Implement retry logic** with exponential backoff for failures
4. **Use progressive loading** for long operations (show partial results)

## Troubleshooting

### Common Issues

**Issue: "Session expired or not found"**
- Cause: Quiz session expired (1 hour TTL)
- Solution: Restart quiz from Section 1

**Issue: "AI service temporarily unavailable"**
- Cause: Claude/Titan API failure or timeout
- Solution: Retry request (backend implements automatic retries)

**Issue: "Unauthorized"**
- Cause: Missing or invalid JWT token
- Solution: Re-authenticate user and refresh token

**Issue: CORS errors**
- Cause: API Gateway CORS configuration
- Solution: Verify `VITE_VIBEGRAPH_API_URL` is correct

## Related Documentation

- [Backend Architecture](../../backend/ARCHITECTURE.md)
- [API Contracts](../../api/API_CONTRACTS.md)
- [Embedding Strategy](../../backend/EMBEDDING_STRATEGY.md)
- [Onboarding System](../ONBOARDING_SYSTEM.md)

## Changelog

### Version 1.0.0 (Initial Release)

- Implemented Quiz API (startSection1, generateSection2, completeQuiz)
- Implemented Profile API (getTasteDNA, getGrowthPath, getMatches, getAnalytics)
- Added authentication token handling
- Added error handling and retry logic
- Documented all API methods and usage patterns
