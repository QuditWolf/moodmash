# dynamoClient Service

## Purpose

DynamoDB client wrapper providing simplified CRUD operations with retry logic, error handling, and connection management for Users, Sessions, and EmbeddingCache tables.

## Location

`backend/src/services/dynamoClient.js`

## Interface

```javascript
class DynamoClient {
  async get(tableName, key)
  async put(tableName, item)
  async update(tableName, key, updates)
  async delete(tableName, key)
  async scan(tableName, filters)
  async query(tableName, keyCondition, filters)
}
```

## Methods

### get(tableName, key)

Retrieve single item by primary key.

**Parameters**:
- `tableName` (string): Table name
- `key` (object): Primary key (e.g., `{ userId: 'uuid' }`)

**Returns**: Item object or null

**Example**:
```javascript
const user = await dynamoClient.get('vibegraph-users', {
  userId: '123e4567-e89b-12d3-a456-426614174000'
})
```

### put(tableName, item)

Create or replace item.

**Parameters**:
- `tableName` (string): Table name
- `item` (object): Complete item data

**Returns**: void

**Example**:
```javascript
await dynamoClient.put('vibegraph-users', {
  userId: '123e4567-e89b-12d3-a456-426614174000',
  username: 'alex_reader',
  vector: [...],
  createdAt: Date.now()
})
```

### update(tableName, key, updates)

Update specific attributes.

**Parameters**:
- `tableName` (string): Table name
- `key` (object): Primary key
- `updates` (object): Attributes to update

**Returns**: Updated item

**Example**:
```javascript
await dynamoClient.update(
  'vibegraph-users',
  { userId: '123...' },
  { tasteDNA: {...}, updatedAt: Date.now() }
)
```

### scan(tableName, filters)

Scan entire table (use sparingly).

**Parameters**:
- `tableName` (string): Table name
- `filters` (object, optional): Filter conditions

**Returns**: Array of items

**Example**:
```javascript
const allUsers = await dynamoClient.scan('vibegraph-users')
```

## Configuration

```bash
DYNAMODB_ENDPOINT=http://localhost:8000  # For local
AWS_REGION=us-east-1
USERS_TABLE=vibegraph-users
SESSIONS_TABLE=vibegraph-sessions
CACHE_TABLE=vibegraph-embedding-cache
```

## Error Handling

- Retries: 3 attempts with exponential backoff (100ms, 200ms, 400ms)
- Throws: `DynamoDBError` with context
- Logs all operations and errors

## Performance

- get(): ~50ms
- put(): ~100ms
- update(): ~100ms
- scan(): O(n) - avoid in production

## Related

- [userService](./userService.md) - Uses dynamoClient
- [cacheService](./cacheService.md) - Uses dynamoClient
