# Backend Scripts

This directory contains utility scripts for the VibeGraph backend.

## init-dynamodb.py

Initializes DynamoDB Local with the required tables for the VibeGraph application.

### Tables Created

1. **vibegraph-users** - User profiles, embeddings, DNA profiles, and growth paths
   - Primary Key: `userId` (String)
   - GSI: `embeddingId-index` for reverse lookups
   - No TTL (data persists indefinitely)

2. **vibegraph-sessions** - Quiz sessions with 1-hour expiration
   - Primary Key: `sessionId` (String)
   - Sessions expire after 1 hour (managed by application logic)
   - No DynamoDB TTL attribute configured

3. **vibegraph-embedding-cache** - Cached Titan embeddings
   - Primary Key: `docHash` (String - SHA-256 hash)
   - Reduces Titan API calls and costs
   - Target cache hit rate: 40%

### Usage

#### Automatic (Docker Container)

The script runs automatically when the DynamoDB Local container starts. No manual intervention required.

#### Manual Execution

```bash
# Set environment variables (optional)
export DYNAMODB_ENDPOINT=http://localhost:8000
export AWS_REGION=us-east-1
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test

# Run the script
python3 backend/scripts/init-dynamodb.py
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DYNAMODB_ENDPOINT` | `http://localhost:8000` | DynamoDB Local endpoint URL |
| `AWS_REGION` | `us-east-1` | AWS region |
| `AWS_ACCESS_KEY_ID` | `test` | AWS access key (fake for local) |
| `AWS_SECRET_ACCESS_KEY` | `test` | AWS secret key (fake for local) |
| `USERS_TABLE` | `vibegraph-users` | Users table name |
| `SESSIONS_TABLE` | `vibegraph-sessions` | Sessions table name |
| `CACHE_TABLE` | `vibegraph-embedding-cache` | Cache table name |

### Requirements

- Python 3.11+
- boto3 (AWS SDK for Python)

Install dependencies:
```bash
pip install boto3
```

### Features

- **Idempotent**: Safe to run multiple times - skips existing tables
- **Wait Logic**: Automatically waits for DynamoDB Local to be ready
- **Error Handling**: Graceful error handling with informative messages
- **Status Monitoring**: Waits for tables to become active before proceeding

### Exit Codes

- `0` - Success (all tables created or already exist)
- `1` - Failure (connection error, table creation error, etc.)

### Troubleshooting

**Connection Refused**
```
Failed to connect to DynamoDB after 30 attempts
```
- Ensure DynamoDB Local is running on port 8000
- Check `DYNAMODB_ENDPOINT` environment variable
- Verify Docker container is healthy

**Table Already Exists**
```
Table vibegraph-users already exists, skipping creation.
```
- This is normal behavior - the script is idempotent
- Tables are preserved across container restarts

**Permission Denied**
```
Error creating table: AccessDeniedException
```
- Check AWS credentials (should be `test`/`test` for local)
- Verify DynamoDB Local is running with correct permissions

### Schema Details

#### Users Table Schema

```python
{
    'userId': 'string',              # Primary key
    'username': 'string',
    'email': 'string',
    'createdAt': 'number',           # Unix timestamp
    'updatedAt': 'number',           # Unix timestamp
    'embeddingId': 'string',         # GSI key
    'vector': ['number'],            # 1024-dimensional array
    'dimension': 'number',           # Always 1024
    'quizVersion': 'string',         # e.g., "v1"
    'tasteDNA': {
        'archetype': 'string',
        'traits': [
            {
                'name': 'string',
                'score': 'number',
                'description': 'string'
            }
        ],
        'categories': [
            {
                'category': 'string',
                'preferences': ['string'],
                'intensity': 'number'
            }
        ],
        'description': 'string'
    },
    'growthPath': {
        'absorb': ['PathItem'],
        'create': ['PathItem'],
        'reflect': ['PathItem'],
        'generatedAt': 'number'
    },
    'analytics': {
        'passiveVsIntentionalRatio': 'number',
        'goalAlignment': 'number',
        'contentBalance': ['CategoryBalance'],
        'insights': ['Insight'],
        'recommendations': ['string'],
        'generatedAt': 'number'
    }
}
```

#### Sessions Table Schema

```python
{
    'sessionId': 'string',           # Primary key
    'userId': 'string',              # Optional
    'createdAt': 'number',           # Unix timestamp
    'expiresAt': 'number',           # createdAt + 3600 seconds
    'status': 'string',              # "section1_complete", "section2_complete", "quiz_complete"
    'section1Questions': ['Question'],
    'section1Answers': ['Answer'],
    'section2Questions': ['Question'],
    'section2Answers': ['Answer']
}
```

#### EmbeddingCache Table Schema

```python
{
    'docHash': 'string',             # Primary key (SHA-256)
    'vector': ['number'],            # 1024-dimensional array
    'createdAt': 'number',           # Unix timestamp
    'hitCount': 'number',            # Cache hit counter
    'lastAccessedAt': 'number'       # Unix timestamp
}
```

## Other Scripts

### deploy-backend.sh
Deploys the backend Lambda functions to AWS using SAM CLI.

### local-dev.sh
Starts the local development environment with Docker containers.

### restructure.sh
Utility script for reorganizing backend code structure.
