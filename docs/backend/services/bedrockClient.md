# bedrockClient Service

## Purpose

Low-level AWS Bedrock API client that handles authentication, request formatting, and error handling for all Bedrock model invocations. Provides a unified interface for Claude and Titan services.

## Location

`backend/src/services/bedrockClient.js`

## Interface

```javascript
class BedrockClient {
  constructor(config)
  async invoke(modelId, payload, options)
  async invokeWithRetry(modelId, payload, retries, options)
}
```

## Methods

### constructor(config)

**Purpose**: Initialize Bedrock client with AWS configuration

**Parameters**:
- `config` (object):
  - `region`: AWS region (default: 'us-east-1')
  - `endpoint`: Custom endpoint for LocalStack (optional)
  - `credentials`: AWS credentials (optional, uses default chain)

**Example**:
```javascript
const client = new BedrockClient({
  region: 'us-east-1',
  endpoint: process.env.BEDROCK_ENDPOINT // For LocalStack
})
```

### invoke(modelId, payload, options)

**Purpose**: Invoke a Bedrock model with the given payload

**Parameters**:
- `modelId` (string): Bedrock model identifier
  - Claude: `anthropic.claude-3-5-sonnet-20241022-v2:0`
  - Titan: `amazon.titan-embed-text-v2:0`
- `payload` (object): Model-specific request body
- `options` (object, optional):
  - `timeout`: Request timeout in ms (default: 30000)
  - `contentType`: Content type (default: 'application/json')

**Returns**: Promise<object> - Model response

**Throws**:
- `BedrockError` - API errors
- `TimeoutError` - Request timeout
- `ValidationError` - Invalid parameters

**Example**:
```javascript
const response = await client.invoke(
  'anthropic.claude-3-5-sonnet-20241022-v2:0',
  {
    messages: [{ role: 'user', content: 'Hello' }],
    max_tokens: 1000,
    temperature: 0.7
  }
)
```

### invokeWithRetry(modelId, payload, retries, options)

**Purpose**: Invoke model with automatic retry on transient failures

**Parameters**:
- `modelId` (string): Bedrock model identifier
- `payload` (object): Model-specific request body
- `retries` (number): Maximum retry attempts (default: 3)
- `options` (object, optional): Same as `invoke()`

**Returns**: Promise<object> - Model response

**Retry Logic**:
- Exponential backoff: 100ms, 200ms, 400ms, 800ms
- Retries on: 429 (throttling), 500, 502, 503, 504
- No retry on: 400, 401, 403, 404

**Example**:
```javascript
const response = await client.invokeWithRetry(
  'anthropic.claude-3-5-sonnet-20241022-v2:0',
  payload,
  3 // Max 3 retries
)
```

## Error Handling

### Error Types

```javascript
class BedrockError extends Error {
  constructor(message, statusCode, modelId)
}

class ThrottlingError extends BedrockError {
  // 429 - Rate limit exceeded
}

class ValidationError extends BedrockError {
  // 400 - Invalid request
}

class AuthenticationError extends BedrockError {
  // 401, 403 - Auth failures
}

class ServiceError extends BedrockError {
  // 500, 502, 503, 504 - Service issues
}
```

### Error Response Format

```javascript
{
  error: {
    message: 'Error description',
    code: 'ERROR_CODE',
    statusCode: 500,
    modelId: 'anthropic.claude-3-5-sonnet-20241022-v2:0',
    requestId: 'uuid'
  }
}
```

## Configuration

### Environment Variables

```bash
AWS_REGION=us-east-1
BEDROCK_ENDPOINT=http://localhost:4566  # For LocalStack
AWS_ACCESS_KEY_ID=test                  # For LocalStack
AWS_SECRET_ACCESS_KEY=test              # For LocalStack
```

### LocalStack Setup

For local development with LocalStack:

```javascript
const client = new BedrockClient({
  region: 'us-east-1',
  endpoint: 'http://localhost:4566',
  credentials: {
    accessKeyId: 'test',
    secretAccessKey: 'test'
  }
})
```

## Performance Considerations

- **Timeout**: Default 30s, adjust based on model
- **Connection pooling**: Reuse client instances
- **Retry overhead**: 3 retries can add 1-2 seconds
- **Rate limits**: Claude: 100 req/min, Titan: 200 req/min

## Logging

Logs include:
- Request start with modelId and payload size
- Response time and token usage
- Errors with full context
- Retry attempts

Example log:
```json
{
  "level": "info",
  "message": "Bedrock invocation",
  "modelId": "anthropic.claude-3-5-sonnet-20241022-v2:0",
  "duration": 2345,
  "inputTokens": 150,
  "outputTokens": 500,
  "requestId": "abc-123"
}
```

## Testing

### Unit Tests
```javascript
// Mock Bedrock client
const mockClient = {
  invoke: jest.fn().mockResolvedValue({ response: 'data' })
}
```

### Integration Tests
```javascript
// Use LocalStack for integration tests
const client = new BedrockClient({
  endpoint: 'http://localhost:4566'
})
```

## Related Services

- [claudeService](./claudeService.md) - Uses bedrockClient for Claude
- [titanEmbeddingService](./titanEmbeddingService.md) - Uses bedrockClient for Titan
