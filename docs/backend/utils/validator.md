# validator Utility

## Purpose

Input validation utilities for quiz answers, UUIDs, vectors, and other data structures. Ensures data integrity before processing.

## Location

`backend/src/utils/validator.js`

## Functions

### validateUUID(value)

Validates UUID format.

**Parameters**: `value` (string)

**Returns**: boolean

**Example**:
```javascript
if (!validator.validateUUID(userId)) {
  throw new ValidationError('Invalid userId format')
}
```

### validateQuizAnswers(answers, expectedCount)

Validates quiz answer structure.

**Parameters**:
- `answers` (array): Quiz answers
- `expectedCount` (number): Expected number of answers (5 per section)

**Validates**:
- Exactly `expectedCount` answers
- Each answer has `questionId` and `selectedOptions`
- At least one option selected per answer
- Options are strings ≤ 500 characters

**Throws**: `ValidationError` with specific message

**Example**:
```javascript
validator.validateQuizAnswers(section1Answers, 5)
```

### validateVector(vector)

Validates embedding vector.

**Parameters**: `vector` (array)

**Validates**:
- Array length is 1024
- All values are numbers
- All values between -1 and 1

**Throws**: `ValidationError`

**Example**:
```javascript
validator.validateVector(embeddingVector)
```

### validateSessionId(sessionId)

Validates session ID format (UUID).

**Parameters**: `sessionId` (string)

**Returns**: boolean

### validateLimit(limit, max)

Validates pagination limit.

**Parameters**:
- `limit` (number): Requested limit
- `max` (number): Maximum allowed

**Returns**: Validated limit (clamped to max)

**Example**:
```javascript
const limit = validator.validateLimit(req.query.limit, 50)
// If limit > 50, returns 50
```

## Error Messages

Validation errors include specific details:

```javascript
{
  error: 'Validation failed',
  details: 'Expected 5 answers, received 3',
  field: 'section1Answers'
}
```

## Related

- Used by all handlers for input validation
- [hash](./hash.md) - Hashing utilities
- [logger](./logger.md) - Logging utilities
