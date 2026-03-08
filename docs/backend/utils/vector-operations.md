# Vector Operations Utilities

## Purpose

Provides core vector mathematics operations for embedding manipulation and similarity calculation. Includes normalization to unit length and cosine similarity computation for taste matching.

## Location

`backend/src/utils/vector_ops.py`

## Functions

### normalize_vector(vector)

Normalizes a vector to unit length (magnitude = 1.0).

**Parameters**:
- `vector` (List[float]): List of float values representing the vector

**Returns**: List[float] - Normalized vector with magnitude approximately 1.0

**Raises**:
- `ValueError`: If vector is empty or has zero magnitude

**Preconditions**:
- vector is non-empty list of numbers
- vector is not zero vector (magnitude > 0)

**Postconditions**:
- Returns list of same length as input
- Resulting vector has unit length (magnitude = 1.0 within 0.0001 tolerance)
- Direction preserved from original vector
- No mutations to input vector

**Example**:
```python
from backend.src.utils.vector_ops import normalize_vector

# Normalize a simple vector
vector = [3.0, 4.0]
normalized = normalize_vector(vector)
# Result: [0.6, 0.8] with magnitude 1.0

# Normalize 1024-dimensional embedding
embedding = [0.5] * 1024
normalized_embedding = normalize_vector(embedding)
# All embeddings normalized to unit length for consistent comparison
```

**Algorithm**:
1. Calculate magnitude (L2 norm): `||v|| = sqrt(v₁² + v₂² + ... + vₙ²)`
2. Divide each element by magnitude: `v_normalized = v / ||v||`
3. Result has unit length: `||v_normalized|| = 1.0`

**Why Normalize?**
- **Cosine similarity**: Requires unit vectors for accurate calculation
- **Consistent scale**: All vectors on same scale regardless of input
- **Numerical stability**: Prevents overflow/underflow in calculations
- **Fair comparison**: Enables comparison between vectors of different origins

---

### cosine_similarity(vector_a, vector_b)

Calculates cosine similarity between two vectors.

**Parameters**:
- `vector_a` (List[float]): First normalized vector
- `vector_b` (List[float]): Second normalized vector

**Returns**: float - Cosine similarity score between -1 and 1

**Raises**:
- `ValueError`: If vectors have different lengths or are empty

**Preconditions**:
- vector_a and vector_b are non-null lists
- vector_a.length == vector_b.length
- Vectors are normalized (unit length)

**Postconditions**:
- Returns float between -1 and 1
- Result represents cosine of angle between vectors
- Higher values indicate greater similarity
- 1.0 means identical vectors, 0.0 means orthogonal, -1.0 means opposite

**Example**:
```python
from backend.src.utils.vector_ops import normalize_vector, cosine_similarity

# Compare two user embeddings
user1_vector = normalize_vector([...])  # 1024-dim
user2_vector = normalize_vector([...])  # 1024-dim

similarity = cosine_similarity(user1_vector, user2_vector)
# Result: 0.85 (high similarity - good match!)

# Identical vectors
vec = normalize_vector([1.0, 2.0, 3.0])
similarity = cosine_similarity(vec, vec)
# Result: 1.0 (perfect match)

# Opposite vectors
vec_a = normalize_vector([1.0] * 1024)
vec_b = normalize_vector([-1.0] * 1024)
similarity = cosine_similarity(vec_a, vec_b)
# Result: -1.0 (completely opposite)
```

**Algorithm**:
1. Calculate dot product: `dot = Σ(aᵢ × bᵢ)`
2. For normalized vectors, dot product equals cosine similarity
3. Clamp result to [-1, 1] to handle floating point errors

**Mathematical Properties**:
- **Symmetric**: `cos_sim(a, b) = cos_sim(b, a)`
- **Bounded**: Always returns value in [-1, 1]
- **Geometric interpretation**: Cosine of angle between vectors
- **Normalized vectors**: Dot product equals cosine similarity

---

### validate_vector(vector, expected_dimension)

Validates that a vector meets requirements for embedding operations.

**Parameters**:
- `vector` (List[float]): Vector to validate
- `expected_dimension` (int): Expected number of dimensions (default: 1024 for Titan v2)

**Returns**: bool - True if vector is valid

**Raises**:
- `ValueError`: If vector is invalid with specific error message

**Validation Checks**:
1. Vector must be a list
2. Vector must have exactly `expected_dimension` elements
3. All elements must be numeric (int or float)
4. All values must be between -1 and 1

**Example**:
```python
from backend.src.utils.vector_ops import validate_vector

# Valid vector
vector = [0.5] * 1024
validate_vector(vector)  # Returns True

# Invalid dimension
vector = [0.5] * 512
validate_vector(vector)  # Raises ValueError: "Vector must have 1024 dimensions, got 512"

# Invalid value range
vector = [1.5] + [0.5] * 1023
validate_vector(vector)  # Raises ValueError: "Vector element 0 must be between -1 and 1"

# Custom dimension
vector = [0.1, 0.2, 0.3]
validate_vector(vector, expected_dimension=3)  # Returns True
```

## Performance

- **normalize_vector**: O(n) where n = vector dimension (1024)
  - Two passes: magnitude calculation + normalization
  - ~0.1ms for 1024-dimensional vector

- **cosine_similarity**: O(n) where n = vector dimension (1024)
  - Single pass: dot product calculation
  - ~0.05ms for 1024-dimensional vector

- **validate_vector**: O(n) where n = vector dimension (1024)
  - Single pass: validation checks
  - ~0.02ms for 1024-dimensional vector

## Use Cases

### Embedding Generation
```python
from backend.src.utils.vector_ops import normalize_vector, validate_vector

# After getting embedding from Titan
raw_embedding = titan_service.generate_embedding(document)

# Validate dimensions
validate_vector(raw_embedding)

# Normalize to unit length
normalized = normalize_vector(raw_embedding)

# Store in database
user_service.store_embedding(user_id, normalized)
```

### Taste Matching
```python
from backend.src.utils.vector_ops import cosine_similarity

# Find similar users
user_embedding = user_service.get_embedding(user_id)
all_users = user_service.get_all_users()

matches = []
for other_user in all_users:
    if other_user.id == user_id:
        continue
    
    similarity = cosine_similarity(user_embedding, other_user.embedding)
    
    if similarity > 0.7:  # Threshold for good match
        matches.append({
            'user_id': other_user.id,
            'similarity': similarity
        })

# Sort by similarity descending
matches.sort(key=lambda x: x['similarity'], reverse=True)
```

## Testing

Unit tests and property-based tests are located in:
- `backend/tests/unit/test_vector_ops.py`

**Property Tests** (using Hypothesis):
- **Property 1**: Normalizing any non-zero vector produces unit length vector
- **Property 2**: Cosine similarity is always between -1 and 1
- **Property 3**: Any vector has similarity 1.0 with itself

**Unit Tests**:
- Normalization of simple vectors
- Normalization of 1024-dimensional vectors
- Zero vector error handling
- Direction preservation
- Identical vector similarity (1.0)
- Orthogonal vector similarity (0.0)
- Opposite vector similarity (-1.0)
- Different length vector error handling

## Related

- [cosineSimilarity](./cosineSimilarity.md) - Detailed cosine similarity documentation
- [normalizeVector](./normalizeVector.md) - Detailed normalization documentation
- [generateEmbedding handler](../handlers/generateEmbedding.md) - Uses vector operations
- [findMatches handler](../handlers/findMatches.md) - Uses cosine similarity
- [weightingEngine](./weightingEngine.md) - Applied before normalization

## References

- **Requirements**: 11.1, 11.2, 11.3, 11.5, 11.6, 11.7
- **Design Properties**: Property 2 (Embedding Vector Normalization), Property 3 (Cosine Similarity Bounds)
