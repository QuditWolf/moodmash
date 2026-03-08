# findMatches Handler

## Purpose

Finds taste-based matches between users by calculating cosine similarity on embedding vectors. Returns users with similar taste profiles, including shared traits and similarity scores.

## Location

`backend/src/handlers/findMatches.js`

## Inputs

### HTTP Request
- **Method**: GET
- **Path**: `/api/profile/matches/:userId`
- **Query Parameters**:
  - `limit` (optional): Maximum matches to return (default: 10, max: 50)

### Parameters
- `userId` (required): UUID of user (from URL path)
- `limit` (optional): Number of matches to return

## Outputs

### Success Response (200)
```json
{
  "matches": [
    {
      "userId": "uuid-string",
      "username": "string",
      "similarity": number,
      "sharedTraits": ["string"],
      "archetype": "string"
    }
  ]
}
```

### Error Responses
- **400**: Invalid userId or limit parameter
- **404**: User not found or embedding not generated
- **401**: Unauthorized
- **500**: Matching failed

## Algorithm

1. Validate userId format (UUID)
2. Validate limit parameter (1-50)
3. Retrieve user's embedding vector from DynamoDB
4. Validate user exists and has embedding
5. Scan all users from DynamoDB (optimize with vector index in production)
6. For each other user:
   - Skip if same as requesting user
   - Skip if no embedding vector
   - Calculate cosine similarity between vectors
   - If similarity > 0.7:
     - Find shared traits between DNA profiles
     - Add to matches array
7. Sort matches by similarity (descending)
8. Limit results to requested number
9. Return matches to client

## Dependencies

- **Services**:
  - `dynamoClient` - Retrieve user data
  - `matchEngine` - Orchestrate matching logic
- **Utils**:
  - `cosineSimilarity` - Calculate vector similarity
  - `validator` - Validate inputs
  - `logger` - Log operations

## Example Usage

```javascript
// Request
GET /api/profile/matches/123e4567-e89b-12d3-a456-426614174000?limit=5
Authorization: Bearer <token>

// Response
{
  "matches": [
    {
      "userId": "987fcdeb-51a2-43f1-b9c8-123456789abc",
      "username": "alex_reader",
      "similarity": 0.89,
      "sharedTraits": ["Curiosity", "Depth", "Emotional Resonance"],
      "archetype": "The Literary Wanderer"
    },
    {
      "userId": "456def78-90ab-cdef-1234-567890abcdef",
      "username": "story_seeker",
      "similarity": 0.82,
      "sharedTraits": ["Curiosity", "Depth"],
      "archetype": "The Narrative Explorer"
    }
    // ... up to 3 more
  ]
}
```

## Error Handling

- Validates userId is valid UUID
- Validates limit is between 1 and 50
- Returns 404 if user not found
- Returns 404 if embedding not generated
- Handles empty results gracefully
- Logs matching performance metrics

## Performance Considerations

- DynamoDB scan: O(n) where n = total users
- Cosine similarity: O(1024) per comparison
- For 1000 users: ~2-3 seconds
- For 10000 users: ~20-30 seconds
- **Production optimization needed**: Vector index or approximate nearest neighbor search

## Similarity Threshold

- **Minimum similarity**: 0.7 (70% match)
- **Similarity range**: -1 to 1
  - 1.0 = Identical taste profiles
  - 0.7-0.9 = Strong match
  - 0.5-0.7 = Moderate match (filtered out)
  - < 0.5 = Weak match (filtered out)

## Shared Traits Detection

- Compares trait names from both DNA profiles
- Matches are case-insensitive
- Returns array of trait names present in both profiles
- Helps users understand why they match

## Matching Quality

- High similarity (>0.85): Very similar taste preferences
- Medium similarity (0.75-0.85): Compatible with differences
- Low similarity (0.70-0.75): Some overlap, worth exploring

## Privacy Considerations

- Only returns public profile information
- Does not expose raw quiz answers
- Does not expose embedding vectors
- Respects user privacy settings (future enhancement)

## Scalability Considerations

Current implementation uses DynamoDB scan, which doesn't scale well beyond 10,000 users. Production improvements:

1. **Vector Database**: Use Pinecone, Weaviate, or OpenSearch
2. **Approximate Nearest Neighbor**: HNSW or IVF algorithms
3. **Batch Processing**: Pre-compute matches periodically
4. **Caching**: Cache match results with TTL
5. **Pagination**: Return matches in batches

## Related Handlers

- [generateEmbedding](./generateEmbedding.md) - Creates vectors for matching
- [generateDNA](./generateDNA.md) - Provides trait data for shared traits
