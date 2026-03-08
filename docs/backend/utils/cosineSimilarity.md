# cosineSimilarity Utility

## Purpose

Calculates cosine similarity between two embedding vectors. Measures the cosine of the angle between vectors, providing a similarity score from -1 to 1.

## Location

`backend/src/matching/cosineSimilarity.js`

## Interface

```javascript
function cosineSimilarity(vectorA, vectorB)
```

## Method

### cosineSimilarity(vectorA, vectorB)

Calculates similarity between two vectors.

**Parameters**:
- `vectorA` (number[]): 1024-dimensional normalized vector
- `vectorB` (number[]): 1024-dimensional normalized vector

**Returns**: number (-1 to 1)

**Preconditions**:
- Both vectors are non-null arrays
- Both vectors have length 1024
- All values are between -1 and 1
- Vectors are normalized (unit length)

**Postconditions**:
- Returns number between -1 and 1
- 1.0 = identical vectors
- 0.0 = orthogonal vectors
- -1.0 = opposite vectors

**Example**:
```javascript
const userA = [0.1, 0.2, 0.3, ...] // 1024 values
const userB = [0.15, 0.18, 0.32, ...] // 1024 values

const similarity = cosineSimilarity(userA, userB)
console.log(similarity) // 0.87 (high similarity)
```

## Algorithm

```javascript
function cosineSimilarity(vectorA, vectorB) {
  // Calculate dot product
  let dotProduct = 0
  for (let i = 0; i < vectorA.length; i++) {
    dotProduct += vectorA[i] * vectorB[i]
  }
  
  // For normalized vectors, dot product = cosine similarity
  return dotProduct
}
```

## Mathematical Formula

For normalized vectors:
```
cosine_similarity = dot_product(A, B)
                  = A₁×B₁ + A₂×B₂ + ... + Aₙ×Bₙ
```

For non-normalized vectors:
```
cosine_similarity = dot_product(A, B) / (||A|| × ||B||)
```

## Interpretation

| Similarity | Meaning | Use Case |
|-----------|---------|----------|
| 0.9 - 1.0 | Nearly identical | Very strong match |
| 0.7 - 0.9 | High similarity | Good match (our threshold) |
| 0.5 - 0.7 | Moderate similarity | Some overlap |
| 0.0 - 0.5 | Low similarity | Different tastes |
| < 0.0 | Opposite | Inverse preferences |

## Performance

- Time complexity: O(n) where n = 1024
- Single pass through vectors
- ~0.05ms for 1024-dimensional vectors
- Highly optimized for repeated calculations

## Why Cosine Similarity?

1. **Scale invariant**: Measures angle, not magnitude
2. **Normalized range**: Always -1 to 1
3. **Intuitive**: Higher = more similar
4. **Efficient**: Simple dot product for normalized vectors
5. **Standard**: Widely used in recommendation systems

## Related

- [findMatches handler](../handlers/findMatches.md) - Uses for matching
- [normalizeVector](./normalizeVector.md) - Prerequisite for accuracy
- [matchEngine](./matchEngine.md) - Orchestrates matching logic
