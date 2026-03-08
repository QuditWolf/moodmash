# generateSection2 Handler

## Purpose

Generates 5 adaptive quiz questions (Section 2) based on the user's Section 1 responses. Uses Claude to create personalized follow-up questions that dive deeper into the user's taste profile.

## Location

`backend/src/handlers/generateSection2.js`

## Inputs

### HTTP Request
- **Method**: POST
- **Path**: `/api/quiz/section2/generate`
- **Body**:
```json
{
  "sessionId": "uuid-string",
  "section1Answers": [
    {
      "questionId": "string",
      "selectedOptions": ["string"]
    }
  ]
}
```

### Parameters
- `sessionId` (required): UUID from Section 1 response
- `section1Answers` (required): Array of 5 answers from Section 1

## Outputs

### Success Response (200)
```json
{
  "questions": [
    {
      "id": "string",
      "title": "string",
      "category": "string",
      "options": ["string"],
      "multiSelect": boolean
    }
  ]
}
```

### Error Responses
- **400**: Invalid sessionId or answers format
- **404**: Session not found or expired
- **500**: Claude invocation failed

## Algorithm

1. Validate sessionId format (UUID)
2. Retrieve session from DynamoDB
3. Validate session exists and contains Section 1 questions
4. Build context from Section 1 questions and answers
5. Load adaptive quiz prompt template
6. Inject Section 1 context into prompt
7. Call Claude 3.5 Sonnet to generate adaptive Section 2 questions
8. Parse questions from Claude response
9. Update session in DynamoDB with:
   - section1Answers
   - section2Questions
   - status: "section2_complete"
10. Return Section 2 questions to client

## Dependencies

- **Services**:
  - `claudeService` - Generate adaptive questions
  - `dynamoClient` - Retrieve and update session
- **Utils**:
  - `validator` - Validate inputs
  - `logger` - Log operations

## Example Usage

```javascript
// Request
POST /api/quiz/section2/generate
Content-Type: application/json

{
  "sessionId": "987fcdeb-51a2-43f1-b9c8-123456789abc",
  "section1Answers": [
    {
      "questionId": "q1",
      "selectedOptions": ["Books", "Films"]
    },
    // ... 4 more answers
  ]
}

// Response
{
  "questions": [
    {
      "id": "q6",
      "title": "What draws you to books and films?",
      "category": "motivation",
      "options": ["Story", "Characters", "Aesthetics", "Ideas"],
      "multiSelect": true
    },
    // ... 4 more adaptive questions
  ]
}
```

## Error Handling

- Validates exactly 5 Section 1 answers provided
- Validates each answer has at least one selected option
- Retries Claude API calls up to 3 times
- Returns 404 if session not found
- Logs all errors with sessionId context

## Performance Considerations

- DynamoDB retrieval: ~50ms
- Claude API call: 3-7 seconds (adaptive generation is more complex)
- DynamoDB update: ~100ms
- Total response time: 3-8 seconds

## Privacy Notes

- Section 1 answers are stored temporarily in session
- Session data is used only for generating Section 2
- Raw answers are NOT stored in Users table
- Only embeddings are persisted long-term

## Related Handlers

- [generateSection1](./generateSection1.md) - Previous step in quiz flow
- [generateEmbedding](./generateEmbedding.md) - Next step after Section 2
