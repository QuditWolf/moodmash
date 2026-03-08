# generatePath Handler

## Purpose

Generates personalized growth path recommendations organized into Absorb, Create, and Reflect categories. Uses Claude to create tailored content suggestions based on the user's taste DNA profile.

## Location

`backend/src/handlers/generatePath.js`

## Inputs

### HTTP Request
- **Method**: GET
- **Path**: `/api/profile/path/:userId`

### Parameters
- `userId` (required): UUID of user (from URL path)

## Outputs

### Success Response (200)
```json
{
  "path": {
    "absorb": [
      {
        "id": "string",
        "title": "string",
        "description": "string",
        "category": "string",
        "estimatedTime": "string",
        "difficulty": "beginner|intermediate|advanced"
      }
    ],
    "create": [...],
    "reflect": [...],
    "generatedAt": number
  }
}
```

### Error Responses
- **400**: Invalid userId format
- **404**: User not found or DNA profile not generated
- **401**: Unauthorized
- **500**: Path generation failed

## Algorithm

1. Validate userId format (UUID)
2. Retrieve user profile from DynamoDB
3. Validate user exists and has DNA profile
4. Build context from DNA profile:
   - Archetype
   - Traits
   - Category preferences
5. Load path generation prompt template
6. Inject DNA context into prompt
7. Call Claude 3.5 Sonnet with:
   - Temperature: 0.7
   - Max tokens: 2500
8. Parse growth path from Claude response:
   - Extract Absorb recommendations (3-5 items)
   - Extract Create recommendations (3-5 items)
   - Extract Reflect recommendations (3-5 items)
9. Store path in Users table:
   - userId
   - growthPath object
   - pathGeneratedAt timestamp
10. Return growth path to client

## Dependencies

- **Services**:
  - `claudeService` - Generate recommendations
  - `dynamoClient` - Retrieve user data, store path
- **Utils**:
  - `validator` - Validate inputs
  - `logger` - Log operations

## Example Usage

```javascript
// Request
GET /api/profile/path/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <token>

// Response
{
  "path": {
    "absorb": [
      {
        "id": "abs-1",
        "title": "Read 'The Overstory' by Richard Powers",
        "description": "A sweeping novel that weaves together multiple narratives about humanity's relationship with nature",
        "category": "Books",
        "estimatedTime": "8-10 hours",
        "difficulty": "intermediate"
      },
      {
        "id": "abs-2",
        "title": "Watch 'Arrival' (2016)",
        "description": "A thought-provoking sci-fi film about language, time, and human connection",
        "category": "Films",
        "estimatedTime": "2 hours",
        "difficulty": "beginner"
      }
      // ... 1-3 more
    ],
    "create": [
      {
        "id": "cre-1",
        "title": "Write a character study",
        "description": "Choose a person you know and write 500 words exploring their inner world",
        "category": "Writing",
        "estimatedTime": "1-2 hours",
        "difficulty": "beginner"
      }
      // ... 2-4 more
    ],
    "reflect": [
      {
        "id": "ref-1",
        "title": "Journal about narrative patterns",
        "description": "Reflect on the types of stories that resonate with you and why",
        "category": "Journaling",
        "estimatedTime": "30 minutes",
        "difficulty": "beginner"
      }
      // ... 2-4 more
    ],
    "generatedAt": 1704067200
  }
}
```

## Error Handling

- Validates userId is valid UUID
- Returns 404 if user not found
- Returns 404 if DNA profile not generated yet
- Retries Claude API calls up to 3 times
- Validates parsed path structure
- Ensures each category has 3-5 recommendations

## Performance Considerations

- DynamoDB retrieval: ~50ms
- Claude API call: 4-8 seconds (complex generation)
- DynamoDB update: ~100ms
- Total response time: 4-9 seconds
- Path can be cached and regenerated periodically

## Growth Path Structure

### Absorb (Passive Consumption)
- Content to consume (books, films, music, podcasts)
- Aligned with user's taste preferences
- Introduces new perspectives within comfort zone
- Estimated time for consumption

### Create (Active Production)
- Creative exercises and projects
- Encourages active engagement with taste
- Builds skills related to preferences
- Difficulty levels for progression

### Reflect (Metacognition)
- Journaling prompts
- Discussion questions
- Self-assessment exercises
- Helps users understand their taste evolution

## Recommendation Quality

- Personalized to DNA archetype and traits
- Balanced across difficulty levels
- Specific and actionable
- Includes context and reasoning
- Respects category intensity scores

## Related Handlers

- [generateDNA](./generateDNA.md) - Required prerequisite
- [generateAnalytics](./generateAnalytics.md) - Uses path for insights
