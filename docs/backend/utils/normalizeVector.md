# normalizeVector Utility

## Purpose

Normalizes embedding vectors to unit length (magnitude = 1.0). Essential for cosine similarity calculations and consistent vector operations.

## Location

`backend/src/embedding/normalizeVector.js`

## Interface

```javascript
function normalizeVector(vector)
```

## Method

### normalizeVector(vector)

Normalizes vector to unit length.

**Parameters**: `vector` (number[]): 1024-dimensional array

**Returns**: number[] - Normalized vector

**Preconditions**:
- Vector is non-null array of 1024 numbers
- Vector is not zero vector (magnitude > 0)

**Postconditions**:
- Returns array of 1024 numbers
- Resulting vector has unit length (magnitude ≈ 1.0)
- Direction preserved from original vector
- No mutations to input vector

**Example**:
```javascript
const rawVector = [0.5, 0.3, 0.8, ...] // 1024 values
const normalized = normalizeVector(rawVector)

// Calculate magnitude
const magnitude = Math.sqrt(
  normalized.reduce((sum, val) => sum + val * val, 0)
)
console.log(magnitude) // ~1.0 (within 0.0001 tolerance)
```

## Algorithm

```javascript
function normalizeVector(vector) {
  // 1. Calculate magnitude (L2 norm)
  const magnitude = Math.sqrt(
    vector.reduce((sum, val) => sum + val * val, 0)
  )
  
  // 2. Divide each element by magnitude
  return vector.map(val => val / magnitude)
}
```

## Mathematical Properties

- **Magnitude formula**: `||v|| = sqrt(v₁² + v₂² + ... + vₙ²)`
- **Normalization**: `v_normalized = v / ||v||`
- **Result magnitude**: `||v_normalized|| = 1.0`
- **Direction preserved**: Angle between vectors unchanged

## Why Normalize?

1. **Cosine similarity**: Requires unit vectors for accurate calculation
2. **Consistent scale**: All vectors on same scale regardless of input
3. **Numerical stability**: Prevents overflow/underflow in calculations
4. **Comparison**: Enables fair comparison between vectors

## Performance

- Time complexity: O(n) where n = 1024
- Two passes: magnitude calculation + normalization
- ~0.1ms for 1024-dimensional vector

## Related

- [cosineSimilarity](./cosineSimilarity.md) - Uses normalized vectors
- [generateEmbedding handler](../handlers/generateEmbedding.md) - Normalizes embeddings
- [weightingEngine](./weightingEngine.md) - Applied before normalization
