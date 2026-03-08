# Quick Reapply Commands

## One-Line Quick Start

```bash
git checkout main && git pull origin main && git checkout punyak && git merge main && bash reapply-session-changes.sh
```

---

## Step-by-Step Commands

### 1. Save Current Work
```bash
git stash
```

### 2. Pull Latest from Main
```bash
git checkout main
git pull origin main
```

### 3. Merge into Your Branch
```bash
git checkout punyak
git merge main
```

### 4. Resolve Conflicts (if any)
```bash
# Edit conflicted files
git add .
git commit -m "Merge main into punyak"
```

### 5. Reapply Session Changes
```bash
# Automated (recommended)
bash reapply-session-changes.sh

# OR Manual
# Follow CHANGES_TO_REAPPLY.md
```

### 6. Verify Changes
```bash
# Check route files exist
ls -la backend/api/routes/

# Check frontend API URL
grep "VITE_API_URL" frontend/src/services/vibeGraphAPI.js

# Check utils location
ls -la backend/src/utils/connection_check.py
```

### 7. Build and Test
```bash
# Clean and rebuild
make clean
make build

# Start containers
make up

# Wait for health
make wait-healthy

# Check status
docker ps

# Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/quiz/section1/start -H "Content-Type: application/json" -d '{}'

# Test frontend
curl http://localhost:3000
```

### 8. Commit Reapplied Changes
```bash
git add .
git commit -m "Reapplied session changes: backend API routes and Docker fixes"
git push origin punyak
```

---

## Quick Troubleshooting Commands

### Container Issues
```bash
# Check logs
docker logs vibegraph-backend-api
docker logs vibegraph-frontend
docker logs vibegraph-dynamodb-init

# Restart specific container
docker-compose restart backend-api

# Rebuild specific container
docker-compose build backend-api
docker-compose up -d backend-api
```

### DynamoDB Issues
```bash
# Run init container
docker-compose up -d dynamodb-init

# Check tables
docker exec vibegraph-backend-api python3 -c "
import boto3
dynamodb = boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000', region_name='us-east-1')
print(dynamodb.list_tables()['TableNames'])
"
```

### Network Issues
```bash
# Check network
docker network inspect vibegraph-network

# Test inter-container communication
docker exec vibegraph-backend-api curl http://dynamodb-local:8000
docker exec vibegraph-backend-api curl http://localstack:4566/_localstack/health
```

### API Issues
```bash
# Check API health
curl http://localhost:8000/health
curl http://localhost:8000/health/ready

# Check API docs
open http://localhost:8000/docs

# Test quiz endpoint
curl -X POST http://localhost:8000/quiz/section1/start \
  -H "Content-Type: application/json" \
  -d '{}' | python3 -m json.tool

# Test profile endpoint
curl http://localhost:8000/profile/dna/test-user-123 | python3 -m json.tool
```

### Frontend Issues
```bash
# Check frontend
curl http://localhost:3000

# Check API URL in built files
docker exec vibegraph-frontend grep -r "localhost:8000" /usr/share/nginx/html/

# Rebuild frontend
docker-compose build frontend
docker-compose up -d frontend
```

---

## Emergency Reset

If everything is broken:

```bash
# Nuclear option - start fresh
make clean
docker system prune -af
docker volume prune -f

# Rebuild everything
make build
make up
make wait-healthy

# Verify
docker ps
curl http://localhost:8000/health
curl http://localhost:3000
```

---

## Verification One-Liners

```bash
# All containers healthy?
docker ps --format "{{.Names}}: {{.Status}}" | grep vibegraph

# Backend API working?
curl -s http://localhost:8000/health | grep -q "healthy" && echo "✅ OK" || echo "❌ FAIL"

# Quiz API working?
curl -s -X POST http://localhost:8000/quiz/section1/start -H "Content-Type: application/json" -d '{}' | grep -q "sessionId" && echo "✅ OK" || echo "❌ FAIL"

# Frontend serving?
curl -s http://localhost:3000 | grep -q "VibeGraph" && echo "✅ OK" || echo "❌ FAIL"

# DynamoDB tables exist?
docker exec vibegraph-backend-api python3 -c "import boto3; print(boto3.client('dynamodb', endpoint_url='http://dynamodb-local:8000', region_name='us-east-1').list_tables()['TableNames'])"
```

---

## File Locations Quick Reference

### Created Files:
- `backend/api/routes/__init__.py`
- `backend/api/routes/quiz.py`
- `backend/api/routes/profile.py`

### Modified Files:
- `frontend/src/services/vibeGraphAPI.js` (line ~10)
- `docker-compose.yml` (multiple sections)
- `docker-compose.override.yml` (multiple sections)
- `backend/api/startup.py` (import line)
- `backend/handlers/Dockerfile` (CMD line)
- `backend/services/Dockerfile` (CMD line)

### Moved Files:
- `backend/utils/connection_check.py` → `backend/src/utils/connection_check.py`

---

## Documentation Quick Access

```bash
# View all documentation
ls -la *.md

# Read specific docs
cat REAPPLY_INSTRUCTIONS.md
cat CHANGES_TO_REAPPLY.md
cat SESSION_CHANGES_SUMMARY.md
cat API_INTEGRATION_COMPLETE.md
```

---

## Makefile Commands

```bash
make build          # Build all images
make up             # Start all containers
make down           # Stop all containers
make restart        # Restart all containers
make logs           # View all logs
make logs-backend   # View backend logs only
make logs-frontend  # View frontend logs only
make clean          # Remove all containers and volumes
make wait-healthy   # Wait for all containers to be healthy
make ps             # Show container status
```

---

## Success Indicators

After reapplication, you should see:

```
✅ backend/api/routes/quiz.py exists
✅ backend/api/routes/profile.py exists
✅ frontend/src/services/vibeGraphAPI.js has VITE_API_URL
✅ backend/src/utils/connection_check.py exists
✅ All containers running and healthy
✅ curl http://localhost:8000/health returns {"status":"healthy"}
✅ curl http://localhost:3000 returns HTML with "VibeGraph"
✅ POST /quiz/section1/start returns sessionId
```

---

## Need Help?

1. **Check documentation**: `CHANGES_TO_REAPPLY.md` has full code
2. **Check logs**: `docker logs <container-name>`
3. **Check status**: `docker ps`
4. **Check network**: `docker network inspect vibegraph-network`
5. **Start fresh**: `make clean && make build && make up`
