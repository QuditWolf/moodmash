# cacheService

## Purpose

Manages embedding cache to minimize Titan API calls. Uses SHA-256 hashing of embedding documents as cache keys and tracks hit counts and access patterns.

## Location

`backend/src/services/cacheService.js`

## Interface

```javascript
async function get(docHash)
async function put(docHash, vector)
async function incrementHitCount(docHash)
```

## Methods

### get(docHash)

Retrieve cached embedding vector.

**Parameters**:
- `docHash` (string): SHA-256 hash of embedding document

**Returns**: 
```javascript
{
  vector: number[],      // 1024 dimensions
  createdAt: number,
  hitCount: number,
  lastAccessedAt: number
} | null
```

**Example**:
```javascript
const cached = await cacheService.get(
  'a1b2c3d4e5f6...' // SHA-256 hash
)
if (cached) {
  console.log('Cache hit!', cached.vector)
}
```

### put(docHash, vector)

Store embedding in cache.

**Parameters**:
- `docHash` (string): SHA-256 hash
- `vector` (number[]): 1024-dimensional embedding

**Returns**: void

**Example**:
```javascript
await cacheService.put(docHash, embeddingVector)
```

### incrementHitCount(docHash)

Update cache statistics on hit.

**Parameters**:
- `docHash` (string): SHA-256 hash

**Returns**: void

## Cache Strategy

- **Key**: SHA-256 hash of embedding document
- **Value**: Vector + metadata
- **TTL**: None (permanent cache)
- **Target hit rate**: 40%

## Benefits

- Reduces Titan API costs
- Faster response times (150ms vs 1-3s)
- Enables A/B testing without re-embedding
- Supports identical answer patterns across users

## Performance

- get(): ~50ms (DynamoDB)
- put(): ~100ms (DynamoDB)
- Cache hit: Saves 1-3 seconds per embedding

## Related

- [generateEmbedding handler](../handlers/generateEmbedding.md) - Uses cache
- [hash util](../utils/hash.md) - Generates cache keys
