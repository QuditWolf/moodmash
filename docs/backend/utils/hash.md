# hash Utility

## Purpose

SHA-256 hashing utilities for generating cache keys from embedding documents. Ensures consistent hashing for cache lookups.

## Location

`backend/src/utils/hash.js`

## Functions

### sha256(text)

Generate SHA-256 hash of text.

**Parameters**: `text` (string)

**Returns**: Hex string (64 characters)

**Example**:
```javascript
const docHash = hash.sha256(embeddingDocument)
// Returns: 'a1b2c3d4e5f6...' (64 hex chars)
```

### hashEmbeddingDocument(document)

Convenience wrapper for embedding documents.

**Parameters**: `document` (string)

**Returns**: SHA-256 hash

**Example**:
```javascript
const embeddingDoc = embeddingBuilder.build(allAnswers)
const cacheKey = hash.hashEmbeddingDocument(embeddingDoc)
```

## Implementation

Uses Node.js `crypto` module:

```javascript
const crypto = require('crypto')

function sha256(text) {
  return crypto
    .createHash('sha256')
    .update(text, 'utf8')
    .digest('hex')
}
```

## Properties

- **Algorithm**: SHA-256
- **Output**: 64 hex characters
- **Deterministic**: Same input always produces same hash
- **Collision resistance**: Cryptographically secure

## Use Cases

1. **Embedding cache keys**: Hash embedding documents
2. **Data integrity**: Verify data hasn't changed
3. **Deduplication**: Identify identical content

## Related

- [cacheService](../services/cacheService.md) - Uses hash for cache keys
- [embeddingBuilder](./embeddingBuilder.md) - Creates documents to hash
