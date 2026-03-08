# Guide: Merge Main and Reapply Session Changes

## Quick Start

```bash
# 1. Pull latest from main and merge
git checkout main
git pull origin main
git checkout punyak
git merge main

# 2. Reapply all session changes
./reapply-session-changes.sh

# 3. Or manually follow CHANGES_TO_REAPPLY.md
```

## What Changed in This Session

### Summary
- ✅ Created backend API routes (quiz & profile endpoints)
- ✅ Fixed frontend API URL to point to backend
- ✅ Fixed Docker configuration issues (DynamoDB, LocalStack, healthchecks)
- ✅ Fixed backend utils directory structure
- ✅ Updated Dockerfile CMDs for handlers/services
- ✅ Created comprehensive documentation

### Files Created
1. `backend/api/routes/__init__.py`
2. `backend/api/routes/quiz.py`
3. `backend/api/routes/profile.py`
4. `SETUP.md`
5. `AWS_MIGRATION.md`
6. `DOCKER_INTEGRATION_COMPLETE.md`
7. `API_INTEGRATION_COMPLETE.md`
8. `CHANGES_TO_REAPPLY.md`
9. `reapply-session-changes.sh`
10. `MERGE_AND_REAPPLY_GUIDE.md` (this file)

### Files Modified
1. `frontend/src/services/vibeGraphAPI.js` - API URL fix
2. `docker-compose.yml` - DynamoDB, LocalStack, healthcheck fixes
3. `docker-compose.override.yml` - Volume and command fixes
4. `backend/api/startup.py` - Import path fix
5. `backend/handlers/Dockerfile` - CMD fix
6. `backend/services/Dockerfile` - CMD fix
7. `backend/src/utils/connection_check.py` - Moved from backend/utils/

## Step-by-Step Merge Process

### Step 1: Backup Current Work

```bash
# Create a backup branch
git checkout punyak
git branch punyak-backup-$(date +%Y%m%d)

# Or stash if you have uncommitted changes
git stash save "backup before merge"
```

### Step 2: Merge Main

```bash
# Get latest main
git checkout main
git pull origin main

# Merge into punyak
git checkout punyak
git merge main
```

**If conflicts occur:**
- Resolve them manually
- Keep your changes for files you modified
- Accept their changes for files you didn't touch
- Run `git add <resolved-files>` and `git merge --continue`

### Step 3: Reapply Session Changes

**Option A: Automated (Recommended)**
```bash
./reapply-session-changes.sh
```

**Option B: Manual**
Follow `CHANGES_TO_REAPPLY.md` step by step

### Step 4: Verify Everything Works

```bash
# Build containers
make build

# Start containers
make down
make up

# Wait for health
make wait-healthy

# Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/quiz/section1/start \
  -H "Content-Type: application/json" -d '{}'

# Test frontend
curl http://localhost:3000
open http://localhost:3000
```

### Step 5: Commit and Push

```bash
# Add all changes
git add .

# Commit
git commit -m "Merged main and reapplied session changes

- Added backend API routes (quiz & profile)
- Fixed frontend API URL configuration
- Fixed Docker configurations
- Updated backend utils structure
- Added comprehensive documentation"

# Push
git push origin punyak
```

## Verification Checklist

After reapplying changes, verify:

### Backend
- [ ] `backend/api/routes/quiz.py` exists
- [ ] `backend/api/routes/profile.py` exists
- [ ] `backend/api/routes/__init__.py` exists
- [ ] `backend/src/utils/connection_check.py` exists (not in backend/utils/)
- [ ] `backend/api/startup.py` imports from `src.utils.connection_check`
- [ ] `backend/handlers/Dockerfile` has `CMD ["tail", "-f", "/dev/null"]`
- [ ] `backend/services/Dockerfile` has `CMD ["tail", "-f", "/dev/null"]`

### Frontend
- [ ] `frontend/src/services/vibeGraphAPI.js` has `VITE_API_URL` and `http://localhost:8000`

### Docker
- [ ] `docker-compose.yml` has DynamoDB `-inMemory` command
- [ ] `docker-compose.yml` frontend healthcheck uses `127.0.0.1`
- [ ] `docker-compose.yml` LocalStack has no volume mounts
- [ ] `docker-compose.override.yml` has no volume bind mounts
- [ ] `docker-compose.override.yml` backend-api has `PYTHONPATH=/app`

### Documentation
- [ ] `SETUP.md` exists
- [ ] `AWS_MIGRATION.md` exists
- [ ] `DOCKER_INTEGRATION_COMPLETE.md` exists
- [ ] `API_INTEGRATION_COMPLETE.md` exists

### System
- [ ] All containers build: `make build`
- [ ] All containers start: `make up`
- [ ] Backend healthy: `curl http://localhost:8000/health`
- [ ] Quiz API works: `curl -X POST http://localhost:8000/quiz/section1/start -H "Content-Type: application/json" -d '{}'`
- [ ] Frontend loads: `curl http://localhost:3000`

## Troubleshooting

### Merge Conflicts

**If you get conflicts in:**

**`docker-compose.yml`:**
- Keep your DynamoDB command: `-inMemory`
- Keep your frontend healthcheck: `127.0.0.1`
- Remove LocalStack volume mounts

**`frontend/src/services/vibeGraphAPI.js`:**
- Keep your API_BASE_URL: `http://localhost:8000`

**`backend/api/main.py`:**
- Keep both route imports if they added routes too
- Merge route registrations

### Build Failures

**"Module not found: utils.connection_check":**
```bash
# Check file location
ls backend/src/utils/connection_check.py

# Check import in startup.py
grep "from src.utils.connection_check" backend/api/startup.py
```

**"DynamoDB tables not found":**
```bash
# Run init container
docker-compose up dynamodb-init

# Check logs
docker logs vibegraph-dynamodb-init
```

**"Container unhealthy":**
```bash
# Check logs
docker logs vibegraph-backend-api

# Check health endpoint
curl http://localhost:8000/health/ready
```

### Runtime Issues

**"CORS error in browser":**
- Check `backend/api/main.py` has `http://localhost:3000` in `allow_origins`

**"API returns 404":**
- Check routes are registered in `backend/api/main.py`
- Check route files exist in `backend/api/routes/`

**"Frontend can't reach backend":**
- Check `frontend/src/services/vibeGraphAPI.js` has correct URL
- Check backend container is healthy: `docker ps`

## Files Reference

### Critical Files to Check After Merge

1. **backend/api/routes/quiz.py** - Quiz endpoints
2. **backend/api/routes/profile.py** - Profile endpoints
3. **frontend/src/services/vibeGraphAPI.js** - API URL
4. **docker-compose.yml** - Container config
5. **docker-compose.override.yml** - Dev overrides
6. **backend/api/startup.py** - Import paths
7. **backend/src/utils/connection_check.py** - Utils location

### Documentation Files

1. **SETUP.md** - Development setup guide
2. **AWS_MIGRATION.md** - Production deployment
3. **DOCKER_INTEGRATION_COMPLETE.md** - Docker implementation
4. **API_INTEGRATION_COMPLETE.md** - API integration
5. **CHANGES_TO_REAPPLY.md** - Detailed change list

## Quick Commands

```bash
# Full rebuild
make clean && make build && make up

# Check status
docker ps
make logs

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/docs

# Test frontend
open http://localhost:3000

# Debug
docker logs vibegraph-backend-api
docker logs vibegraph-frontend
docker exec -it vibegraph-backend-api bash
```

## Support

If you encounter issues:
1. Check `CHANGES_TO_REAPPLY.md` for exact changes
2. Check `TROUBLESHOOTING` section in `SETUP.md`
3. Review Docker logs: `make logs`
4. Verify file locations match the checklist above

## Summary

This session added:
- ✅ Complete backend API (mock data, ready for real implementation)
- ✅ Frontend-backend integration
- ✅ Fixed Docker configuration
- ✅ Comprehensive documentation
- ✅ Test and deployment guides

The system is now fully integrated and ready for:
1. Local development and testing
2. Real business logic implementation (Tasks 11-13)
3. Production deployment to AWS

All changes are documented and can be reapplied after merging main.
