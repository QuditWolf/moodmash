# embeddingBuilder Utility

## Purpose

Builds structured embedding documents from quiz answers. Formats responses into semantic text suitable for Titan v2 embedding generation while ensuring consistent formatting for cache effectiveness.

## Location

`backend/src/embedding/embeddingBuilder.js`

## Interface

```javascript
function build(allAnswers)
```

## Method

### build(allAnswers)

Converts quiz answers into structured text document.

**Parameters**:
- `allAnswers` (object):
  - `section1`: Array of 5 answers
  - `section2`: Array of 5 answers

**Returns**: String (500-2000 characters)

**Example**:
```javascript
const embeddingDoc = embeddingBuilder.build({
  section1: [
    { questionId: 'q1', selectedOptions: ['Books', 'Films'] },
    // ... 4 more
  ],
  section2: [
    { questionId: 'q6', selectedOptions: ['Story', 'Characters'] },
    // ... 4 more
  ]
})

// Returns formatted text:
// "User taste profile based on quiz responses:
//  Content preferences: Books, Films
//  Motivation: Story, Characters
//  ..."
```

## Document Structure

The embedding document follows this format:

```
User taste profile based on quiz responses:

Section 1 - Foundational Preferences:
- Question 1: [selected options]
- Question 2: [selected options]
...

Section 2 - Deeper Exploration:
- Question 6: [selected options]
- Question 7: [selected options]
...

Overall taste signature: [summary]
```

## Design Principles

1. **Semantic richness**: Include context, not just raw answers
2. **Consistency**: Same format for all users (enables caching)
3. **Completeness**: Include all relevant information
4. **Conciseness**: Keep under 2000 characters for Titan efficiency

## Cache Effectiveness

Consistent formatting ensures:
- Identical answer patterns produce identical documents
- SHA-256 hashing works reliably
- Cache hit rate maximized

## Related

- [generateEmbedding handler](../handlers/generateEmbedding.md) - Uses builder
- [titanEmbeddingService](../services/titanEmbeddingService.md) - Embeds document
- [hash](./hash.md) - Hashes document for caching
