# matchEngine Utility

## Purpose

Orchestrates the taste matching process by coordinating vector retrieval, similarity calculations, trait comparison, and result ranking. Provides high-level matching logic used by the findMatches handler.

## Location

`backend/src/matching/matchEngine.js`

## Interface

```javascript
async function findMatches(userId, limit, options)
async function findSharedTraits(dnaA, dnaB)
```

## Methods

### findMatches(userId, limit, options)

Find taste matches for a user.

**Parameters**:
- `userId` (string): UUID of requesting user
- `limit` (number): Maximum matches to return (1-50)
- `options` (object):
  - `minSimilarity`: Minimum similarity threshold (default: 0.7)
  - `includeSelf`: Include requesting user (default: false)

**Returns**: Array of Match objects

**Example**:
```javascript
const matches = await matchEngine.findMatches(
  '123e4567-e89b-12d3-a456-426614174000',
  10,
  { minSimilarity: 0.75 }
)
```

### findSharedTraits(dnaA, dnaB)

Identify shared traits between two DNA profiles.

**Parameters**:
- `dnaA` (object): First user's DNA profile
- `dnaB` (object): Second user's DNA profile

**Returns**: Array of shared trait names

**Example**:
```javascript
const shared = matchEngine.findSharedTraits(
  { traits: [{ name: 'Curiosity' }, { name: 'Depth' }] },
  { traits: [{ name: 'Curiosity' }, { name: 'Breadth' }] }
)
// Returns: ['Curiosity']
```

## Algorithm

```javascript
async function findMatches(userId, limit, options) {
  // 1. Get user's embedding
  const user = await userService.getUser(userId)
  if (!user?.vector) throw new Error('User embedding not found')
  
  // 2. Get all other users
  const allUsers = await userService.getAllUsers()
  
  // 3. Calculate similarities
  const matches = []
  for (const otherUser of allUsers) {
    if (otherUser.userId === userId) continue
    if (!otherUser.vector) continue
    
    const similarity = cosineSimilarity(user.vector, otherUser.vector)
    
    if (similarity >= options.minSimilarity) {
      const sharedTraits = findSharedTraits(
        user.tasteDNA,
        otherUser.tasteDNA
      )
      
      matches.push({
        userId: otherUser.userId,
        username: otherUser.username,
        similarity,
        sharedTraits,
        archetype: otherUser.tasteDNA?.archetype
      })
    }
  }
  
  // 4. Sort by similarity (descending)
  matches.sort((a, b) => b.similarity - a.similarity)
  
  // 5. Limit results
  return matches.slice(0, limit)
}
```

## Performance Considerations

- **Current**: O(n) scan of all users
- **Bottleneck**: Scales poorly beyond 10,000 users
- **Future**: Implement vector index (Pinecone, OpenSearch)

## Matching Quality

The engine ensures high-quality matches by:

1. **Similarity threshold**: Only matches above 0.7
2. **Trait analysis**: Identifies specific commonalities
3. **Ranking**: Best matches first
4. **Limit enforcement**: Prevents overwhelming results

## Related

- [findMatches handler](../handlers/findMatches.md) - Uses matchEngine
- [cosineSimilarity](./cosineSimilarity.md) - Core similarity calculation
- [userService](../services/userService.md) - Data retrieval
