# Frontend Configuration

This document describes the environment variables and configuration options for the VibeGraph frontend application.

## Environment Variables

The frontend uses Vite's environment variable system, which requires all variables to be prefixed with `VITE_` to be exposed to the client-side code.

### Core Variables

#### `VITE_VIBEGRAPH_API_URL`

**Type**: String (URL)  
**Required**: Yes  
**Description**: The base URL for the VibeGraph backend API. All API requests are made relative to this URL.

**Values by Environment**:
- **Docker Development**: `http://backend-api:8000`
- **Local Development**: `http://localhost:8000`
- **Production**: `https://api.vibegraph.com` (or your production API domain)

**Usage Example**:
```javascript
// In frontend/src/services/vibeGraphAPI.js
const API_BASE_URL = import.meta.env.VITE_VIBEGRAPH_API_URL

const response = await fetch(`${API_BASE_URL}/quiz/section1/start`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
})
```

#### `VITE_ENV`

**Type**: String  
**Required**: No  
**Default**: `development`  
**Description**: Specifies the application environment for feature flags and conditional behavior.

**Valid Values**:
- `development` - Development mode with debug features enabled
- `staging` - Staging environment for pre-production testing
- `production` - Production mode with optimizations and analytics

#### `NODE_ENV`

**Type**: String  
**Required**: No  
**Default**: `development`  
**Description**: Standard Node.js environment variable used by build tools and dependencies.

**Valid Values**:
- `development` - Development build with source maps and hot reload
- `production` - Optimized production build with minification

## Configuration Files

### `.env.docker`

**Location**: `frontend/.env.docker`  
**Purpose**: Environment configuration for Docker containerized deployment  
**Used When**: Running the frontend in a Docker container via docker-compose

**Contents**:
```env
# API Base URL - Points to the backend API container
VITE_VIBEGRAPH_API_URL=http://backend-api:8000

# Environment
VITE_ENV=development

# Node Environment
NODE_ENV=development
```

**Key Points**:
- Uses Docker service name `backend-api` for internal container communication
- Docker's internal DNS resolves `backend-api` to the correct container IP
- Port 8000 is the internal port exposed by the backend-api container

### `.env.local` (Optional)

**Location**: `frontend/.env.local`  
**Purpose**: Local development overrides (not committed to git)  
**Used When**: Running the frontend locally with `npm run dev`

**Example Contents**:
```env
# For local development pointing to local backend
VITE_VIBEGRAPH_API_URL=http://localhost:8000

# Or pointing to Docker backend from host machine
# VITE_VIBEGRAPH_API_URL=http://localhost:8000

VITE_ENV=development
NODE_ENV=development
```

### `.env.production`

**Location**: `frontend/.env.production`  
**Purpose**: Production environment configuration  
**Used When**: Building for production deployment

**Example Contents**:
```env
VITE_VIBEGRAPH_API_URL=https://api.vibegraph.com
VITE_ENV=production
NODE_ENV=production
```

## Docker Configuration

### Container Networking

When running in Docker, the frontend container communicates with the backend-api container using Docker's internal network:

- **Network Name**: `vibegraph-network`
- **Frontend Container**: `vibegraph-frontend` (172.28.0.10)
- **Backend Container**: `vibegraph-backend-api` (172.28.0.20)
- **DNS Resolution**: Docker automatically resolves `backend-api` to `172.28.0.20`

### Environment Variable Injection

Environment variables are injected into the Docker container via docker-compose.yml:

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    environment:
      - VITE_VIBEGRAPH_API_URL=http://backend-api:8000
      - VITE_ENV=development
      - NODE_ENV=development
```

Alternatively, using an env_file:

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    env_file:
      - ./frontend/.env.docker
```

## Accessing Environment Variables

### In JavaScript/React Code

Environment variables are accessed using Vite's `import.meta.env` object:

```javascript
// Get API URL
const apiUrl = import.meta.env.VITE_VIBEGRAPH_API_URL

// Get environment
const environment = import.meta.env.VITE_ENV

// Check if production
const isProduction = import.meta.env.PROD

// Check if development
const isDevelopment = import.meta.env.DEV
```

### Built-in Vite Variables

Vite provides several built-in environment variables:

- `import.meta.env.MODE` - The mode the app is running in (development/production)
- `import.meta.env.BASE_URL` - The base URL the app is being served from
- `import.meta.env.PROD` - Boolean, true if running in production
- `import.meta.env.DEV` - Boolean, true if running in development
- `import.meta.env.SSR` - Boolean, true if running in server-side rendering

## Validation and Type Safety

### Runtime Validation

It's recommended to validate required environment variables at application startup:

```javascript
// frontend/src/config/env.js
const requiredEnvVars = ['VITE_VIBEGRAPH_API_URL']

requiredEnvVars.forEach((varName) => {
  if (!import.meta.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`)
  }
})

export const config = {
  apiUrl: import.meta.env.VITE_VIBEGRAPH_API_URL,
  environment: import.meta.env.VITE_ENV || 'development',
  isProduction: import.meta.env.PROD,
  isDevelopment: import.meta.env.DEV,
}
```

### TypeScript Support

For TypeScript projects, define environment variable types:

```typescript
// frontend/src/vite-env.d.ts
/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_VIBEGRAPH_API_URL: string
  readonly VITE_ENV: 'development' | 'staging' | 'production'
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
```

## Troubleshooting

### Variable Not Defined

**Problem**: Environment variable is undefined in the application

**Solutions**:
1. Ensure the variable is prefixed with `VITE_`
2. Restart the dev server after adding new variables
3. Check that the variable is defined in the correct .env file
4. Verify the .env file is in the correct location (frontend/ directory)

### Docker Container Can't Reach Backend

**Problem**: API requests fail with connection errors

**Solutions**:
1. Verify `VITE_VIBEGRAPH_API_URL` uses the service name `backend-api`, not `localhost`
2. Check that both containers are on the same Docker network
3. Ensure the backend-api container is running and healthy
4. Verify the port number matches the backend's exposed port (8000)

### CORS Errors

**Problem**: Browser blocks API requests due to CORS policy

**Solutions**:
1. Ensure the backend API has CORS configured to allow the frontend origin
2. In Docker, the backend should allow `http://frontend:3000` or `http://localhost:3000`
3. Check that the API URL is correct and accessible

### Build-Time vs Runtime Variables

**Problem**: Variables work in development but not in production build

**Explanation**: Vite injects environment variables at build time, not runtime. The values are baked into the JavaScript bundle.

**Solutions**:
1. Use different .env files for different environments
2. Set environment variables during the build process
3. For runtime configuration, consider using a config.json file loaded at startup

## Security Considerations

### Never Expose Secrets

**Important**: Never put sensitive information in environment variables prefixed with `VITE_`:

❌ **DO NOT**:
```env
VITE_API_SECRET_KEY=abc123  # This will be exposed in the client bundle!
VITE_DATABASE_PASSWORD=secret  # Never do this!
```

✅ **DO**:
```env
VITE_VIBEGRAPH_API_URL=http://backend-api:8000  # Public API URL is safe
```

### API Keys and Tokens

- Never store API keys or secrets in frontend environment variables
- Use backend-for-frontend (BFF) pattern for sensitive operations
- Store authentication tokens in secure httpOnly cookies or secure storage
- All sensitive operations should be performed by the backend API

## References

- [Vite Environment Variables Documentation](https://vitejs.dev/guide/env-and-mode.html)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [VibeGraph Backend Integration Design](../architecture/design.md)
- [Docker Networking Documentation](../infrastructure/networking.md)
