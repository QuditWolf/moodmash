# VibeGraph Testing Guide

This document provides comprehensive guidance on testing the VibeGraph application, including how to run tests, write new tests, and understand test coverage requirements.

## Table of Contents

- [Overview](#overview)
- [Test Types](#test-types)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Coverage Requirements](#test-coverage-requirements)
- [Mocking AWS Services](#mocking-aws-services)
- [Continuous Integration](#continuous-integration)

## Overview

VibeGraph uses a comprehensive testing strategy that includes:

- **Backend Unit Tests**: Test individual Python functions and modules using pytest
- **Frontend Unit Tests**: Test React components and services using Vitest and React Testing Library
- **Integration Tests**: Test complete end-to-end flows across services
- **Property-Based Tests**: Test universal properties using Hypothesis (backend) and fast-check (frontend)

## Test Types

### Backend Unit Tests

Located in `backend/tests/unit/`, these tests verify:
- Vector operations (normalization, cosine similarity)
- Input validation functions
- Embedding generation logic
- DynamoDB client operations
- Bedrock client interactions

**Framework**: pytest with moto for AWS mocking

### Frontend Unit Tests

Located in `frontend/tests/unit/`, these tests verify:
- API service layer (request/response handling)
- React component rendering and behavior
- State management
- Error handling

**Framework**: Vitest with React Testing Library and MSW (Mock Service Worker)

### Integration Tests

Located in `tests/integration/`, these tests verify:
- Complete quiz flow (Section 1 → Section 2 → Completion)
- Taste matching across users
- Growth path generation
- Analytics generation
- Inter-service communication

**Framework**: pytest with requests library

## Running Tests

### Quick Start

Run all tests:
```bash
make test
```

### Backend Tests

Run backend unit tests:
```bash
make test-backend
```

Run backend tests in watch mode (auto-rerun on file changes):
```bash
make test-watch-backend
```

Run specific test file:
```bash
docker-compose exec backend-api pytest tests/unit/test_vector_ops.py -v
```

Run tests with coverage report:
```bash
docker-compose exec backend-api pytest tests/unit/ -v --cov=src --cov=api --cov-report=html
```

### Frontend Tests

Run frontend unit tests:
```bash
make test-frontend
```

Run frontend tests in watch mode:
```bash
make test-watch-frontend
```

Run specific test file:
```bash
docker-compose exec frontend npm run test -- tests/unit/vibeGraphAPI.test.js
```

Run tests with UI:
```bash
docker-compose exec frontend npm run test:ui
```

### Integration Tests

Run integration tests:
```bash
make test-integration
```

**Note**: Integration tests require all services to be running and healthy. The Makefile target automatically checks service health before running tests.

Run specific integration test:
```bash
pytest tests/integration/test_quiz_flow.py::TestQuizFlow::test_complete_quiz_flow -v
```

## Writing Tests

### Backend Unit Test Example

```python
# backend/tests/unit/test_my_module.py

import pytest
from backend.src.utils.my_module import my_function


class TestMyFunction:
    """Test suite for my_function."""
    
    def test_basic_functionality(self):
        """Test basic functionality of my_function."""
        result = my_function(input_data)
        assert result == expected_output
    
    def test_error_handling(self):
        """Test that invalid input raises appropriate error."""
        with pytest.raises(ValueError, match="Invalid input"):
            my_function(invalid_input)
    
    @pytest.mark.aws
    def test_with_dynamodb(self, users_table):
        """Test function that interacts with DynamoDB."""
        # users_table fixture provides mocked DynamoDB table
        result = my_function_with_db(users_table)
        assert result is not None
```

### Frontend Unit Test Example

```javascript
// frontend/tests/unit/MyComponent.test.jsx

import { describe, it, expect } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import MyComponent from '@/components/MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })
  
  it('handles user interaction', async () => {
    render(<MyComponent />)
    
    const button = screen.getByRole('button', { name: 'Click Me' })
    fireEvent.click(button)
    
    expect(await screen.findByText('Success')).toBeInTheDocument()
  })
})
```

### Property-Based Test Example

```python
# backend/tests/unit/test_properties.py

import pytest
from hypothesis import given, strategies as st
from backend.src.utils.vector_ops import normalize_vector


class TestVectorProperties:
    """Property-based tests for vector operations."""
    
    @pytest.mark.property
    @given(st.lists(
        st.floats(min_value=-1.0, max_value=1.0, allow_nan=False),
        min_size=1024,
        max_size=1024
    ))
    def test_normalization_produces_unit_vector(self, vector):
        """Property: Any normalized vector has magnitude 1.0."""
        normalized = normalize_vector(vector)
        magnitude = sum(v * v for v in normalized) ** 0.5
        assert abs(magnitude - 1.0) < 0.0001
```

### Integration Test Example

```python
# tests/integration/test_my_flow.py

import pytest
import requests


class TestMyFlow:
    """Integration test for my workflow."""
    
    def test_complete_flow(self, api_client):
        """Test complete workflow from start to finish."""
        # Step 1: Initial request
        response = api_client.post(
            "http://localhost:8000/api/start",
            json={"data": "value"}
        )
        assert response.status_code == 200
        
        # Step 2: Follow-up request
        result_id = response.json()["id"]
        response = api_client.get(
            f"http://localhost:8000/api/result/{result_id}"
        )
        assert response.status_code == 200
        assert "result" in response.json()
```

## Test Coverage Requirements

### Coverage Thresholds

Both backend and frontend tests enforce minimum coverage thresholds:

- **Lines**: 80%
- **Functions**: 80%
- **Branches**: 80%
- **Statements**: 80%

### Viewing Coverage Reports

**Backend**:
```bash
docker-compose exec backend-api pytest tests/unit/ --cov=src --cov=api --cov-report=html
```
Open `backend/htmlcov/index.html` in a browser.

**Frontend**:
```bash
docker-compose exec frontend npm run test:coverage
```
Open `frontend/coverage/index.html` in a browser.

### Coverage Exclusions

Some code is excluded from coverage requirements:
- Test files themselves
- Configuration files
- Type checking blocks (`if TYPE_CHECKING:`)
- Abstract methods
- Debug/development code

## Mocking AWS Services

### Backend: Mocking DynamoDB

We use `moto` to mock AWS services in backend tests:

```python
import pytest
from moto import mock_dynamodb
import boto3


@pytest.fixture
def dynamodb_mock():
    """Mock DynamoDB service."""
    with mock_dynamodb():
        yield boto3.resource('dynamodb', region_name='us-east-1')


@pytest.fixture
def users_table(dynamodb_mock):
    """Create mock Users table."""
    table = dynamodb_mock.create_table(
        TableName='Users',
        KeySchema=[{'AttributeName': 'userId', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'userId', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )
    return table


def test_with_dynamodb(users_table):
    """Test function that uses DynamoDB."""
    # users_table is a fully functional mock DynamoDB table
    users_table.put_item(Item={'userId': 'test-123', 'name': 'Test User'})
    
    response = users_table.get_item(Key={'userId': 'test-123'})
    assert response['Item']['name'] == 'Test User'
```

### Backend: Mocking Bedrock (Claude/Titan)

Mock Bedrock responses for deterministic testing:

```python
from unittest.mock import MagicMock


@pytest.fixture
def bedrock_client_mock():
    """Mock Bedrock client."""
    mock_client = MagicMock()
    
    # Mock Claude response
    mock_client.invoke_claude.return_value = {
        'content': [{
            'text': '{"questions": [...]}'
        }]
    }
    
    # Mock Titan embedding response
    mock_client.invoke_titan.return_value = {
        'embedding': [0.001] * 1024
    }
    
    return mock_client
```

### Frontend: Mocking API Calls

We use MSW (Mock Service Worker) to intercept API calls:

```javascript
// frontend/tests/mocks/handlers.js

import { http, HttpResponse } from 'msw'

export const handlers = [
  http.post('http://localhost:8000/quiz/section1/start', () => {
    return HttpResponse.json({
      sessionId: 'mock-session-123',
      questions: [/* mock questions */]
    })
  }),
  
  http.get('http://localhost:8000/profile/dna/:userId', () => {
    return HttpResponse.json({
      tasteDNA: {/* mock DNA */}
    })
  })
]
```

MSW automatically intercepts fetch/axios calls in tests without modifying application code.

## Test Organization

### Backend Test Structure

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_vector_ops.py   # Vector math tests
│   │   ├── test_validation.py   # Input validation tests
│   │   └── test_handlers.py     # Lambda handler tests
│   └── integration/
│       ├── __init__.py
│       └── test_dynamodb.py     # DynamoDB integration tests
├── pytest.ini                   # Pytest configuration
└── requirements-test.txt        # Test dependencies
```

### Frontend Test Structure

```
frontend/
├── tests/
│   ├── setup.js                 # Test setup and configuration
│   ├── mocks/
│   │   ├── server.js            # MSW server setup
│   │   └── handlers.js          # API mock handlers
│   └── unit/
│       ├── vibeGraphAPI.test.js # API service tests
│       └── components/
│           └── MyComponent.test.jsx
├── vitest.config.js             # Vitest configuration
└── package.json                 # Test scripts
```

### Integration Test Structure

```
tests/
└── integration/
    ├── __init__.py
    ├── test_quiz_flow.py        # Complete quiz workflow
    ├── test_matching_flow.py    # Taste matching workflow
    └── test_growth_path.py      # Growth path generation
```

## Continuous Integration

### Pre-commit Checks

Before committing code, run:
```bash
make test
```

This ensures all tests pass before pushing changes.

### CI Pipeline

The CI pipeline runs:
1. Backend unit tests with coverage
2. Frontend unit tests with coverage
3. Integration tests (if services are available)
4. Linting and type checking

Tests must pass with minimum 80% coverage for the build to succeed.

## Troubleshooting

### Tests Fail with "Connection Refused"

**Problem**: Integration tests can't connect to services.

**Solution**: Ensure all services are running and healthy:
```bash
make up
make wait-healthy
make test-integration
```

### Mock Not Working

**Problem**: AWS service mock not intercepting calls.

**Solution**: Ensure you're using the fixture:
```python
def test_my_function(users_table):  # ← Use fixture
    # Test code here
```

### Frontend Test Timeout

**Problem**: Test times out waiting for element.

**Solution**: Use `findBy` queries for async elements:
```javascript
// ❌ Wrong - synchronous query
expect(screen.getByText('Loaded')).toBeInTheDocument()

// ✅ Correct - async query
expect(await screen.findByText('Loaded')).toBeInTheDocument()
```

### Coverage Below Threshold

**Problem**: Coverage is below 80%.

**Solution**: 
1. Check coverage report to identify uncovered lines
2. Add tests for uncovered code paths
3. Consider if code should be excluded from coverage

## Best Practices

### Do's

✅ Write tests before or alongside implementation (TDD)
✅ Use descriptive test names that explain what is being tested
✅ Test both success and error cases
✅ Mock external dependencies (AWS, APIs)
✅ Keep tests fast and independent
✅ Use fixtures for common test data
✅ Aim for high coverage of critical paths

### Don'ts

❌ Don't test implementation details
❌ Don't write tests that depend on other tests
❌ Don't use real AWS services in tests
❌ Don't skip error case testing
❌ Don't commit code with failing tests
❌ Don't mock everything (test real logic when possible)

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [Vitest documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [MSW documentation](https://mswjs.io/)
- [moto documentation](https://docs.getmoto.org/)
- [Hypothesis documentation](https://hypothesis.readthedocs.io/)

## Getting Help

If you encounter issues with testing:

1. Check this documentation
2. Review existing test examples in the codebase
3. Check test output for specific error messages
4. Ask the team in the development channel

---

**Last Updated**: 2024-01-15
**Maintained By**: VibeGraph Development Team
