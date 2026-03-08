# generateDNA Handler

## Purpose

Generates a personalized taste DNA archetype using Claude 3.5 Sonnet based on quiz answers. Creates a rich profile including archetype name, trait scores, category preferences, and descriptive text that helps users understand their unique taste personality.

## Location

`backend/src/handlers/generateDNA.js`

## Inputs

### HTTP Request
- **Method**: POST
- **Path**: `/api/quiz/complete` (called in parallel with generateEmbedding)
- **Body**:
```json
{
  "userId": "uuid-string",
  "allAnswers": {
    "section1": [{ "questionId": "string", "selectedOptions": ["string"] }],
    "section2": [{ "questionId": "string", "selectedOptions": ["string"] }]
  }
}
```

### Parameters
- `userId` (required): UUID of user
- `allAnswers` (required): Complete quiz responses

## Outputs

### Success Response (200)
```json
{
  "tasteDNA": {
    "archetype": "string",
    "traits": [
      {
        "name": "string",
        "score": number,
        "description": "string"
      }
    ],
    "categories": [
      {
        "category": "string",
        "preferences": ["string"],
        "intensity": number
      }
    ],
    "description": "string"
  }
}
```

### Error Responses
- **400**: Invalid userId or answers format
- **500**: DNA generation failed

## Algorithm

1. Validate userId and allAnswers
2. Build answer summary from quiz responses
3. Load DNA generation prompt template
4. Inject answer summary into prompt
5. Call Claude 3.5 Sonnet with:
   - Temperature: 0.8 (creative generation)
   - Max tokens: 1500
6. Parse DNA profile from Claude response:
   - Extract archetype name
   - Parse trait scores (0-10 scale)
   - Parse category preferences
   - Extract description
7. Store DNA profile in Users table:
   - userId
   - tasteDNA object
   - updatedAt timestamp
8. Return DNA profile to client

## Dependencies

- **Services**:
  - `claudeService` - Generate DNA profile
  - `dynamoClient` - Store DNA data
- **Utils**:
  - `validator` - Validate inputs
  - `logger` - Log operations

## Example Usage

```javascript
// Request
POST /api/quiz/complete
Content-Type: application/json

{
  "userId": "123e4567-e89b-12d3-a456-426614174000",
  "allAnswers": {
    "section1": [
      { "questionId": "q1", "selectedOptions": ["Books", "Films"] }
      // ... more answers
    ],
    "section2": [
      { "questionId": "q6", "selectedOptions": ["Story", "Characters"] }
      // ... more answers
    ]
  }
}

// Response
{
  "tasteDNA": {
    "archetype": "The Narrative Explorer",
    "traits": [
      {
        "name": "Curiosity",
        "score": 9,
        "description": "Driven by a desire to discover new stories and perspectives"
      },
      {
        "name": "Depth",
        "score": 8,
        "description": "Prefers complex narratives with layered meanings"
      },
      {
        "name": "Emotional Resonance",
        "score": 7,
        "description": "Values content that creates strong emotional connections"
      }
    ],
    "categories": [
      {
        "category": "Books",
        "preferences": ["Literary Fiction", "Magical Realism", "Historical"],
        "intensity": 9
      },
      {
        "category": "Films",
        "preferences": ["Character-driven Drama", "Indie Cinema"],
        "intensity": 8
      }
    ],
    "description": "You are a Narrative Explorer who seeks out stories that challenge and transform. You're drawn to complex characters and layered narratives that reveal deeper truths about the human experience."
  }
}
```

## Error Handling

- Validates all quiz answers are present
- Retries Claude API calls up to 3 times
- Validates parsed DNA structure before storing
- Ensures trait scores are 0-10
- Logs all errors with userId context

## Performance Considerations

- Claude API call: 3-6 seconds
- DynamoDB update: ~100ms
- Total response time: 3-7 seconds
- Can run in parallel with generateEmbedding

## DNA Profile Structure

### Archetype
- Creative name describing taste personality
- Examples: "The Minimalist", "The Explorer", "The Curator"
- Should be memorable and meaningful

### Traits
- 3-5 key personality traits
- Each has name, score (0-10), and description
- Scores indicate strength of trait
- Descriptions explain how trait manifests

### Categories
- Content type preferences (Books, Films, Music, etc.)
- Specific preferences within each category
- Intensity score (0-10) for engagement level

### Description
- 2-3 sentence summary
- Written in second person ("You are...")
- Captures essence of taste profile

## Related Handlers

- [generateEmbedding](./generateEmbedding.md) - Parallel processing
- [generatePath](./generatePath.md) - Uses DNA for recommendations
- [generateAnalytics](./generateAnalytics.md) - Uses DNA for insights
