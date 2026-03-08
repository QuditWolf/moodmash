# Testing Quick Reference

Quick reference for common testing commands and patterns in VibeGraph.

## Quick Commands

### Run All Tests
```bash
make test                    # All tests (backend + frontend + integration)
make test-backend           # Backend unit tests only
make test-frontend          # Frontend unit tests only
make test-integration       # Integration tests only
```

### Watch Mode (Auto-rerun on changes)
```bash
make test-watch-backend     # Backend tests in watch mode
make test-watch-frontend    # Frontend tests in watch mode
```

### Coverage Reports
```bash
# Backend coverage
docker-compose exec backend-api pytest tests/unit/ --cov=src --cov=api --cov-report=html
# Open backend/htmlcov/index.html

# Frontend coverage
docker-compose exec frontend npm run test:coverage
# Open frontend/coverage/index.html
```

### Run Specific Tests
```bash
# Backend - specific file
docker-compose exec backend-api pytest tests/unit/test_vector_ops.py -v

# Backend - specific test
docker-compose exec backend-api pytest tests/unit/test_vector_ops.py::TestNormalizeVector::test_normalize_simple_vector -v

# Frontend - specific file
docker-compose exec frontend npm run test -- tests/unit/vibeGraphAPI.test.js

# Integration - specific test
pytest tests/integration/test_quiz_flow.py::TestQuizFlow::test_complete_quiz_flow -v
```

## Test Patterns

### Backend Unit Test Pattern

```python
import pytest

class TestMyFunction:
    """Test suite for my_function."""
    
    def test_success_case(self):
        """Test successful execution."""
        result = my_function(valid_input)
        assert result == expected_output
    
    def test_error_case(self):
        """Test error handling."""
        with pytest.raises(ValueError, match="Error message"):
            my_function(invalid_input)
    
    @pytest.mark.aws
    def test_with_mock(self, users_table):
        """Test with mocked AWS service."""
        result = my_function_with_db(users_table)
        assert result is not None
```

### Frontend Unit Test Pattern

```javascript
import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Text')).toBeInTheDocument()
  })
  
  it('handles interaction', async () => {
    render(<MyComponent />)
    fireEvent.click(screen.getByRole('button'))
    expect(await screen.findByText('Result')).toBeInTheDocument()
  })
})
```

### Integration Test Pattern

```python
import pytest
import requests

class TestFlow:
    def test_complete_flow(self, api_client):
        response = api_client.post(
            "http://localhost:8000/api/endpoint",
            json={"data": "value"}
        )
        assert response.status_code == 200
        assert "field" in response.json()
```

## Common Fixtures

### Backend Fixtures (from conftest.py)

```python
def test_with_fixtures(
    users_table,              # Mock DynamoDB Users table
    sessions_table,           # Mock DynamoDB Sessions table
    embedding_cache_table,    # Mock DynamoDB EmbeddingCache table
    bedrock_client_mock,      # Mock Bedrock client
    sample_quiz_answers,      # Sample quiz answer data
    sample_embedding_vector,  # Sample 1024-dim vector
    sample_taste_dna,         # Sample TasteDNA profile
    sample_session,           # Sample session data
    sample_user_record,       # Sample user record
    api_gateway_event,        # Mock API Gateway event
    lambda_context            # Mock Lambda context
):
    # Use fixtures in test
    pass
```

### Frontend Fixtures (MSW handlers)

API mocking is automatic via MSW. Override handlers in tests:

```javascript
import { server } from '../mocks/server'
import { http, HttpResponse } from 'msw'

it('handles error', async () => {
  server.use(
    http.post('http://localhost:8000/api/endpoint', () => {
      return HttpResponse.json(
        { message: 'Error' },
        { status: 500 }
      )
    })
  )
  
  // Test error handling
})
```

## Debugging Tests

### Backend Debugging

```bash
# Run with print statements visible
docker-compose exec backend-api pytest tests/unit/test_file.py -v -s

# Run with debugger
docker-compose exec backend-api pytest tests/unit/test_file.py --pdb

# Show local variables on failure
docker-compose exec backend-api pytest tests/unit/test_file.py -l
```

### Frontend Debugging

```bash
# Run with console output
docker-compose exec frontend npm run test -- --reporter=verbose

# Run single test in watch mode
docker-compose exec frontend npm run test:watch -- tests/unit/mytest.test.js

# Use Vitest UI
docker-compose exec frontend npm run test:ui
```

### Integration Test Debugging

```bash
# Check service health first
make health

# View service logs
make logs-backend
make logs-frontend

# Run test with verbose output
pytest tests/integration/test_quiz_flow.py -v -s

# Run test with debugger
pytest tests/integration/test_quiz_flow.py --pdb
```

## Test Markers

### Backend Markers

```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.slow          # Slow running test
@pytest.mark.aws           # Uses AWS services (mocked)
@pytest.mark.property      # Property-based test
```

Run tests by marker:
```bash
docker-compose exec backend-api pytest -m unit
docker-compose exec backend-api pytest -m "not slow"
```

## Coverage Thresholds

Both backend and frontend require:
- **Lines**: 80%
- **Functions**: 80%
- **Branches**: 80%
- **Statements**: 80%

## Common Issues

### Issue: Tests fail with "Connection Refused"
**Solution**: Ensure services are running
```bash
make up
make wait-healthy
```

### Issue: Mock not working
**Solution**: Use the fixture parameter
```python
def test_my_function(users_table):  # ← Add fixture
    # Test code
```

### Issue: Frontend test timeout
**Solution**: Use async queries
```javascript
// ❌ Wrong
expect(screen.getByText('Text')).toBeInTheDocument()

// ✅ Correct
expect(await screen.findByText('Text')).toBeInTheDocument()
```

### Issue: Coverage below threshold
**Solution**: Check coverage report and add tests
```bash
# Backend
docker-compose exec backend-api pytest --cov=src --cov-report=html
# Open backend/htmlcov/index.html

# Frontend
docker-compose exec frontend npm run test:coverage
# Open frontend/coverage/index.html
```

## Test File Naming

### Backend
- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Frontend
- Test files: `*.test.js`, `*.test.jsx`, `*.spec.js`, `*.spec.jsx`
- Test suites: `describe('Name', () => {})`
- Test cases: `it('does something', () => {})` or `test('does something', () => {})`

## Useful Commands

```bash
# Check test discovery (backend)
docker-compose exec backend-api pytest --collect-only

# Run tests in parallel (backend)
docker-compose exec backend-api pytest -n auto

# Generate coverage badge
docker-compose exec backend-api pytest --cov=src --cov-report=term

# Clear test cache (backend)
docker-compose exec backend-api pytest --cache-clear

# Update snapshots (frontend)
docker-compose exec frontend npm run test -- -u
```

## Resources

- [Full Testing Guide](./README.md)
- [pytest docs](https://docs.pytest.org/)
- [Vitest docs](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [MSW docs](https://mswjs.io/)

---

**Tip**: Bookmark this page for quick reference during development!
