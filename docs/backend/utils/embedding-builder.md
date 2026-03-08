# Embedding Builder Utility

## Purpose

Builds structured embedding documents from quiz answers. Formats responses into semantic text suitable for Titan v2 embedding generation while ensuring consistent formatting for cache effectiveness.

## Location

`backend/src/utils/embedding_builder.py`

## Functions

### build_embedding_document(all_answers)

Converts quiz answers into structured text document.

**Parameters**:
- `all_answers` (Dict[str, Any]): Dictionary containing:
  - `section1`: List of 5 answer dictionaries
  - `section2`: List of 5 answer dictionaries

**Returns**: str - Structured text document (100-5000 characters)

**Raises**:
- `ValueError`: If answers are invalid or incomplete

**Preconditions**:
- all_answers contains valid Section 1 and Section 2 responses
- Each answer has questionId and selectedOptions
- selectedOptions is non-empty list

**Postconditions**:
- Returns structured text document
- Document contains all quiz responses in semantic format
- Document length is between 100-5000 characters (truncated if needed)
- Format is consistent for caching purposes

**Example**:
```python
from backend.src.utils.embedding_builder import build_embedding_document

embedding_doc = build_embedding_document({
    'section1': [
        {'questionId': 'q1', 'selectedOptions': ['Books', 'Films']},
        {'questionId': 'q2', 'selectedOptions': ['Story-driven']},
        {'questionId': 'q3', 'selectedOptions': ['Deep', 'Thoughtful']},
        {'questionId': 'q4', 'selectedOptions': ['Solo']},
        {'questionId': 'q5', 'selectedOptions': ['Evening']}
    ],
    'section2': [
        {'questionId': 'q6', 'selectedOptions': ['Character development']},
        {'questionId': 'q7', 'selectedOptions': ['Indie', 'Experimental']},
        {'questionId': 'q8', 'selectedOptions': ['Slow burn']},
        {'questionId': 'q9', 'selectedOptions': ['Introspective']},
        {'questionId': 'q10', 'selectedOptions': ['Minimalist']}
    ]
})

# Returns formatted text:
# "=== Taste Profile: Foundational Preferences ===
#  Q1: Books, Films
#  Q2: Story-driven
#  Q3: Deep, Thoughtful
#  Q4: Solo
#  Q5: Evening
#  
#  === Taste Profile: Deep Dive Preferences ===
#  Q1: Character development
#  Q2: Indie, Experimental
#  Q3: Slow burn
#  Q4: Introspective
#  Q5: Minimalist"
```

## Document Structure

The embedding document follows this format:

```
=== Taste Profile: Foundational Preferences ===
Q1: [selected options comma-separated]
Q2: [selected options comma-separated]
Q3: [selected options comma-separated]
Q4: [selected options comma-separated]
Q5: [selected options comma-separated]

=== Taste Profile: Deep Dive Preferences ===
Q1: [selected options comma-separated]
Q2: [selected options comma-separated]
Q3: [selected options comma-separated]
Q4: [selected options comma-separated]
Q5: [selected options comma-separated]
```

## Design Principles

1. **Semantic richness**: Include context headers, not just raw answers
2. **Consistency**: Same format for all users (enables caching)
3. **Completeness**: Include all relevant information from both sections
4. **Conciseness**: Keep under 5000 characters (truncated if exceeded)
5. **Structure**: Clear section separation for better embedding quality

## Cache Effectiveness

Consistent formatting ensures:
- Identical answer patterns produce identical documents
- SHA-256 hashing works reliably
- Cache hit rate maximized (~40% target)
- Reduced Titan API calls and costs

**Example Cache Scenario**:
```python
# User A answers
doc_a = build_embedding_document(user_a_answers)
hash_a = hashlib.sha256(doc_a.encode()).hexdigest()

# User B with identical answers
doc_b = build_embedding_document(user_b_answers)
hash_b = hashlib.sha256(doc_b.encode()).hexdigest()

# If answers identical, hashes match
assert hash_a == hash_b  # Cache hit!
```

---

### apply_weights(vector, answers)

Applies weighting to embedding vector based on answer patterns.

**Parameters**:
- `vector` (List[float]): 1024-dimensional embedding vector
- `answers` (Dict[str, Any]): Complete quiz answers

**Returns**: List[float] - Weighted vector (NOT normalized)

**Raises**:
- `ValueError`: If vector or answers are invalid

**Preconditions**:
- vector is 1024-dimensional normalized embedding
- answers contains complete quiz responses

**Postconditions**:
- Returns 1024-dimensional weighted vector
- Weights applied based on answer patterns
- Vector maintains semantic meaning
- Result is NOT normalized (requires separate normalization)

**Example**:
```python
from backend.src.utils.embedding_builder import apply_weights
from backend.src.utils.vector_ops import normalize_vector

# Get raw embedding from Titan
raw_vector = titan_service.generate_embedding(document)

# Apply weighting based on answer patterns
weighted = apply_weights(raw_vector, all_answers)

# Normalize after weighting
final_vector = normalize_vector(weighted)
```

**Current Implementation**:
For MVP, uses uniform weighting (weight = 1.0 for all dimensions). Returns vector unchanged.

**Future Enhancements**:
- Boost dimensions for strongly expressed preferences
- Reduce dimensions for neutral/uncertain responses
- Apply category-specific weights
- Weight based on answer confidence scores
- Adjust for multi-select vs single-select questions

## Validation

The builder performs comprehensive validation:

```python
# Validates structure
if 'section1' not in all_answers or 'section2' not in all_answers:
    raise ValueError("Quiz answers must contain section1 and section2")

# Validates content
if not section1 or not section2:
    raise ValueError("Both sections must have answers")

# Validates each answer
for answer in section1:
    if not answer.get('selectedOptions'):
        raise ValueError(f"Answer {answer.get('questionId')} has no selected options")

# Validates document length
if len(document) < 100:
    raise ValueError(f"Document too short: {len(document)} chars (minimum 100)")
```

## Performance

- **Time complexity**: O(n) where n = total number of answers (typically 10)
- **Space complexity**: O(m) where m = document length (100-5000 chars)
- **Execution time**: ~0.5ms for typical quiz (10 answers)

## Use Cases

### Embedding Generation Flow
```python
from backend.src.utils.embedding_builder import build_embedding_document
from backend.src.services.cache_service import CacheService
from backend.src.services.titan_embedding_service import TitanEmbeddingService
import hashlib

# Build document
document = build_embedding_document(all_answers)

# Check cache
doc_hash = hashlib.sha256(document.encode()).hexdigest()
cached = cache_service.get(doc_hash)

if cached:
    vector = cached['vector']
    print("Cache hit!")
else:
    # Generate new embedding
    vector = titan_service.generate_embedding(document)
    cache_service.put(doc_hash, vector)
    print("Cache miss - generated new embedding")
```

### Privacy-First Design
```python
# Build document for embedding
document = build_embedding_document(all_answers)

# Generate embedding
vector = titan_service.generate_embedding(document)

# Store ONLY the vector, NOT the raw answers
user_service.store_embedding(user_id, vector)

# Raw answers are never persisted
# Document is only used transiently for embedding generation
```

## Testing

Unit tests are located in:
- `backend/tests/unit/test_embedding_builder.py` (to be created)

**Test Cases**:
- Valid quiz answers produce correct document format
- Document includes all sections and answers
- Document length is within bounds
- Missing sections raise ValueError
- Empty selectedOptions raise ValueError
- Consistent formatting for identical answers
- Weighting preserves vector dimensions

## Related

- [vector_ops](./vector-operations.md) - Normalization after weighting
- [generateEmbedding handler](../handlers/generateEmbedding.md) - Uses builder
- [titanEmbeddingService](../services/titanEmbeddingService.md) - Embeds document
- [cacheService](../services/cacheService.md) - Caches embeddings by document hash

## References

- **Requirements**: 3.1, 3.2, 16.1, 16.2
- **Design**: Embedding Cache Strategy section
