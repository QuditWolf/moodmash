# Docker Architecture Diagrams

## System Overview Diagram

```mermaid
graph TB
    subgraph "Host Machine"
        BROWSER[Web Browser]
        CLI[AWS CLI / Postman]
    end
    
    subgraph "Docker Environment - vibegraph-network (172.28.0.0/16)"
        subgraph "Frontend Container (172.28.0.10)"
            VITE[Vite Dev Server<br/>:5173]
            REACT[React Application]
            VITE --> REACT
        end
        
        subgraph "Backend API Container (172.28.0.20)"
            APIGW[API Gateway Emulator<br/>:3000]
            LAMBDA_RUNTIME[Lambda Runtime<br/>Node.js 18]
            HANDLERS[Lambda Handlers<br/>- generateSection1<br/>- generateSection2<br/>- generateEmbedding<br/>- generateDNA<br/>- generatePath<br/>- findMatches<br/>- generateAnalytics]
            APIGW --> LAMBDA_RUNTIME
            LAMBDA_RUNTIME --> HANDLERS
        end
        
        subgraph "Backend Services Container (172.28.0.30)"
            BEDROCK_MOCK[Bedrock Mock API<br/>:8080]
            CLAUDE_MOCK[Claude 3.5 Sonnet Mock]
            TITAN_MOCK[Titan v2 Embeddings Mock]
            BEDROCK_MOCK --> CLAUDE_MOCK
            BEDROCK_MOCK --> TITAN_MOCK
        end
        
        subgraph "DynamoDB Local Container (172.28.0.40)"
            DYNAMODB[DynamoDB Local<br/>:8000]
            USERS_TABLE[(Users Table)]
            SESSIONS_TABLE[(Sessions Table)]
            CACHE_TABLE[(Embedding Cache)]
            DYNAMODB --> USERS_TABLE
            DYNAMODB --> SESSIONS_TABLE
            DYNAMODB --> CACHE_TABLE
        end
        
        subgraph "LocalStack Container (172.28.0.50)"
            LOCALSTACK_GW[LocalStack Gateway<br/>:4566]
            S3_MOCK[S3 Mock]
            CW_MOCK[CloudWatch Mock]
            SECRETS_MOCK[Secrets Manager Mock]
            LOCALSTACK_GW --> S3_MOCK
            LOCALSTACK_GW --> CW_MOCK
            LOCALSTACK_GW --> SECRETS_MOCK
        end
    end
    
    subgraph "Persistent Storage"
        VOL_DYNAMODB[dynamodb-data<br/>Named Volume]
        VOL_LOCALSTACK[localstack-data<br/>Named Volume]
        BIND_FRONTEND[./frontend<br/>Bind Mount]
        BIND_BACKEND[./backend/src<br/>Bind Mount]
    end
    
    BROWSER -->|http://localhost:5173| VITE
    CLI -->|http://localhost:3000| APIGW
    CLI -->|http://localhost:8000| DYNAMODB
    
    REACT -->|API Calls| APIGW
    HANDLERS -->|Bedrock SDK| BEDROCK_MOCK
    HANDLERS -->|DynamoDB SDK| DYNAMODB
    HANDLERS -->|AWS SDK| LOCALSTACK_GW
    BEDROCK_MOCK -->|Store Mocks| S3_MOCK
    
    DYNAMODB -.->|Persist| VOL_DYNAMODB
    LOCALSTACK_GW -.->|Persist| VOL_LOCALSTACK
    VITE -.->|Hot Reload| BIND_FRONTEND
    HANDLERS -.->|Hot Reload| BIND_BACKEND
    
    style BROWSER fill:#e1f5ff
    style CLI fill:#e1f5ff
    style VITE fill:#61dafb
    style REACT fill:#61dafb
    style APIGW fill:#ff9900
    style LAMBDA_RUNTIME fill:#ff9900
    style HANDLERS fill:#ff9900
    style BEDROCK_MOCK fill:#ff6b6b
    style CLAUDE_MOCK fill:#ff6b6b
    style TITAN_MOCK fill:#ff6b6b
    style DYNAMODB fill:#4053d6
    style USERS_TABLE fill:#4053d6
    style SESSIONS_TABLE fill:#4053d6
    style CACHE_TABLE fill:#4053d6
    style LOCALSTACK_GW fill:#00c7b7
    style S3_MOCK fill:#00c7b7
    style CW_MOCK fill:#00c7b7
    style SECRETS_MOCK fill:#00c7b7
```

## Container Startup Sequence

```mermaid
sequenceDiagram
    participant Docker as Docker Compose
    participant DDB as DynamoDB Local
    participant LS as LocalStack
    participant BS as Backend Services
    participant API as Backend API
    participant FE as Frontend
    
    Note over Docker: Phase 1: Base Services
    Docker->>DDB: Start container
    Docker->>LS: Start container
    
    DDB->>DDB: Initialize DynamoDB
    DDB->>DDB: Create tables
    DDB->>Docker: Health check PASS
    
    LS->>LS: Initialize LocalStack
    LS->>LS: Start S3, CloudWatch, Secrets
    LS->>Docker: Health check PASS
    
    Note over Docker: Phase 2: Backend Services
    Docker->>BS: Start container (depends on LS)
    BS->>BS: Load Bedrock mocks
    BS->>LS: Store mock responses in S3
    BS->>Docker: Health check PASS
    
    Note over Docker: Phase 3: API Layer
    Docker->>API: Start container (depends on DDB, LS, BS)
    API->>API: Initialize Lambda runtime
    API->>DDB: Test connection
    API->>LS: Test connection
    API->>BS: Test connection
    API->>Docker: Health check PASS
    
    Note over Docker: Phase 4: Frontend
    Docker->>FE: Start container (depends on API)
    FE->>FE: Start Vite dev server
    FE->>API: Test connection
    FE->>Docker: Health check PASS
    
    Note over Docker: All services ready
```

## Data Flow: Quiz Completion

```mermaid
sequenceDiagram
    participant Browser
    participant Frontend as Frontend Container
    participant API as Backend API Container
    participant Bedrock as Backend Services Container
    participant DDB as DynamoDB Local Container
    participant LS as LocalStack Container
    
    Browser->>Frontend: Submit quiz answers
    Frontend->>API: POST /quiz/complete
    
    API->>DDB: Retrieve session
    DDB-->>API: Session data
    
    API->>Bedrock: Generate embedding (Titan)
    Bedrock->>Bedrock: Check mock cache
    Bedrock-->>API: 1024-dim vector
    
    API->>API: Normalize vector
    API->>DDB: Store embedding in Users table
    API->>DDB: Store in Embedding Cache
    
    API->>Bedrock: Generate DNA (Claude)
    Bedrock->>LS: Retrieve mock response from S3
    LS-->>Bedrock: Mock DNA data
    Bedrock-->>API: DNA profile
    
    API->>DDB: Store DNA in Users table
    API->>LS: Log to CloudWatch
    
    API-->>Frontend: Complete profile response
    Frontend-->>Browser: Display TasteDNACard
```

## Volume Mount Strategy

```mermaid
graph LR
    subgraph "Host File System"
        HOST_FE[./frontend/]
        HOST_BE[./backend/src/]
        HOST_INFRA[./backend/infrastructure/]
        HOST_MOCKS[./backend/mocks/]
    end
    
    subgraph "Frontend Container"
        CONT_FE[/app/]
        CONT_FE_NM[/app/node_modules/<br/>Anonymous Volume]
    end
    
    subgraph "Backend API Container"
        CONT_BE[/var/task/src/]
        CONT_BE_NM[/var/task/node_modules/<br/>Anonymous Volume]
        CONT_INFRA[/var/task/infrastructure/<br/>Read-Only]
    end
    
    subgraph "Backend Services Container"
        CONT_MOCKS[/app/]
    end
    
    subgraph "DynamoDB Local Container"
        CONT_DDB[/data/]
    end
    
    subgraph "LocalStack Container"
        CONT_LS[/tmp/localstack/]
    end
    
    subgraph "Docker Volumes"
        VOL_DDB[dynamodb-data]
        VOL_LS[localstack-data]
    end
    
    HOST_FE -.->|Bind Mount<br/>Read-Write| CONT_FE
    HOST_BE -.->|Bind Mount<br/>Read-Write| CONT_BE
    HOST_INFRA -.->|Bind Mount<br/>Read-Only| CONT_INFRA
    HOST_MOCKS -.->|Bind Mount<br/>Read-Write| CONT_MOCKS
    
    VOL_DDB -.->|Named Volume<br/>Persistent| CONT_DDB
    VOL_LS -.->|Named Volume<br/>Persistent| CONT_LS
    
    style HOST_FE fill:#e1f5ff
    style HOST_BE fill:#e1f5ff
    style HOST_INFRA fill:#e1f5ff
    style HOST_MOCKS fill:#e1f5ff
    style CONT_FE fill:#61dafb
    style CONT_BE fill:#ff9900
    style CONT_MOCKS fill:#ff6b6b
    style CONT_DDB fill:#4053d6
    style CONT_LS fill:#00c7b7
    style VOL_DDB fill:#ffd700
    style VOL_LS fill:#ffd700
```

## Network Communication Matrix

```mermaid
graph TD
    subgraph "Communication Paths"
        FE[Frontend<br/>172.28.0.10:5173]
        API[Backend API<br/>172.28.0.20:3000]
        BS[Backend Services<br/>172.28.0.30:8080]
        DDB[DynamoDB Local<br/>172.28.0.40:8000]
        LS[LocalStack<br/>172.28.0.50:4566]
    end
    
    FE -->|HTTP REST API| API
    API -->|AWS Bedrock SDK| BS
    API -->|AWS DynamoDB SDK| DDB
    API -->|AWS SDK<br/>S3, CloudWatch, Secrets| LS
    BS -->|AWS S3 SDK<br/>Store mock responses| LS
    
    style FE fill:#61dafb
    style API fill:#ff9900
    style BS fill:#ff6b6b
    style DDB fill:#4053d6
    style LS fill:#00c7b7
```

## Resource Allocation Visualization

```mermaid
pie title CPU Allocation (Total: 5.5 cores)
    "Backend API" : 2.0
    "Frontend" : 1.0
    "Backend Services" : 1.0
    "LocalStack" : 1.0
    "DynamoDB Local" : 0.5
```

```mermaid
pie title Memory Allocation (Total: 5.5 GB)
    "Backend API" : 2048
    "Frontend" : 1024
    "Backend Services" : 1024
    "LocalStack" : 1024
    "DynamoDB Local" : 512
```

## Container Health Check Flow

```mermaid
stateDiagram-v2
    [*] --> Starting: Container starts
    Starting --> Initializing: Start period begins
    Initializing --> HealthCheck: Start period ends
    
    HealthCheck --> Healthy: Check passes
    HealthCheck --> Unhealthy: Check fails
    
    Unhealthy --> HealthCheck: Retry (max 5 times)
    Unhealthy --> Failed: Max retries exceeded
    
    Healthy --> HealthCheck: Periodic check (every 10s)
    Healthy --> Unhealthy: Check fails
    
    Failed --> Restarting: Auto-restart policy
    Restarting --> Starting: Container restarts
    
    Failed --> [*]: Max restarts exceeded
```

## Development vs Production Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        DEV_FE[Frontend Container<br/>Vite Dev Server<br/>Hot Reload]
        DEV_API[Backend API Container<br/>SAM Local<br/>Lambda Emulation]
        DEV_BS[Backend Services<br/>Bedrock Mocks]
        DEV_DDB[DynamoDB Local]
        DEV_LS[LocalStack]
        
        DEV_FE --> DEV_API
        DEV_API --> DEV_BS
        DEV_API --> DEV_DDB
        DEV_API --> DEV_LS
    end
    
    subgraph "Production Environment"
        PROD_FE[Frontend Container<br/>Nginx<br/>Static Files]
        PROD_CF[CloudFront CDN]
        PROD_LAMBDA[AWS Lambda<br/>Real Functions]
        PROD_BEDROCK[AWS Bedrock<br/>Claude + Titan]
        PROD_DDB[AWS DynamoDB]
        PROD_CW[AWS CloudWatch]
        
        PROD_CF --> PROD_FE
        PROD_FE --> PROD_LAMBDA
        PROD_LAMBDA --> PROD_BEDROCK
        PROD_LAMBDA --> PROD_DDB
        PROD_LAMBDA --> PROD_CW
    end
    
    style DEV_FE fill:#61dafb
    style DEV_API fill:#ff9900
    style DEV_BS fill:#ff6b6b
    style DEV_DDB fill:#4053d6
    style DEV_LS fill:#00c7b7
    
    style PROD_FE fill:#61dafb
    style PROD_CF fill:#ff9900
    style PROD_LAMBDA fill:#ff9900
    style PROD_BEDROCK fill:#ff6b6b
    style PROD_DDB fill:#4053d6
    style PROD_CW fill:#00c7b7
```

## Container Dependency Tree

```mermaid
graph TD
    ROOT[docker-compose up]
    
    ROOT --> DDB[dynamodb-local<br/>No dependencies]
    ROOT --> LS[localstack<br/>No dependencies]
    
    DDB --> DDB_HEALTH{Health Check}
    LS --> LS_HEALTH{Health Check}
    
    DDB_HEALTH -->|Pass| BS_START[Start backend-services]
    LS_HEALTH -->|Pass| BS_START
    
    BS_START --> BS[backend-services<br/>Depends: localstack]
    BS --> BS_HEALTH{Health Check}
    
    DDB_HEALTH -->|Pass| API_START[Start backend-api]
    LS_HEALTH -->|Pass| API_START
    BS_HEALTH -->|Pass| API_START
    
    API_START --> API[backend-api<br/>Depends: dynamodb-local,<br/>localstack, backend-services]
    API --> API_HEALTH{Health Check}
    
    API_HEALTH -->|Pass| FE_START[Start frontend]
    FE_START --> FE[frontend<br/>Depends: backend-api]
    FE --> FE_HEALTH{Health Check}
    
    FE_HEALTH -->|Pass| READY[All Services Ready]
    
    DDB_HEALTH -->|Fail| RETRY1[Retry]
    LS_HEALTH -->|Fail| RETRY2[Retry]
    BS_HEALTH -->|Fail| RETRY3[Retry]
    API_HEALTH -->|Fail| RETRY4[Retry]
    FE_HEALTH -->|Fail| RETRY5[Retry]
    
    RETRY1 --> DDB_HEALTH
    RETRY2 --> LS_HEALTH
    RETRY3 --> BS_HEALTH
    RETRY4 --> API_HEALTH
    RETRY5 --> FE_HEALTH
    
    style ROOT fill:#e1f5ff
    style DDB fill:#4053d6
    style LS fill:#00c7b7
    style BS fill:#ff6b6b
    style API fill:#ff9900
    style FE fill:#61dafb
    style READY fill:#90ee90
```

## Port Mapping Overview

```mermaid
graph LR
    subgraph "Host Machine"
        HOST_5173[localhost:5173]
        HOST_3000[localhost:3000]
        HOST_8000[localhost:8000]
        HOST_4566[localhost:4566]
        HOST_9229[localhost:9229]
    end
    
    subgraph "Docker Network"
        CONT_FE[frontend:5173<br/>Vite Dev Server]
        CONT_API[backend-api:3000<br/>API Gateway]
        CONT_DDB[dynamodb-local:8000<br/>DynamoDB API]
        CONT_LS[localstack:4566<br/>LocalStack Gateway]
        CONT_DEBUG[backend-api:9229<br/>Node.js Debugger]
        CONT_BS[backend-services:8080<br/>Bedrock Mock<br/>Internal Only]
    end
    
    HOST_5173 -.->|Port Mapping| CONT_FE
    HOST_3000 -.->|Port Mapping| CONT_API
    HOST_8000 -.->|Port Mapping| CONT_DDB
    HOST_4566 -.->|Port Mapping| CONT_LS
    HOST_9229 -.->|Port Mapping| CONT_DEBUG
    
    style HOST_5173 fill:#e1f5ff
    style HOST_3000 fill:#e1f5ff
    style HOST_8000 fill:#e1f5ff
    style HOST_4566 fill:#e1f5ff
    style HOST_9229 fill:#e1f5ff
    style CONT_FE fill:#61dafb
    style CONT_API fill:#ff9900
    style CONT_DDB fill:#4053d6
    style CONT_LS fill:#00c7b7
    style CONT_DEBUG fill:#ff9900
    style CONT_BS fill:#ff6b6b
```

## Legend

### Container Colors
- 🔵 **Blue (#61dafb)**: Frontend (React/Vite)
- 🟠 **Orange (#ff9900)**: Backend API (Lambda/API Gateway)
- 🔴 **Red (#ff6b6b)**: Backend Services (Bedrock Mocks)
- 🟣 **Purple (#4053d6)**: Database (DynamoDB)
- 🟢 **Teal (#00c7b7)**: AWS Services (LocalStack)
- 🟡 **Yellow (#ffd700)**: Persistent Storage (Volumes)
- ⚪ **Light Blue (#e1f5ff)**: External (Host/Browser)

### Connection Types
- **Solid Arrow (→)**: Direct communication
- **Dotted Arrow (-.->)**: Volume mount or persistence
- **Dashed Line (---)**: Dependency relationship
