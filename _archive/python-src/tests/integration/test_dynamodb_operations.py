"""
Integration tests for DynamoDB operations.

These tests verify that DynamoDB client operations work correctly
with mocked DynamoDB tables.
"""

import pytest
import time
from moto import mock_dynamodb
import boto3


@pytest.fixture
def dynamodb_resource():
    """Create mock DynamoDB resource."""
    with mock_dynamodb():
        yield boto3.resource('dynamodb', region_name='us-east-1')


@pytest.fixture
def users_table(dynamodb_resource):
    """Create Users table for testing."""
    table = dynamodb_resource.create_table(
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
def sessions_table(dynamodb_resource):
    """Create Sessions table for testing."""
    table = dynamodb_resource.create_table(
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


class TestUserOperations:
    """Test suite for user-related DynamoDB operations."""
    
    def test_create_user(self, users_table):
        """Test creating a new user record."""
        user_data = {
            'userId': 'test-user-123',
            'username': 'testuser',
            'email': 'test@example.com',
            'createdAt': int(time.time() * 1000),
            'vector': [0.5] * 1024,
            'dimension': 1024
        }
        
        users_table.put_item(Item=user_data)
        
        # Verify user was created
        response = users_table.get_item(Key={'userId': 'test-user-123'})
        assert 'Item' in response
        assert response['Item']['username'] == 'testuser'
        assert response['Item']['email'] == 'test@example.com'
    
    def test_update_user_with_taste_dna(self, users_table):
        """Test updating user with taste DNA profile."""
        # Create initial user
        users_table.put_item(Item={
            'userId': 'test-user-123',
            'username': 'testuser',
            'createdAt': int(time.time() * 1000)
        })
        
        # Update with taste DNA
        taste_dna = {
            'archetype': 'The Explorer',
            'traits': [
                {
                    'name': 'Curiosity',
                    'score': 8.5,
                    'description': 'High curiosity'
                }
            ],
            'categories': [
                {
                    'category': 'Books',
                    'preferences': ['Philosophy'],
                    'intensity': 8
                }
            ],
            'description': 'An explorer archetype'
        }
        
        users_table.update_item(
            Key={'userId': 'test-user-123'},
            UpdateExpression='SET tasteDNA = :dna, updatedAt = :updated',
            ExpressionAttributeValues={
                ':dna': taste_dna,
                ':updated': int(time.time() * 1000)
            }
        )
        
        # Verify update
        response = users_table.get_item(Key={'userId': 'test-user-123'})
        assert 'tasteDNA' in response['Item']
        assert response['Item']['tasteDNA']['archetype'] == 'The Explorer'
    
    def test_query_user_not_found(self, users_table):
        """Test querying non-existent user."""
        response = users_table.get_item(Key={'userId': 'non-existent'})
        assert 'Item' not in response


class TestSessionOperations:
    """Test suite for session-related DynamoDB operations."""
    
    def test_create_session(self, sessions_table):
        """Test creating a quiz session."""
        timestamp = int(time.time() * 1000)
        session_data = {
            'sessionId': 'session-123',
            'userId': 'user-456',
            'createdAt': timestamp,
            'expiresAt': timestamp + 3600000,
            'status': 'section1_complete',
            'section1Questions': [
                {
                    'id': 'q1',
                    'title': 'Question 1',
                    'category': 'Books',
                    'options': ['A', 'B'],
                    'multiSelect': False
                }
            ]
        }
        
        sessions_table.put_item(Item=session_data)
        
        # Verify session was created
        response = sessions_table.get_item(Key={'sessionId': 'session-123'})
        assert 'Item' in response
        assert response['Item']['status'] == 'section1_complete'
        assert len(response['Item']['section1Questions']) == 1
    
    def test_update_session_with_section2(self, sessions_table):
        """Test updating session with Section 2 data."""
        timestamp = int(time.time() * 1000)
        
        # Create initial session
        sessions_table.put_item(Item={
            'sessionId': 'session-123',
            'createdAt': timestamp,
            'expiresAt': timestamp + 3600000,
            'status': 'section1_complete'
        })
        
        # Update with Section 2
        section2_questions = [
            {
                'id': 'q6',
                'title': 'Question 6',
                'category': 'General',
                'options': ['A', 'B'],
                'multiSelect': False
            }
        ]
        
        sessions_table.update_item(
            Key={'sessionId': 'session-123'},
            UpdateExpression='SET section2Questions = :q2, #status = :status',
            ExpressionAttributeNames={
                '#status': 'status'
            },
            ExpressionAttributeValues={
                ':q2': section2_questions,
                ':status': 'section2_complete'
            }
        )
        
        # Verify update
        response = sessions_table.get_item(Key={'sessionId': 'session-123'})
        assert response['Item']['status'] == 'section2_complete'
        assert 'section2Questions' in response['Item']
    
    def test_session_expiration_check(self, sessions_table):
        """Test checking if session is expired."""
        current_time = int(time.time() * 1000)
        
        # Create expired session
        sessions_table.put_item(Item={
            'sessionId': 'expired-session',
            'createdAt': current_time - 7200000,  # 2 hours ago
            'expiresAt': current_time - 3600000,  # 1 hour ago
            'status': 'section1_complete'
        })
        
        # Create valid session
        sessions_table.put_item(Item={
            'sessionId': 'valid-session',
            'createdAt': current_time,
            'expiresAt': current_time + 3600000,  # 1 hour from now
            'status': 'section1_complete'
        })
        
        # Check expired session
        response = sessions_table.get_item(Key={'sessionId': 'expired-session'})
        assert response['Item']['expiresAt'] < current_time
        
        # Check valid session
        response = sessions_table.get_item(Key={'sessionId': 'valid-session'})
        assert response['Item']['expiresAt'] > current_time


class TestEmbeddingCacheOperations:
    """Test suite for embedding cache operations."""
    
    @pytest.fixture
    def cache_table(self, dynamodb_resource):
        """Create EmbeddingCache table."""
        table = dynamodb_resource.create_table(
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
    
    def test_cache_miss(self, cache_table):
        """Test cache miss scenario."""
        response = cache_table.get_item(Key={'docHash': 'non-existent-hash'})
        assert 'Item' not in response
    
    def test_cache_hit(self, cache_table):
        """Test cache hit scenario."""
        # Store embedding in cache
        cache_table.put_item(Item={
            'docHash': 'abc123',
            'vector': [0.5] * 1024,
            'createdAt': int(time.time() * 1000),
            'hitCount': 0,
            'lastAccessedAt': int(time.time() * 1000)
        })
        
        # Retrieve from cache
        response = cache_table.get_item(Key={'docHash': 'abc123'})
        assert 'Item' in response
        assert len(response['Item']['vector']) == 1024
    
    def test_cache_hit_count_increment(self, cache_table):
        """Test incrementing cache hit count."""
        doc_hash = 'abc123'
        
        # Initial cache entry
        cache_table.put_item(Item={
            'docHash': doc_hash,
            'vector': [0.5] * 1024,
            'createdAt': int(time.time() * 1000),
            'hitCount': 0,
            'lastAccessedAt': int(time.time() * 1000)
        })
        
        # Simulate cache hit - increment hit count
        cache_table.update_item(
            Key={'docHash': doc_hash},
            UpdateExpression='SET hitCount = hitCount + :inc, lastAccessedAt = :time',
            ExpressionAttributeValues={
                ':inc': 1,
                ':time': int(time.time() * 1000)
            }
        )
        
        # Verify hit count incremented
        response = cache_table.get_item(Key={'docHash': doc_hash})
        assert response['Item']['hitCount'] == 1
        
        # Increment again
        cache_table.update_item(
            Key={'docHash': doc_hash},
            UpdateExpression='SET hitCount = hitCount + :inc',
            ExpressionAttributeValues={':inc': 1}
        )
        
        response = cache_table.get_item(Key={'docHash': doc_hash})
        assert response['Item']['hitCount'] == 2
