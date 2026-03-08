# titanEmbeddingService

## Purpose

Service for generating 1024-dimensional embeddings using AWS Bedrock Titan v2 model. Handles embedding document formatting and vector extraction.

## Location

`backend/src/services/titanEmbeddingService.js`

## Interface

```javascript
async function generateEmbedding(text, options)
```

## Method

### generateEmbedding(text, options)

**Purpose**: Generate 1024-dimensional embedding vector from text

**Parameters**:
- `text` (string): Embedding document (500-2000 chars)
- `options` (object):
  - `dimensions`: 1024 (fixed for Titan v2)
  - `normalize`: true (return normalized vector)

**Returns**: 
```javascript
{
  embedding: number[], // 1024 dimensions
  inputTokens: number
}
```

**Example**:
```javascript
const result = await titanEmbeddingService.generateEmbedding(
  embeddingDocument,
  { dimensions: 1024, normalize: true }
)
// result.embedding = [0.123, -0.456, ..., 0.789] (1024 values)
```

## Configuration

```javascript
{
  modelId: 'amazon.titan-embed-text-v2:0',
  dimensions: 1024,
  normalize: true,
  retries: 2
}
```

## Performance

- API call: 1-3 seconds
- Input limit: 8192 tokens
- Output: 1024 floats (8KB)

## Related

- [bedrockClient](./bedrockClient.md) - API client
- [cacheService](./cacheService.md) - Caches embeddings
