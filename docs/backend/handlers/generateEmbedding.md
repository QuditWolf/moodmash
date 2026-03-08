# generateEmbedding Handler

## Purpose

Generates a 1024-dimensional taste embedding vector from complete quiz answers using Titan v2. Implements intelligent caching to minimize API calls and applies weighting based on answer patterns. This is the core privacy-preserving component that converts raw answers into mathematical representations.

## Location

`backend/src/handlers/generateEmbedding.js`

## Inputs

### HTTP Request
- **Method**: POST
- **Path**: `/api/quiz/complete`
- **Body**:
```json
{
  "sessionId": "uuid-string",
  "userId": "uuid-string",
  "allAnswers": {
    "section1": [
      {
        "questionId": "string",
        "selectedOptions": ["string"]
      }
    ],
    "section2": [
      {
        "questionId": "string",
        "selectedOptions": ["string"]
      }
    ]
  }
}
```

### Parameters
- `sessionId` (required): UUID from quiz session
- `userId` (required): UUID of user
- `allAnswers` (required): Complete answers from both sections

## Outputs

### Success Response (200)
```json
{
  "embeddingId": "uuid-string",
  "vector": [number],  // 1024 dimensions (optional, for debugging)
  "dimension": 1024,
  "cached": boolean
}
```

### Error Responses
- **400**: Invalid sessionId, userId, or answers format
- **404**: Session not found
- **500**: Embedding generation failed

## Algorithm

1. Validate all inputs (sessionId, userId, answers)
2. Build structured embedding document from quiz answers
3. Calculate SHA-256 hash of embedding document
4. Check embedding cache for existing vector:
   - **Cache hit**: Retrieve cached vector, increment hitCount
   - **Cache miss**: Generate new embedding via Titan v2
5. If new embedding generated:
   - Call Titan v2 with 1024 dimensions
   - Store in cache with document hash
6. Apply weighting engine based on answer patterns
7. Normalize vector to unit length
8. Generate unique embeddingId
9. Store in Users table:
   - userId
   - embeddingId
   - vector (1024 dimensions)
   - dimension: 1024
   - quizVersion: "v1"
   - createdAt timestamp
10. Return embeddingId and metadata

## Dependencies

- **Services**:
  - `titanEmbeddingService` - Generate embeddings
  - `cacheService` - Cache management
  - `dynamoClient` - Store user data
- **Utils**:
  - `embeddingBuilder` - Build embedding document
  - `weightingEngine` - Apply weighting
  - `normalizeVector` - Normalize to unit length
  - `hash` - SHA-256 hashing
  - `validator` - Validate inputs
  - `logger` - Log operations

## Example Usage

```javascript
// Request
POST /api/quiz/complete
Content-Type: application/json

{
  "sessionId": "987fcdeb-51a2-43f1-b9c8-123456789abc",
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "allAnswers": {
    "section1": [
      { "questionId": "q1", "selectedOptions": ["Books", "Films"] },
      // ... 4 more
    ],
    "section2": [
      { "questionId": "q6", "selectedOptions": ["Story", "Characters"] },
      // ... 4 more
    ]
  }
}

// Response
{
  "embeddingId": "abc12345-6789-def0-1234-567890abcdef",
  "dimension": 1024,
  "cached": false
}
```

## Error Handling

- Validates exactly 5 answers per section
- Validates each answer has at least one selected option
- Validates option strings are max 500 characters
- Retries Titan API calls up to 2 times
- Does NOT store partial data on failure
- Logs cache hit/miss rates

## Performance Considerations

- **Cache hit**: ~150ms (DynamoDB retrieval + normalization)
- **Cache miss**: 1-3 seconds (Titan API + caching + normalization)
- Target cache hit rate: 40%
- Embedding document size: 500-2000 characters
- Vector storage: ~8KB per user (1024 floats)

## Privacy Guarantees

- **Raw quiz answers are NEVER stored in Users table**
- Only the 1024-dimensional vector is persisted
- Embeddings are mathematically irreversible
- Cache uses document hash, not user identifiers
- Session data can be deleted after embedding generation

## Caching Strategy

- Cache key: SHA-256 hash of embedding document
- Cache stores: vector, createdAt, hitCount, lastAccessedAt
- Cache benefits:
  - Reduces Titan API costs
  - Faster response for common answer patterns
  - Enables A/B testing without re-embedding

## Vector Properties

- **Dimension**: 1024 (Titan v2 standard)
- **Normalization**: Unit length (magnitude = 1.0)
- **Value range**: -1 to 1 per dimension
- **Weighting**: Applied before normalization
- **Similarity metric**: Cosine similarity

## Related Handlers

- [generateSection2](./generateSection2.md) - Previous step
- [generateDNA](./generateDNA.md) - Parallel processing
- [findMatches](./findMatches.md) - Uses embedding for matching
