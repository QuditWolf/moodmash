# weightingEngine Utility

## Purpose

Applies intelligent weighting to embedding vectors based on answer patterns. Enhances embedding quality by emphasizing important dimensions and adjusting for answer characteristics.

## Location

`backend/src/embedding/weightingEngine.js`

## Interface

```javascript
function apply(vector, answers)
```

## Method

### apply(vector, answers)

Applies weighting to embedding vector.

**Parameters**:
- `vector` (number[]): 1024-dimensional embedding from Titan
- `answers` (object): Complete quiz responses

**Returns**: number[] - Weighted vector (NOT normalized)

**Preconditions**:
- Vector is 1024-dimensional normalized embedding
- Answers contains complete quiz responses
- Weighting rules are loaded and valid

**Postconditions**:
- Returns 1024-dimensional weighted vector
- Weights applied based on answer patterns
- Vector maintains semantic meaning
- Result is NOT normalized (requires separate normalization)

**Example**:
```javascript
const rawEmbedding = [...] // From Titan
const weighted = weightingEngine.apply(rawEmbedding, allAnswers)
const normalized = normalizeVector(weighted)
```

## Weighting Strategies

### 1. Multi-select Emphasis
Questions with multiple selections get higher weight:
```javascript
weight = 1.0 + (selectedCount - 1) * 0.1
// 1 selection: 1.0
// 2 selections: 1.1
// 3 selections: 1.2
```

### 2. Category Balance
Adjust weights to balance category representation:
```javascript
// If user heavily favors one category, reduce its dominance
categoryWeight = 1.0 / sqrt(categoryFrequency)
```

### 3. Specificity Boost
More specific answers get higher weight:
```javascript
// Specific: "Magical Realism" > Generic: "Fiction"
specificityWeight = 1.0 + specificityScore * 0.2
```

### 4. Consistency Reward
Consistent patterns across sections get boosted:
```javascript
// If Section 1 and Section 2 align, increase weight
consistencyWeight = 1.0 + alignmentScore * 0.15
```

## Algorithm

```javascript
function apply(vector, answers) {
  const weights = calculateWeights(answers)
  
  return vector.map((value, index) => {
    const dimensionWeight = weights[index] || 1.0
    return value * dimensionWeight
  })
}

function calculateWeights(answers) {
  // Analyze answer patterns
  const multiSelectWeights = analyzeMultiSelect(answers)
  const categoryWeights = analyzeCategoryBalance(answers)
  const specificityWeights = analyzeSpecificity(answers)
  const consistencyWeights = analyzeConsistency(answers)
  
  // Combine weights
  return combineWeights([
    multiSelectWeights,
    categoryWeights,
    specificityWeights,
    consistencyWeights
  ])
}
```

## Benefits

1. **Improved matching**: Better similarity scores
2. **Nuanced profiles**: Captures subtle preferences
3. **Reduced noise**: De-emphasizes generic answers
4. **Enhanced discrimination**: Better differentiation between users

## Configuration

Weighting parameters can be tuned:

```javascript
{
  multiSelectFactor: 0.1,
  categoryBalanceFactor: 0.15,
  specificityFactor: 0.2,
  consistencyFactor: 0.15
}
```

## Performance

- Time complexity: O(n) where n = 1024
- Minimal overhead: ~0.2ms
- Applied once per embedding generation

## Important Notes

- **Must normalize after weighting**: Weighting changes magnitude
- **Preserves direction**: Only adjusts emphasis
- **Deterministic**: Same answers = same weights

## Related

- [generateEmbedding handler](../handlers/generateEmbedding.md) - Uses weighting
- [normalizeVector](./normalizeVector.md) - Applied after weighting
- [embeddingBuilder](./embeddingBuilder.md) - Provides answer context
