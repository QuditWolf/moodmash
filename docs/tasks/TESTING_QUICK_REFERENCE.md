# Container Testing Quick Reference

Quick reference for running container orchestration tests.

## Run All Tests

```bash
./scripts/run-all-tests.sh
```

## Individual Tests

```bash
# 1. Build validation
./scripts/test-build.sh

# 2. Container startup
./scripts/test-startup.sh

# 3. Health endpoints
./scripts/test-health-endpoints.sh

# 4. Inter-container communication
./scripts/test-inter-container.sh

# 5. Connection resilience
./scripts/test-resilience.sh

# 6. API endpoints
./scripts/test-api-endpoints.sh
```

## Health Monitoring

```bash
# Start monitoring dashboard
./scripts/monitor-health.sh

# Or via Makefile
make monitor
```

## Common Commands

```bash
# Build all images
make build

# Start containers
make up

# Stop containers
make down

# View logs
make logs
make logs-backend
make logs-frontend

# Check health
make health

# Run diagnostics
make diagnose

# Check connections
make check-connections
```

## Test Sequence

1. **Build** → Validates images build correctly
2. **Startup** → Validates containers start and become healthy
3. **Health** → Validates health endpoints work
4. **Communication** → Validates inter-container networking
5. **Resilience** → Validates failure handling
6. **API** → Validates API endpoints are accessible

## Expected Results

✓ All tests pass = System is working correctly
✗ Some tests fail = Check logs and diagnostics

## Troubleshooting

```bash
# View container status
docker-compose ps

# View logs
make logs

# Run diagnostics
make diagnose

# Restart everything
make restart

# Reset everything
make reset
```

## Test Duration

- Build validation: 5-10 min (first), 30s (cached)
- Container startup: 2-3 min
- Health endpoints: 1-2 min
- Inter-container: 1 min
- Resilience: 3-4 min
- API endpoints: 1 min
- **Total**: ~15-20 minutes

## Log Files

- `logs/health-monitor.log` - Health check history
- `logs/health-alerts.log` - Status change alerts

## Documentation

- Full guide: `docs/infrastructure/testing.md`
- Test scripts: `scripts/README.md`
- Docker setup: `docs/infrastructure/docker-setup.md`
- Troubleshooting: `docs/TROUBLESHOOTING.md`

## Support

For issues:
1. Check logs: `make logs`
2. Run diagnostics: `make diagnose`
3. Review documentation
4. Check test output for specific errors
