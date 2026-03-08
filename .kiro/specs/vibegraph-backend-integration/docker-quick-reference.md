# Docker Architecture Quick Reference

## Container Summary

| Container | Purpose | Port | IP Address | Dependencies |
|-----------|---------|------|------------|--------------|
| **frontend** | React app with Vite | 5173 | 172.28.0.10 | backend-api |
| **backend-api** | Lambda functions + API Gateway | 3000 | 172.28.0.20 | dynamodb-local, localstack, backend-services |
| **backend-services** | Bedrock mock (Claude + Titan) | 8080 (internal) | 172.28.0.30 | localstack |
| **dynamodb-local** | Local DynamoDB instance | 8000 | 172.28.0.40 | None |
| **localstack** | AWS services mock | 4566 | 172.28.0.50 | None |

## Quick Commands

### Start All Services
```bash
docker-compose -f docker-compose.dev.yml up --build
```

### Start Specific Service
```bash
docker-compose -f docker-compose.dev.yml up frontend
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend-api

# Last 100 lines
docker-compose logs --tail=100 backend-api
```

### Stop All Services
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

### Restart Service
```bash
docker-compose restart backend-api
```

### Execute Command in Container
```bash
docker-compose exec backend-api sh
docker-compose exec frontend npm run test
```

### Check Service Health
```bash
docker-compose ps
```

### View Resource Usage
```bash
docker stats
```

## Access Points

### Web Interfaces
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:3000
- **DynamoDB Admin**: http://localhost:8000
- **LocalStack Dashboard**: http://localhost:4566/_localstack/health

### API Endpoints
```bash
# Health check
curl http://localhost:3000/health

# Start Section 1
curl -X POST http://localhost:3000/quiz/section1/start \
  -H "Content-Type: application/json" \
  -d '{}'

# Generate Section 2
curl -X POST http://localhost:3000/quiz/section2/generate \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "...", "section1Answers": [...]}'

# Complete Quiz
curl -X POST http://localhost:3000/quiz/complete \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "...", "userId": "...", "allAnswers": {...}}'
```

### DynamoDB CLI
```bash
# List tables
aws dynamodb list-tables \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# Scan users table
aws dynamodb scan \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# Get item
aws dynamodb get-item \
  --table-name vibegraph-users \
  --key '{"userId": {"S": "..."}}' \
  --endpoint-url http://localhost:8000 \
  --region us-east-1
```

### LocalStack CLI
```bash
# List S3 buckets
awslocal s3 ls

# List secrets
awslocal secretsmanager list-secrets

# View CloudWatch logs
awslocal logs describe-log-groups
```

## Environment Variables

### Frontend (.env.development)
```env
VITE_VIBEGRAPH_API_URL=http://localhost:3000
VITE_ENV=development
NODE_ENV=development
```

### Backend API (.env.development)
```env
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=test
AWS_SECRET_ACCESS_KEY=test
DYNAMODB_ENDPOINT=http://dynamodb-local:8000
LOCALSTACK_ENDPOINT=http://localstack:4566
BEDROCK_ENDPOINT=http://backend-services:8080
SESSIONS_TABLE=vibegraph-sessions
USERS_TABLE=vibegraph-users
CACHE_TABLE=vibegraph-embedding-cache
JWT_SECRET=dev-secret-key-change-in-production
LOG_LEVEL=debug
NODE_ENV=development
```

## Volume Locations

### Named Volumes
```bash
# DynamoDB data
docker volume inspect vibegraph_dynamodb-data

# LocalStack data
docker volume inspect vibegraph_localstack-data

# Remove all volumes
docker volume rm vibegraph_dynamodb-data vibegraph_localstack-data
```

### Bind Mounts
- Frontend source: `./frontend` → `/app`
- Backend source: `./backend/src` → `/var/task/src`
- Infrastructure: `./backend/infrastructure` → `/var/task/infrastructure`
- Bedrock mocks: `./backend/mocks/bedrock` → `/app`

## Troubleshooting

### Container Won't Start
```bash
# Check logs
docker-compose logs [service-name]

# Check health status
docker-compose ps

# Rebuild container
docker-compose up --build --force-recreate [service-name]
```

### Port Already in Use
```bash
# Find process using port
lsof -i :5173
lsof -i :3000

# Kill process
kill -9 [PID]

# Or change port in docker-compose.yml
```

### Out of Memory
```bash
# Check Docker memory limit
docker info | grep Memory

# Increase Docker memory in Docker Desktop settings
# Or reduce container memory limits in docker-compose.yml
```

### Database Not Initialized
```bash
# Restart DynamoDB container
docker-compose restart dynamodb-local

# Manually run init script
docker-compose exec dynamodb-local sh
aws dynamodb create-table --cli-input-json file:///docker-entrypoint-initdb.d/usersTable.json --endpoint-url http://localhost:8000
```

### Cannot Connect to Backend
```bash
# Check backend health
curl http://localhost:3000/health

# Check network connectivity
docker-compose exec frontend ping backend-api

# Verify environment variable
docker-compose exec frontend env | grep VITE_VIBEGRAPH_API_URL
```

## Network Debugging

### Test Container Connectivity
```bash
# From frontend to backend-api
docker-compose exec frontend wget -O- http://backend-api:3000/health

# From backend-api to dynamodb-local
docker-compose exec backend-api curl http://dynamodb-local:8000

# From backend-api to localstack
docker-compose exec backend-api curl http://localstack:4566/_localstack/health
```

### Inspect Network
```bash
# View network details
docker network inspect vibegraph-network

# List containers on network
docker network inspect vibegraph-network | grep Name
```

## Data Management

### Backup DynamoDB Data
```bash
# Export users table
aws dynamodb scan \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8000 \
  --region us-east-1 > backup-users.json

# Export sessions table
aws dynamodb scan \
  --table-name vibegraph-sessions \
  --endpoint-url http://localhost:8000 \
  --region us-east-1 > backup-sessions.json

# Export cache table
aws dynamodb scan \
  --table-name vibegraph-embedding-cache \
  --endpoint-url http://localhost:8000 \
  --region us-east-1 > backup-cache.json
```

### Restore DynamoDB Data
```bash
# Import data (requires custom script)
node scripts/import-dynamodb.js backup-users.json vibegraph-users
```

### Clear All Data
```bash
# Stop containers and remove volumes
docker-compose down -v

# Restart with fresh data
docker-compose up --build
```

## Performance Monitoring

### View Resource Usage
```bash
# Real-time stats
docker stats

# Specific container
docker stats frontend

# Export stats to file
docker stats --no-stream > stats.txt
```

### Check Container Logs Size
```bash
# View log file size
docker inspect --format='{{.LogPath}}' vibegraph_frontend_1
ls -lh $(docker inspect --format='{{.LogPath}}' vibegraph_frontend_1)
```

### Prune Unused Resources
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

## Development Workflow

### Hot Reload Testing
1. Edit frontend file: `./frontend/src/App.jsx`
2. Browser auto-refreshes at http://localhost:5173
3. Edit backend file: `./backend/src/handlers/generateSection1.js`
4. Lambda function reloads automatically on next request

### Debug Backend Lambda
1. Attach debugger to port 9229
2. Set breakpoints in `./backend/src/handlers/*.js`
3. Trigger API call from frontend or curl
4. Debugger pauses at breakpoint

### Test API Endpoints
```bash
# Using curl
curl -X POST http://localhost:3000/quiz/section1/start \
  -H "Content-Type: application/json" \
  -d '{}'

# Using Postman
# Import collection from ./backend/postman/vibegraph.postman_collection.json

# Using AWS CLI
aws lambda invoke \
  --function-name generateSection1 \
  --endpoint-url http://localhost:3000 \
  --payload file://backend/events/section1.json \
  response.json
```

### View Database Contents
```bash
# Using AWS CLI
aws dynamodb scan \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8000 \
  --region us-east-1

# Using DynamoDB Admin (install globally)
npm install -g dynamodb-admin
DYNAMO_ENDPOINT=http://localhost:8000 dynamodb-admin
# Open http://localhost:8001
```

## CI/CD Integration

### Build for Production
```bash
# Build frontend
docker build -f frontend/Dockerfile.prod -t vibegraph-frontend:latest ./frontend

# Test production build locally
docker run -p 80:80 vibegraph-frontend:latest
```

### Run Tests in Containers
```bash
# Frontend tests
docker-compose exec frontend npm run test

# Backend tests
docker-compose exec backend-api npm run test

# Integration tests
docker-compose exec backend-api npm run test:integration
```

### Health Check All Services
```bash
#!/bin/bash
services=("frontend" "backend-api" "dynamodb-local" "localstack")
for service in "${services[@]}"; do
  status=$(docker-compose ps -q $service | xargs docker inspect -f '{{.State.Health.Status}}')
  echo "$service: $status"
done
```

## Security Notes

### Development Credentials
- AWS Access Key: `test`
- AWS Secret Key: `test`
- JWT Secret: `dev-secret-key-change-in-production`

**⚠️ NEVER use these in production!**

### Production Checklist
- [ ] Replace JWT_SECRET with secure random string
- [ ] Use AWS IAM roles instead of access keys
- [ ] Enable HTTPS/TLS for all endpoints
- [ ] Restrict CORS to production domain only
- [ ] Enable CloudWatch logging
- [ ] Set up AWS Secrets Manager for sensitive data
- [ ] Use AWS DynamoDB instead of DynamoDB Local
- [ ] Use AWS Bedrock instead of mocks
- [ ] Enable DynamoDB encryption at rest
- [ ] Implement rate limiting on API Gateway

## Resource Limits

### Default Limits
| Container | CPU Limit | Memory Limit | CPU Reserve | Memory Reserve |
|-----------|-----------|--------------|-------------|----------------|
| frontend | 1.0 | 1 GB | 0.5 | 512 MB |
| backend-api | 2.0 | 2 GB | 1.0 | 1 GB |
| backend-services | 1.0 | 1 GB | 0.5 | 512 MB |
| dynamodb-local | 0.5 | 512 MB | 0.25 | 256 MB |
| localstack | 1.0 | 1 GB | 0.5 | 512 MB |

### Adjust Limits
Edit `docker-compose.dev.yml`:
```yaml
services:
  backend-api:
    deploy:
      resources:
        limits:
          cpus: '3.0'  # Increase CPU
          memory: 4G   # Increase memory
```

## Common Issues & Solutions

| Issue | Symptom | Solution |
|-------|---------|----------|
| Port conflict | `Error: bind: address already in use` | Change port mapping or kill process using port |
| Out of memory | Container killed by OOM | Increase Docker memory limit or reduce container limits |
| Health check failing | Container repeatedly restarts | Check logs, verify dependencies are healthy |
| Cannot connect to service | `Connection refused` | Verify service is running, check network connectivity |
| Volume permission denied | `EACCES: permission denied` | Run `chmod -R 755` on bind mount directory |
| DynamoDB table not found | `ResourceNotFoundException` | Restart dynamodb-local, run init script manually |
| Bedrock mock 404 | `Model not found` | Check backend-services logs, verify mock data loaded |
| Frontend CORS error | `Access-Control-Allow-Origin` | Verify VITE_VIBEGRAPH_API_URL, check backend CORS config |

## Useful Docker Commands

```bash
# View all containers (including stopped)
docker ps -a

# Remove all stopped containers
docker container prune

# View all images
docker images

# Remove unused images
docker image prune -a

# View all volumes
docker volume ls

# Remove unused volumes
docker volume prune

# View all networks
docker network ls

# Inspect container
docker inspect [container-id]

# View container processes
docker top [container-id]

# Copy file from container
docker cp [container-id]:/path/to/file ./local/path

# Copy file to container
docker cp ./local/file [container-id]:/path/to/destination

# Export container filesystem
docker export [container-id] > container.tar

# Save image to tar
docker save vibegraph-frontend:latest > image.tar

# Load image from tar
docker load < image.tar
```

## Next Steps

After setting up the Docker architecture:

1. **Verify all services are running**: `docker-compose ps`
2. **Check health status**: All services should show "healthy"
3. **Test frontend**: Open http://localhost:5173
4. **Test backend API**: `curl http://localhost:3000/health`
5. **Test DynamoDB**: `aws dynamodb list-tables --endpoint-url http://localhost:8000`
6. **Test LocalStack**: `curl http://localhost:4566/_localstack/health`
7. **Run integration tests**: `docker-compose exec backend-api npm run test:integration`
8. **Start developing**: Edit files and see changes live!

## Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [AWS SAM Local](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-start-api.html)
- [LocalStack Documentation](https://docs.localstack.cloud/)
- [DynamoDB Local Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
- [Vite Documentation](https://vitejs.dev/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
