# userService

## Purpose

High-level service for user data operations. Provides business logic layer on top of DynamoDB client for user profile management, embedding storage, and data retrieval.

## Location

`backend/src/services/userService.js`

## Interface

```javascript
async function getUser(userId)
async function createUser(userData)
async function updateUser(userId, updates)
async function storeEmbedding(userId, embeddingData)
async function storeDNA(userId, dnaProfile)
async function storePath(userId, growthPath)
async function storeAnalytics(userId, analytics)
```

## Methods

### getUser(userId)

Retrieve complete user profile.

**Returns**: User object with all data or null

### createUser(userData)

Create new user record.

**Parameters**:
- `userData` (object): username, email, etc.

**Returns**: Created user object

### updateUser(userId, updates)

Update user attributes.

**Parameters**:
- `userId` (string): UUID
- `updates` (object): Fields to update

**Returns**: Updated user object

### storeEmbedding(userId, embeddingData)

Store embedding vector in user profile.

**Parameters**:
- `userId` (string): UUID
- `embeddingData` (object):
  - `embeddingId`: UUID
  - `vector`: 1024-dimensional array
  - `dimension`: 1024
  - `quizVersion`: "v1"

**Returns**: void

### storeDNA(userId, dnaProfile)

Store taste DNA profile.

**Parameters**:
- `userId` (string): UUID
- `dnaProfile` (object): TasteDNA structure

**Returns**: void

### storePath(userId, growthPath)

Store growth path recommendations.

**Parameters**:
- `userId` (string): UUID
- `growthPath` (object): GrowthPath structure

**Returns**: void

### storeAnalytics(userId, analytics)

Store behavioral analytics.

**Parameters**:
- `userId` (string): UUID
- `analytics` (object): Analytics structure

**Returns**: void

## Example Usage

```javascript
// Get user
const user = await userService.getUser(userId)

// Store embedding
await userService.storeEmbedding(userId, {
  embeddingId: 'abc-123',
  vector: [...],
  dimension: 1024,
  quizVersion: 'v1'
})

// Store DNA
await userService.storeDNA(userId, {
  archetype: 'The Explorer',
  traits: [...],
  categories: [...],
  description: '...'
})
```

## Related

- [dynamoClient](./dynamoClient.md) - Underlying data access
- All handlers use userService for data operations
