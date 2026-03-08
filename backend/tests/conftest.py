"""
Pytest configuration and shared fixtures for VibeGraph backend tests.

This module provides fixtures for mocking AWS services (DynamoDB, Bedrock),
test data generation, and common test utilities.
"""

import pytest
import json
import os
from unittest.mock import Mock, MagicMock
from moto import mock_dynamodb
import boto3


# ============================================================================
# AWS Service Mocks
# ============================================================================

@pytest.fixture
def aws_credentials():
    """Mock AWS credentials for testing."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'


@pytest.fixture
def dynamodb_mock(aws_credentials):
    """Mock DynamoDB service with moto."""
    with mock_dynamodb():
        yield boto3.resource('dynamodb', region_name='us-east-1')


@pytest.fixture
def users_table(dynamodb_mock):
    """Create mock Users table."""
    table = dynamodb_mock.create_table(
        TableName='Users',
        KeySchema=[
            {'AttributeName': 'userId', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'userId', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table


@pytest.fixture
def sessions_table(dynamodb_mock):
    """Create mock Sessions table."""
    table = dynamodb_mock.create_table(
        TableName='Sessions',
        KeySchema=[
            {'AttributeName': 'sessionId', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'sessionId', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table


@pytest.fixture
def embedding_cache_table(dynamodb_mock):
    """Create mock EmbeddingCache table."""
    table = dynamodb_mock.create_table(
        TableName='EmbeddingCache',
        KeySchema=[
            {'AttributeName': 'docHash', 'KeyType': 'HASH'}
        ],
        AttributeDefinitions=[
            {'AttributeName': 'docHash', 'AttributeType': 'S'}
        ],
        BillingMode='PAY_PER_REQUEST'
    )
    return table


@pytest.fixture
def bedrock_client_mock():
    """Mock Bedrock client for Claude and Titan."""
    mock_client = MagicMock()
    
    # Mock Claude response
    def mock_claude_invoke(model, messages, **kwargs):
        return {
            'content': [{
                'text': json.dumps({
                    'questions': [
                        {
                            'id': f'q{i}',
                            'title': f'Question {i}',
                            'category': 'test',
                            'options': ['Option A', 'Option B'],
                            'multiSelect': False
                        }
                        for i in range(1, 6)
                    ]
                })
            }]
        }
    
    # Mock Titan embedding response
    def mock_titan_invoke(model, inputText, **kwargs):
        # Return a mock 1024-dimensional embedding
        return {
            'embedding': [0.001] * 1024
        }
    
    mock_client.invoke_claude = Mock(side_effect=mock_claude_invoke)
    mock_client.invoke_titan = Mock(side_effect=mock_titan_invoke)
    
    return mock_client


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_quiz_answers():
    """Sample quiz answers for testing."""
    return {
        'section1': [
            {
                'questionId': 'q1',
                'selectedOptions': ['Option A']
            },
            {
                'questionId': 'q2',
                'selectedOptions': ['Option B', 'Option C']
            },
            {
                'questionId': 'q3',
                'selectedOptions': ['Option A']
            },
            {
                'questionId': 'q4',
                'selectedOptions': ['Option D']
            },
            {
                'questionId': 'q5',
                'selectedOptions': ['Option A', 'Option B']
            }
        ],
        'section2': [
            {
                'questionId': 'q6',
                'selectedOptions': ['Option C']
            },
            {
                'questionId': 'q7',
                'selectedOptions': ['Option A']
            },
            {
                'questionId': 'q8',
                'selectedOptions': ['Option B', 'Option D']
            },
            {
                'questionId': 'q9',
                'selectedOptions': ['Option A']
            },
            {
                'questionId': 'q10',
                'selectedOptions': ['Option C']
            }
        ]
    }


@pytest.fixture
def sample_embedding_vector():
    """Sample normalized 1024-dimensional embedding vector."""
    import math
    # Create a simple normalized vector
    value = 1.0 / math.sqrt(1024)
    return [value] * 1024


@pytest.fixture
def sample_taste_dna():
    """Sample TasteDNA profile for testing."""
    return {
        'archetype': 'The Explorer',
        'traits': [
            {
                'name': 'Curiosity',
                'score': 8.5,
                'description': 'High curiosity and openness to new experiences'
            },
            {
                'name': 'Depth',
                'score': 7.2,
                'description': 'Preference for deep, meaningful content'
            }
        ],
        'categories': [
            {
                'category': 'Books',
                'preferences': ['Philosophy', 'Science Fiction'],
                'intensity': 8
            },
            {
                'category': 'Music',
                'preferences': ['Jazz', 'Classical'],
                'intensity': 6
            }
        ],
        'description': 'An explorer archetype with high curiosity'
    }


@pytest.fixture
def sample_session():
    """Sample session data for testing."""
    import time
    timestamp = int(time.time() * 1000)
    
    return {
        'sessionId': 'test-session-123',
        'userId': 'test-user-456',
        'createdAt': timestamp,
        'expiresAt': timestamp + 3600000,
        'status': 'section1_complete',
        'section1Questions': [
            {
                'id': f'q{i}',
                'title': f'Question {i}',
                'category': 'test',
                'options': ['Option A', 'Option B'],
                'multiSelect': False
            }
            for i in range(1, 6)
        ]
    }


@pytest.fixture
def sample_user_record(sample_embedding_vector, sample_taste_dna):
    """Sample user record for testing."""
    import time
    
    return {
        'userId': 'test-user-123',
        'username': 'testuser',
        'email': 'test@example.com',
        'createdAt': int(time.time() * 1000),
        'updatedAt': int(time.time() * 1000),
        'embeddingId': 'emb-123',
        'vector': sample_embedding_vector,
        'dimension': 1024,
        'quizVersion': 'v1',
        'tasteDNA': sample_taste_dna
    }


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    return MagicMock()


@pytest.fixture
def api_gateway_event():
    """Sample API Gateway event for Lambda testing."""
    return {
        'httpMethod': 'POST',
        'path': '/test',
        'headers': {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token'
        },
        'body': json.dumps({'test': 'data'}),
        'requestContext': {
            'requestId': 'test-request-id',
            'authorizer': {
                'userId': 'test-user-123'
            }
        }
    }


@pytest.fixture
def lambda_context():
    """Mock Lambda context for testing."""
    context = MagicMock()
    context.function_name = 'test-function'
    context.function_version = '1'
    context.invoked_function_arn = 'arn:aws:lambda:us-east-1:123456789012:function:test'
    context.memory_limit_in_mb = 128
    context.aws_request_id = 'test-request-id'
    context.log_group_name = '/aws/lambda/test'
    context.log_stream_name = '2024/01/01/[$LATEST]test'
    return context
