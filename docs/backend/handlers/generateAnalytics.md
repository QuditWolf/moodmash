# generateAnalytics Handler

## Purpose

Generates behavioral insights and analytics about the user's content consumption patterns using Claude. Provides metrics on passive vs. intentional consumption, goal alignment, content balance, and personalized recommendations.

## Location

`backend/src/handlers/generateAnalytics.js`

## Inputs

### HTTP Request
- **Method**: GET
- **Path**: `/api/profile/analytics/:userId`

### Parameters
- `userId` (required): UUID of user (from URL path)

## Outputs

### Success Response (200)
```json
{
  "analytics": {
    "passiveVsIntentionalRatio": number,
    "goalAlignment": number,
    "contentBalance": [
      {
        "category": "string",
        "percentage": number,
        "trend": "increasing|stable|decreasing"
      }
    ],
    "insights": [
      {
        "type": "strength|opportunity|pattern",
        "title": "string",
        "description": "string"
      }
    ],
    "recommendations": ["string"]
  }
}
```

### Error Responses
- **400**: Invalid userId format
- **404**: User not found or profile incomplete
- **401**: Unauthorized
- **500**: Analytics generation failed

## Algorithm

1. Validate userId format (UUID)
2. Retrieve user profile from DynamoDB
3. Validate user exists with DNA profile and growth path
4. Build analytics context:
   - Taste DNA profile
   - Growth path data
   - Historical activity (if available)
5. Load analytics generation prompt template
6. Inject context into prompt
7. Call Claude 3.5 Sonnet with:
   - Temperature: 0.6 (balanced creativity/accuracy)
   - Max tokens: 2000
8. Parse analytics from Claude response:
   - Extract passive vs. intentional ratio
   - Extract goal alignment score
   - Parse content balance data
   - Extract insights (strengths, opportunities, patterns)
   - Extract recommendations
9. Store analytics in Users table:
   - userId
   - analytics object
   - analyticsGeneratedAt timestamp
10. Return analytics to client

## Dependencies

- **Services**:
  - `claudeService` - Generate analytics
  - `dynamoClient` - Retrieve user data, store analytics
- **Utils**:
  - `validator` - Validate inputs
  - `logger` - Log operations

## Example Usage

```javascript
// Request
GET /api/profile/analytics/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <token>

// Response
{
  "analytics": {
    "passiveVsIntentionalRatio": 0.65,
    "goalAlignment": 0.78,
    "contentBalance": [
      {
        "category": "Books",
        "percentage": 45,
        "trend": "stable"
      },
      {
        "category": "Films",
        "percentage": 35,
        "trend": "increasing"
      },
      {
        "category": "Music",
        "percentage": 20,
        "trend": "decreasing"
      }
    ],
    "insights": [
      {
        "type": "strength",
        "title": "Deep Engagement with Literature",
        "description": "You consistently engage with complex literary works, showing strong commitment to depth over breadth."
      },
      {
        "type": "opportunity",
        "title": "Expand Creative Practice",
        "description": "Your 'Create' activities are underutilized. Consider dedicating time to creative exercises to deepen your taste understanding."
      },
      {
        "type": "pattern",
        "title": "Weekend Consumption Spike",
        "description": "Your content consumption increases significantly on weekends, suggesting intentional time allocation for taste development."
      }
    ],
    "recommendations": [
      "Set aside 30 minutes daily for 'Reflect' activities to process your consumption",
      "Try one 'Create' activity per week to balance passive and active engagement",
      "Explore music recommendations to diversify your content balance"
    ]
  }
}
```

## Error Handling

- Validates userId is valid UUID
- Returns 404 if user not found
- Returns 404 if DNA or growth path not generated
- Retries Claude API calls up to 3 times
- Validates parsed analytics structure
- Ensures all required fields are present

## Performance Considerations

- DynamoDB retrieval: ~50ms
- Claude API call: 3-6 seconds
- DynamoDB update: ~100ms
- Total response time: 3-7 seconds
- Analytics can be cached and regenerated periodically

## Analytics Metrics

### Passive vs. Intentional Ratio
- **Range**: 0 to 1
- **0.0**: Entirely passive consumption
- **0.5**: Balanced passive and intentional
- **1.0**: Entirely intentional engagement
- Calculated from growth path activity patterns

### Goal Alignment Score
- **Range**: 0 to 1
- **0.0**: No alignment with stated goals
- **1.0**: Perfect alignment
- Measures how well consumption matches DNA preferences

### Content Balance
- Percentage breakdown by category
- Trend indicators (increasing/stable/decreasing)
- Helps identify over/under-consumption areas

### Insights
- **Strengths**: Positive patterns to reinforce
- **Opportunities**: Areas for growth
- **Patterns**: Behavioral observations

### Recommendations
- Actionable suggestions (3-5 items)
- Specific and achievable
- Aligned with DNA profile
- Address identified opportunities

## Use Cases

1. **Self-awareness**: Help users understand their consumption patterns
2. **Goal setting**: Identify areas for improvement
3. **Habit formation**: Suggest specific behavioral changes
4. **Progress tracking**: Monitor taste development over time
5. **Engagement**: Provide personalized insights to increase retention

## Future Enhancements

- Historical trend analysis (requires activity tracking)
- Comparative analytics (vs. similar users)
- Predictive recommendations (ML-based)
- Integration with external platforms (Goodreads, Letterboxd, etc.)

## Related Handlers

- [generateDNA](./generateDNA.md) - Provides taste profile data
- [generatePath](./generatePath.md) - Provides activity data
