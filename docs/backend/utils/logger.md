# logger Utility

## Purpose

Structured logging utility for consistent log formatting across all backend components. Supports multiple log levels and contextual information.

## Location

`backend/src/utils/logger.js`

## Interface

```javascript
logger.info(message, context)
logger.warn(message, context)
logger.error(message, context)
logger.debug(message, context)
```

## Methods

### info(message, context)

Log informational messages.

**Example**:
```javascript
logger.info('Quiz section 1 generated', {
  sessionId: 'abc-123',
  questionCount: 5,
  duration: 2345
})
```

### warn(message, context)

Log warnings.

**Example**:
```javascript
logger.warn('Cache miss', {
  docHash: 'a1b2c3...',
  operation: 'generateEmbedding'
})
```

### error(message, context)

Log errors with stack traces.

**Example**:
```javascript
logger.error('Claude API failed', {
  error: err.message,
  stack: err.stack,
  modelId: 'anthropic.claude-3-5-sonnet...',
  retries: 3
})
```

### debug(message, context)

Log debug information (only in development).

**Example**:
```javascript
logger.debug('Vector normalized', {
  originalMagnitude: 1.234,
  normalizedMagnitude: 1.0
})
```

## Log Format

JSON structured logs:

```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "level": "info",
  "message": "Quiz section 1 generated",
  "sessionId": "abc-123",
  "questionCount": 5,
  "duration": 2345,
  "service": "vibegraph-backend"
}
```

## Configuration

```bash
LOG_LEVEL=info  # debug, info, warn, error
LOG_FORMAT=json # json or text
```

## Best Practices

1. **Include context**: Always add relevant IDs and metadata
2. **No sensitive data**: Never log tokens, passwords, or raw quiz answers
3. **Performance metrics**: Log durations for operations
4. **Error details**: Include error messages and stack traces
5. **Consistent naming**: Use camelCase for context keys

## What NOT to Log

- JWT tokens
- Raw quiz answers
- Embedding vectors (too large)
- AWS credentials
- User passwords or PII

## Related

- Used by all handlers and services
- [CloudWatch integration](../../infrastructure/monitoring.md)
