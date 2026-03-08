# Validation Checklist

This document provides a comprehensive checklist for validating the VibeGraph system after Docker build completion. Use this checklist to ensure all components are functioning correctly before deploying to production.

## Prerequisites

Before running validation tests, ensure:

- [ ] Docker Engine 20.10+ is installed
- [ ] Docker Compose 2.0+ is installed
- [ ] All containers are built: `make build`
- [ ] All containers are running: `make up`
- [ ] All containers report healthy status: `docker ps` shows "healthy" for all services

## 1. Container Health Validation

### 1.1 Container Status
- [ ] All containers are running: `docker ps`
- [ ] No containers are in "restarting" state
- [ ] All containers show "healthy" status (not "starting" or "unhealthy")
- [ ] Check container logs for errors: `make logs`

### 1.2 Health Endpoints
- [ ] Frontend health: `curl http://localhost:3000` returns 200
- [ ] Backend API health: `curl http://localhost:8000/health` returns 200
- [ ] Backend ready: `curl http://localhost:8000/health/ready` returns 200
- [ ] DynamoDB health: `curl http://localhost:8000/health/db` returns 200
- [ ] Bedrock health: `curl http://localhost:8000/health/bedrock` returns 200
- [ ] Cache health: `curl http://localhost:8000/health/cache` returns 200
- [ ] Status overview: `curl http://localhost:8000/health/status` returns comprehensive JSON

**Validation Script**: `scripts/test-health-endpoints.sh`

## 2. Inter-Container Communication

### 2.1 Network Connectivity
- [ ] Frontend can reach backend API
- [ ] Backend API can reach DynamoDB Local
- [ ] Backend API can reach LocalStack (Bedrock mock)
- [ ] DNS resolution works for all service names
- [ ] Network latency is acceptable (<100ms between services)

**Validation Script**: `scripts/test-inter-container.sh`

### 2.2 CORS Configuration
- [ ] Frontend requests include proper Origin header
- [ ] Backend returns Access-Control-Allow-Origin header
- [ ] Preflight OPTIONS requests succeed
- [ ] All HTTP methods are allowed (GET, POST, PUT, DELETE)

## 3. Database Validation

### 3.1 DynamoDB Tables
- [ ] Users table exists and is accessible
- [ ] Sessions table exists and is accessible
- [ ] EmbeddingCache table exists and is accessible
- [ ] Tables have correct schema (partition keys, attributes)
- [ ] Tables can be queried without errors

**Validation Command**: 
```bash
docker exec vibegraph-backend-api python -c "from src.services.dynamodb_client import DynamoDBClient; client = DynamoDBClient(); print(client.list_tables())"
```

### 3.2 Data Operations
- [ ] Can write to Users table
- [ ] Can read from Users table
- [ ] Can update Users table records
- [ ] Can scan Users table
- [ ] Cache operations work (get/put)

## 4. API Endpoint Validation

### 4.1 Quiz Endpoints
- [ ] POST /api/quiz/section1/start returns sessionId and questions
- [ ] POST /api/quiz/section2/generate accepts sessionId and returns adaptive questions
- [ ] POST /api/quiz/complete processes answers and returns tasteDNA
- [ ] All endpoints return proper JSON responses
- [ ] Error responses include descriptive messages

**Validation Script**: `scripts/test-api-endpoints.sh`

### 4.2 Profile Endpoints
- [ ] GET /api/profile/dna/:userId returns taste DNA profile
- [ ] GET /api/profile/path/:userId returns growth path
- [ ] GET /api/profile/matches/:userId returns taste matches
- [ ] GET /api/profile/analytics/:userId returns analytics data
- [ ] 404 errors returned for non-existent users

### 4.3 Error Handling
- [ ] Invalid requests return 400 with error message
- [ ] Missing authentication returns 401
- [ ] Unauthorized access returns 403
- [ ] Non-existent resources return 404
- [ ] Server errors return 500 with generic message (no stack traces)

## 5. AI Service Integration

### 5.1 Claude Integration (via LocalStack)
- [ ] Section 1 question generation works
- [ ] Section 2 adaptive question generation works
- [ ] DNA archetype generation works
- [ ] Growth path generation works
- [ ] Analytics generation works
- [ ] Responses are properly formatted JSON

### 5.2 Titan Embedding Integration (via LocalStack)
- [ ] Embedding generation returns 1024-dimensional vector
- [ ] Vectors are normalized (magnitude ≈ 1.0)
- [ ] All vector values are between -1 and 1
- [ ] Cache hit/miss logic works correctly

## 6. End-to-End Quiz Flow

### 6.1 Complete Quiz Journey
- [ ] User can start Section 1 and receive 5 questions
- [ ] User can submit Section 1 answers and receive Section 2 questions
- [ ] User can complete quiz and receive taste DNA profile
- [ ] Session persists across all phases
- [ ] All data is stored correctly in database
- [ ] No raw quiz answers are stored (privacy check)

**Validation Script**: `tests/integration/test_quiz_flow.py`

### 6.2 Profile Generation
- [ ] Taste DNA includes archetype, traits, categories, description
- [ ] Growth path includes absorb, create, reflect categories
- [ ] Each category has 3-5 recommendations
- [ ] Analytics include insights and recommendations

## 7. Frontend Integration

### 7.1 UI Functionality
- [ ] OnboardingPage loads without errors
- [ ] Section 1 questions display correctly
- [ ] User can select answers and proceed
- [ ] Section 2 questions display after Section 1 completion
- [ ] Loading states display during API calls
- [ ] TasteDNACard displays after quiz completion
- [ ] Error messages display for API failures

### 7.2 API Service Layer
- [ ] vibeGraphAPI service is properly configured
- [ ] API base URL points to backend container
- [ ] Authentication tokens are included in requests
- [ ] Error handling works correctly
- [ ] Retry logic functions for failed requests

## 8. Performance Validation

### 8.1 Response Times
- [ ] Health endpoints respond in <100ms
- [ ] Quiz endpoints respond in <2s
- [ ] Profile endpoints respond in <1s
- [ ] Embedding generation completes in <3s
- [ ] DNA generation completes in <5s

### 8.2 Resource Usage
- [ ] Container memory usage is reasonable (<512MB per container)
- [ ] CPU usage is acceptable (<50% under normal load)
- [ ] No memory leaks detected over 1-hour run
- [ ] Disk usage is stable (no unbounded log growth)

**Validation Command**: `docker stats`

## 9. Logging and Monitoring

### 9.1 Log Output
- [ ] All containers produce structured JSON logs
- [ ] Log levels are appropriate (INFO for normal, ERROR for failures)
- [ ] No sensitive data in logs (tokens, passwords, raw answers)
- [ ] Timestamps are included in all log entries
- [ ] Request IDs are tracked across services

### 9.2 Error Logging
- [ ] API errors are logged with context
- [ ] Stack traces are logged for server errors
- [ ] Connection failures are logged with retry attempts
- [ ] Health check failures are logged

**Validation Command**: `make logs | grep ERROR`

## 10. Security Validation

### 10.1 Data Privacy
- [ ] Raw quiz answers are NOT stored in database
- [ ] Only embedding vectors are persisted
- [ ] Sensitive data is not logged
- [ ] Authentication tokens are validated
- [ ] CORS is properly configured

### 10.2 Input Validation
- [ ] Invalid UUIDs are rejected
- [ ] Malformed JSON is rejected
- [ ] SQL injection attempts are blocked
- [ ] XSS attempts are sanitized
- [ ] Request size limits are enforced

## 11. Resilience Testing

### 11.1 Service Failure Recovery
- [ ] Backend recovers when DynamoDB is temporarily unavailable
- [ ] Backend recovers when Bedrock is temporarily unavailable
- [ ] Frontend displays error messages when backend is down
- [ ] Retry logic works for transient failures
- [ ] Health checks detect service failures

**Validation Script**: `scripts/test-resilience.sh`

### 11.2 Container Restart
- [ ] Containers restart automatically on failure
- [ ] Data persists after container restart
- [ ] Services reconnect after restart
- [ ] No data loss during restart

**Validation Command**: `docker restart vibegraph-backend-api && make wait-healthy`

## 12. Documentation Validation

### 12.1 Documentation Completeness
- [ ] README.md provides clear overview
- [ ] QUICKSTART.md has minimal setup steps
- [ ] DEPLOYMENT.md covers production deployment
- [ ] TROUBLESHOOTING.md addresses common issues
- [ ] API documentation is accurate and complete
- [ ] All code examples work as documented

### 12.2 Documentation Accuracy
- [ ] Port numbers match actual configuration
- [ ] Environment variables are documented
- [ ] Command examples execute successfully
- [ ] Links are not broken
- [ ] Screenshots/diagrams are up-to-date

## Validation Scripts Summary

Run all validation scripts in sequence:

```bash
# 1. Build and start containers
make clean
make build
make up
make wait-healthy

# 2. Run validation scripts
scripts/test-health-endpoints.sh
scripts/test-inter-container.sh
scripts/test-api-endpoints.sh
scripts/test-resilience.sh

# 3. Run integration tests
make test-integration

# 4. Monitor health
scripts/monitor-health.sh
```

## Sign-Off Checklist

Before marking validation complete:

- [ ] All validation scripts pass without errors
- [ ] All integration tests pass
- [ ] All containers remain healthy for 30+ minutes
- [ ] No critical errors in logs
- [ ] Documentation is reviewed and accurate
- [ ] Performance metrics are acceptable
- [ ] Security checks pass
- [ ] Team has reviewed and approved

## Post-Validation Actions

After successful validation:

1. Tag Docker images with version number
2. Update CHANGELOG.md with changes
3. Create release notes
4. Deploy to staging environment
5. Schedule production deployment

## Troubleshooting

If validation fails, see:
- `docs/TROUBLESHOOTING.md` for common issues
- `scripts/README.md` for script usage
- Container logs: `make logs-backend` or `make logs-frontend`
- Health status: `curl http://localhost:8000/health/status`

## Notes

- This checklist should be completed AFTER Docker build is complete
- Run validation in a clean environment (fresh containers)
- Some checks may require manual verification
- Automated scripts cover most validation points
- Document any deviations or issues encountered
