# generateSection1 Handler

## Purpose

Generates 5 foundational quiz questions (Section 1) using Claude 3.5 Sonnet to establish baseline taste preferences. Creates a new session to track the user's quiz progress.

## Location

`backend/src/handlers/generateSection1.js`

## Inputs

### HTTP Request
- **Method**: POST
- **Path**: `/api/quiz/section1/start`
- **Body**: 
```json
{
  "userId": "string (optional)"
}
```

### Parameters
- `userId` (optional): UUID of authenticated user

## Outputs

### Success Response (200)
```json
{
  "sessionId": "uuid-string",
  "questions": [
    {
      "id": "string",
      "title": "string",
      "category": "string",
      "options": ["string"],
      "multiSelect": boolean
    }
  ],
  "expiresAt": number
}
```

### Error Responses
- **500**: Claude invocation failed
- **503**: Service temporarily unavailable

## Algorithm

1. Generate unique session ID (UUID)
2. Load adaptive quiz prompt template
3. Call Claude 3.5 Sonnet to generate 5 foundational questions
4. Parse questions from Claude response
5. Create session record in DynamoDB with:
   - sessionId
   - userId (if provided)
   - section1Questions
   - createdAt timestamp
   - status: "section1_complete"
6. Return sessionId and questions to client

## Dependencies

- **Services**:
  - `claudeService` - Generate questions via Claude
  - `dynamoClient` - Store session data
- **Utils**:
  - `validator` - Validate inputs
  - `logger` - Log operations

## Example Usage

```javascript
// Request
POST /api/quiz/section1/start
Content-Type: application/json

{
  "userId": "123e4567-e89b-12d3-a456-426614174000"
}

// Response
{
  "sessionId": "987fcdeb-51a2-43f1-b9c8-123456789abc",
  "questions": [
    {
      "id": "q1",
      "title": "What type of content do you consume most often?",
      "category": "consumption_patterns",
      "options": ["Books", "Films", "Music", "Podcasts"],
      "multiSelect": true
    },
    // ... 4 more questions
  ],
  "expiresAt": 1704067200
}
```

## Error Handling

- Retries Claude API calls up to 3 times with exponential backoff
- Logs all errors with context (sessionId, userId)
- Returns user-friendly error messages
- Does not expose internal error details

## Performance Considerations

- Claude API call typically takes 2-5 seconds
- Session creation in DynamoDB adds ~100ms
- Total response time: 2-6 seconds
- Consider provisioned concurrency for production

## Related Handlers

- [generateSection2](./generateSection2.md) - Next step in quiz flow
- [generateEmbedding](./generateEmbedding.md) - Final quiz processing
