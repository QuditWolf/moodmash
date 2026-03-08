# API Service Documentation

## Overview

The API service layer (`src/services/api.js`) provides a centralized interface for all backend communication. It abstracts HTTP request details from UI components and provides a clean, typed API for frontend developers.

## Architecture

### Base Configuration

```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
```

The base URL is configured via environment variables, allowing different endpoints for development, staging, and production.

### Core Request Handler

The `apiRequest` helper function handles all HTTP communication:

```javascript
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add auth token if available
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'API request failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};
```

**Features:**
- Automatic authentication token injection from localStorage
- Consistent error handling and parsing
- JSON request/response handling
- Configurable headers per request

## API Modules

### Authentication API

Handles user authentication and session management.

#### `authAPI.login(email, password)`

Authenticates a user with email and password.

**Parameters:**
- `email` (string): User email address
- `password` (string): User password

**Returns:** Promise resolving to:
```javascript
{
  token: string,
  user: {
    id: string,
    email: string,
    name: string
  }
}
```

**Example:**
```javascript
import { authAPI } from '@/services/api';

try {
  const response = await authAPI.login('user@example.com', 'password123');
  localStorage.setItem('authToken', response.token);
  // Handle successful login
} catch (error) {
  // Handle login error
  console.error('Login failed:', error.message);
}
```

#### `authAPI.signup(email, password, name)`

Creates a new user account.

**Parameters:**
- `email` (string): User email address
- `password` (string): User password
- `name` (string): User display name

**Returns:** Promise resolving to user object and token

**Example:**
```javascript
const response = await authAPI.signup('new@example.com', 'password123', 'John Doe');
```

#### `authAPI.logout()`

Logs out the current user.

**Returns:** Promise resolving to success confirmation

**Example:**
```javascript
await authAPI.logout();
localStorage.removeItem('authToken');
```

#### `authAPI.getCurrentUser()`

Retrieves the current authenticated user's profile.

**Returns:** Promise resolving to user object

**Example:**
```javascript
const user = await authAPI.getCurrentUser();
```

---

### User API

Manages user profile data and settings.

#### `userAPI.updateProfile(updates)`

Updates the current user's profile information.

**Parameters:**
- `updates` (object): Fields to update (name, bio, preferences, etc.)

**Returns:** Promise resolving to updated user object

**Example:**
```javascript
import { userAPI } from '@/services/api';

const updatedUser = await userAPI.updateProfile({
  name: 'Jane Doe',
  bio: 'Music enthusiast and coffee lover'
});
```

#### `userAPI.uploadAvatar(file)`

Uploads a new profile avatar image.

**Parameters:**
- `file` (File): Image file from file input

**Returns:** Promise resolving to avatar URL

**Example:**
```javascript
const fileInput = document.querySelector('input[type="file"]');
const file = fileInput.files[0];

const response = await userAPI.uploadAvatar(file);
console.log('New avatar URL:', response.avatarUrl);
```

---

### Recommendations API

Provides personalized content recommendations.

#### `recommendationsAPI.getPersonalized(category, limit)`

Fetches personalized recommendations for the current user.

**Parameters:**
- `category` (string, optional): Filter by content category
- `limit` (number, optional): Maximum number of results (default: 20)

**Returns:** Promise resolving to array of recommendation objects

**Example:**
```javascript
import { recommendationsAPI } from '@/services/api';

// Get all recommendations
const allRecs = await recommendationsAPI.getPersonalized();

// Get music recommendations only
const musicRecs = await recommendationsAPI.getPersonalized('music', 10);
```

**Response Format:**
```javascript
[
  {
    id: string,
    title: string,
    category: string,
    description: string,
    imageUrl: string,
    score: number
  }
]
```

#### `recommendationsAPI.getSimilar(itemId)`

Finds content similar to a specific item.

**Parameters:**
- `itemId` (string): ID of the reference item

**Returns:** Promise resolving to array of similar items

**Example:**
```javascript
const similarItems = await recommendationsAPI.getSimilar('item-123');
```

---

### Vibe Spaces API

Manages community spaces and memberships.

#### `vibeSpacesAPI.getAll()`

Retrieves all available vibe spaces.

**Returns:** Promise resolving to array of space objects

**Example:**
```javascript
import { vibeSpacesAPI } from '@/services/api';

const spaces = await vibeSpacesAPI.getAll();
```

**Response Format:**
```javascript
[
  {
    id: string,
    name: string,
    description: string,
    memberCount: number,
    imageUrl: string,
    tags: string[]
  }
]
```

#### `vibeSpacesAPI.getById(spaceId)`

Retrieves details for a specific space.

**Parameters:**
- `spaceId` (string): Space ID

**Returns:** Promise resolving to space object with full details

**Example:**
```javascript
const space = await vibeSpacesAPI.getById('space-456');
```

#### `vibeSpacesAPI.join(spaceId)`

Joins a vibe space.

**Parameters:**
- `spaceId` (string): Space ID to join

**Returns:** Promise resolving to membership confirmation

**Example:**
```javascript
await vibeSpacesAPI.join('space-456');
```

#### `vibeSpacesAPI.leave(spaceId)`

Leaves a vibe space.

**Parameters:**
- `spaceId` (string): Space ID to leave

**Returns:** Promise resolving to success confirmation

**Example:**
```javascript
await vibeSpacesAPI.leave('space-456');
```

---

### Content API

Handles content search and saved items.

#### `contentAPI.search(query, filters)`

Searches for content across all categories.

**Parameters:**
- `query` (string): Search query text
- `filters` (object, optional): Additional filters (category, tags, etc.)

**Returns:** Promise resolving to array of content items

**Example:**
```javascript
import { contentAPI } from '@/services/api';

// Basic search
const results = await contentAPI.search('jazz music');

// Search with filters
const filteredResults = await contentAPI.search('jazz', {
  category: 'music',
  minScore: 0.8
});
```

#### `contentAPI.save(itemId)`

Saves a content item to the user's collection.

**Parameters:**
- `itemId` (string): Content item ID

**Returns:** Promise resolving to success confirmation

**Example:**
```javascript
await contentAPI.save('content-789');
```

#### `contentAPI.getSaved()`

Retrieves all saved content for the current user.

**Returns:** Promise resolving to array of saved items

**Example:**
```javascript
const savedItems = await contentAPI.getSaved();
```

---

### Notifications API

Manages user notifications.

#### `notificationsAPI.getAll()`

Retrieves all notifications for the current user.

**Returns:** Promise resolving to array of notification objects

**Example:**
```javascript
import { notificationsAPI } from '@/services/api';

const notifications = await notificationsAPI.getAll();
```

**Response Format:**
```javascript
[
  {
    id: string,
    type: string,
    title: string,
    message: string,
    read: boolean,
    createdAt: number
  }
]
```

#### `notificationsAPI.markAsRead(notificationId)`

Marks a specific notification as read.

**Parameters:**
- `notificationId` (string): Notification ID

**Returns:** Promise resolving to success confirmation

**Example:**
```javascript
await notificationsAPI.markAsRead('notif-123');
```

#### `notificationsAPI.markAllAsRead()`

Marks all notifications as read.

**Returns:** Promise resolving to success confirmation

**Example:**
```javascript
await notificationsAPI.markAllAsRead();
```

---

## Error Handling

All API methods throw errors that should be caught and handled by the calling component:

```javascript
try {
  const data = await authAPI.login(email, password);
  // Handle success
} catch (error) {
  // error.message contains the error description
  console.error('API Error:', error.message);
  // Show error to user
}
```

### Common Error Scenarios

- **401 Unauthorized**: Token expired or invalid - redirect to login
- **403 Forbidden**: User lacks permission for the resource
- **404 Not Found**: Resource doesn't exist
- **500 Server Error**: Backend service error - show retry option
- **Network Error**: Connection failed - check internet connection

## Usage in Components

### React Component Example

```javascript
import { useState, useEffect } from 'react';
import { recommendationsAPI } from '@/services/api';

function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchRecommendations = async () => {
      try {
        setLoading(true);
        const data = await recommendationsAPI.getPersonalized();
        setRecommendations(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, []);

  if (loading) return <Loader />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      {recommendations.map(rec => (
        <RecommendationCard key={rec.id} {...rec} />
      ))}
    </div>
  );
}
```

### Custom Hook Example

```javascript
import { useState, useEffect } from 'react';
import { recommendationsAPI } from '@/services/api';

function useRecommendations(category = null) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const recommendations = await recommendationsAPI.getPersonalized(category);
        setData(recommendations);
        setError(null);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [category]);

  return { data, loading, error };
}

// Usage in component
function MyComponent() {
  const { data, loading, error } = useRecommendations('music');
  // ...
}
```

## Testing

### Mocking API Calls

For unit tests, mock the API service:

```javascript
import { vi } from 'vitest';
import * as api from '@/services/api';

vi.mock('@/services/api', () => ({
  authAPI: {
    login: vi.fn(),
    logout: vi.fn(),
  },
  recommendationsAPI: {
    getPersonalized: vi.fn(),
  },
}));

// In test
api.authAPI.login.mockResolvedValue({
  token: 'fake-token',
  user: { id: '1', email: 'test@example.com' }
});
```

## Environment Configuration

Set the API base URL in `.env`:

```bash
# Development
VITE_API_BASE_URL=http://localhost:8000

# Production
VITE_API_BASE_URL=https://api.vibegraph.com

# Docker
VITE_API_BASE_URL=http://backend-api:8000
```

## Future Enhancements

Planned improvements to the API service:

- [ ] Request caching with TTL
- [ ] Automatic retry with exponential backoff
- [ ] Request deduplication
- [ ] WebSocket support for real-time updates
- [ ] Optimistic updates for better UX
- [ ] Request cancellation for unmounted components
- [ ] TypeScript type definitions

## Related Documentation

- [Frontend README](../README.md)
- [Backend API Contracts](../../api/API_CONTRACTS.md)
- [Authentication Flow](../../backend/ARCHITECTURE.md#authentication)
- [Error Handling Guide](../ERROR_HANDLING.md)
