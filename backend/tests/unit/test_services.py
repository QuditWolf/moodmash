"""
Unit Tests for Service Clients

Tests DynamoDB client, Bedrock client, and Cache service with mocking.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError

from src.services.dynamodb_client import DynamoDBClient
from src.services.bedrock_client import BedrockClient, ClaudeService, TitanService
from src.services.cache_service import CacheService


class TestDynamoDBClient:
    """Test DynamoDB client functionality."""
    
    @pytest.fixture
    def mock_boto3(self):
        """Mock boto3 client and resource."""
        with patch('src.services.dynamodb_client.boto3') as mock:
            yield mock
    
    def test_init_with_endpoint(self, mock_boto3):
        """Test initialization with custom endpoint."""
        client = DynamoDBClient(endpoint_url="http://localhost:8000")
        
        assert client.endpoint_url == "http://localhost:8000"
        mock_boto3.client.assert_called()
        mock_boto3.resource.assert_called()
    
    def test_put_item(self, mock_boto3):
        """Test putting item into table."""
        mock_table = Mock()
        mock_boto3.resource.return_value.Table.return_value = mock_table
        
        client = DynamoDBClient()
        item = {"userId": "test-user", "data": "test"}
        
        client.put("test-table", item)
        
        mock_table.put_item.assert_called_once_with(Item=item)
    
    def test_get_item(self, mock_boto3):
        """Test getting item from table."""
        mock_table = Mock()
        mock_table.get_item.return_value = {"Item": {"userId": "test-user"}}
        mock_boto3.resource.return_value.Table.return_value = mock_table
        
        client = DynamoDBClient()
        result = client.get("test-table", {"userId": "test-user"})
        
        assert result == {"userId": "test-user"}
        mock_table.get_item.assert_called_once()
    
    def test_get_item_not_found(self, mock_boto3):
        """Test getting non-existent item returns None."""
        mock_table = Mock()
        mock_table.get_item.return_value = {}
        mock_boto3.resource.return_value.Table.return_value = mock_table
        
        client = DynamoDBClient()
        result = client.get("test-table", {"userId": "missing"})
        
        assert result is None
    
    def test_retry_on_throttling(self, mock_boto3):
        """Test retry logic on throttling exception."""
        mock_table = Mock()
        
        # First call raises throttling, second succeeds
        mock_table.put_item.side_effect = [
            ClientError(
                {"Error": {"Code": "ThrottlingException"}},
                "PutItem"
            ),
            {"ResponseMetadata": {"HTTPStatusCode": 200}}
        ]
        
        mock_boto3.resource.return_value.Table.return_value = mock_table
        
        client = DynamoDBClient(retry_delay=0.01)  # Fast retry for testing
        client.put("test-table", {"userId": "test"})
        
        assert mock_table.put_item.call_count == 2
    
    def test_convenience_methods(self, mock_boto3):
        """Test convenience methods for specific tables."""
        mock_table = Mock()
        mock_boto3.resource.return_value.Table.return_value = mock_table
        
        client = DynamoDBClient()
        
        # Test put_user
        client.put_user({"userId": "test"})
        mock_table.put_item.assert_called()
        
        # Test get_user
        mock_table.get_item.return_value = {"Item": {"userId": "test"}}
        result = client.get_user("test")
        assert result == {"userId": "test"}


class TestBedrockClient:
    """Test Bedrock client functionality."""
    
    @pytest.fixture
    def mock_boto3(self):
        """Mock boto3 client."""
        with patch('src.services.bedrock_client.boto3') as mock:
            yield mock
    
    def test_init_with_endpoint(self, mock_boto3):
        """Test initialization with custom endpoint."""
        client = BedrockClient(endpoint_url="http://localhost:4566")
        
        assert client.endpoint_url == "http://localhost:4566"
        mock_boto3.client.assert_called()
    
    def test_invoke_claude(self, mock_boto3):
        """Test Claude invocation."""
        mock_client = Mock()
        mock_response = {
            "body": Mock(read=lambda: b'{"content": [{"text": "Generated response"}]}')
        }
        mock_client.invoke_model.return_value = mock_response
        mock_boto3.client.return_value = mock_client
        
        client = BedrockClient()
        result = client.invoke_claude("Test prompt")
        
        assert result == "Generated response"
        mock_client.invoke_model.assert_called_once()
    
    def test_generate_embedding(self, mock_boto3):
        """Test Titan embedding generation."""
        mock_client = Mock()
        mock_embedding = [0.1] * 1024
        mock_response = {
            "body": Mock(read=lambda: f'{{"embedding": {mock_embedding}}}'.encode())
        }
        mock_client.invoke_model.return_value = mock_response
        mock_boto3.client.return_value = mock_client
        
        client = BedrockClient()
        result = client.generate_embedding("Test text")
        
        assert len(result) == 1024
        mock_client.invoke_model.assert_called_once()
    
    def test_generate_embedding_wrong_dimensions_raises(self, mock_boto3):
        """Test that wrong embedding dimensions raise ValueError."""
        mock_client = Mock()
        mock_embedding = [0.1] * 512  # Wrong size
        mock_response = {
            "body": Mock(read=lambda: f'{{"embedding": {mock_embedding}}}'.encode())
        }
        mock_client.invoke_model.return_value = mock_response
        mock_boto3.client.return_value = mock_client
        
        client = BedrockClient()
        
        with pytest.raises(ValueError, match="Expected 1024-dimensional"):
            client.generate_embedding("Test text")
    
    def test_retry_on_throttling(self, mock_boto3):
        """Test retry logic on throttling."""
        mock_client = Mock()
        
        # First call raises throttling, second succeeds
        mock_client.invoke_model.side_effect = [
            ClientError(
                {"Error": {"Code": "ThrottlingException"}},
                "InvokeModel"
            ),
            {
                "body": Mock(read=lambda: b'{"content": [{"text": "Success"}]}')
            }
        ]
        
        mock_boto3.client.return_value = mock_client
        
        client = BedrockClient(retry_delay=0.01)
        result = client.invoke_claude("Test")
        
        assert result == "Success"
        assert mock_client.invoke_model.call_count == 2


class TestClaudeService:
    """Test Claude service high-level methods."""
    
    @pytest.fixture
    def mock_bedrock_client(self):
        """Mock BedrockClient."""
        mock = Mock(spec=BedrockClient)
        mock.invoke_claude.return_value = "Generated text"
        return mock
    
    def test_generate_questions(self, mock_bedrock_client):
        """Test question generation."""
        service = ClaudeService(mock_bedrock_client)
        result = service.generate_questions("Generate questions", num_questions=5)
        
        assert result == "Generated text"
        mock_bedrock_client.invoke_claude.assert_called_once()
    
    def test_generate_taste_dna(self, mock_bedrock_client):
        """Test DNA generation."""
        service = ClaudeService(mock_bedrock_client)
        result = service.generate_taste_dna("Generate DNA", "Quiz summary")
        
        assert result == "Generated text"
        mock_bedrock_client.invoke_claude.assert_called_once()


class TestTitanService:
    """Test Titan service high-level methods."""
    
    @pytest.fixture
    def mock_bedrock_client(self):
        """Mock BedrockClient."""
        mock = Mock(spec=BedrockClient)
        mock.generate_embedding.return_value = [0.1] * 1024
        return mock
    
    def test_embed_text(self, mock_bedrock_client):
        """Test text embedding."""
        service = TitanService(mock_bedrock_client)
        result = service.embed_text("Test text")
        
        assert len(result) == 1024
        mock_bedrock_client.generate_embedding.assert_called_once_with(
            "Test text",
            normalize=True
        )


class TestCacheService:
    """Test cache service functionality."""
    
    @pytest.fixture
    def mock_dynamodb_client(self):
        """Mock DynamoDBClient."""
        mock = Mock(spec=DynamoDBClient)
        mock.cache_table = "test-cache-table"
        return mock
    
    def test_compute_hash(self, mock_dynamodb_client):
        """Test hash computation."""
        service = CacheService(mock_dynamodb_client)
        hash1 = service.compute_hash("test document")
        hash2 = service.compute_hash("test document")
        
        assert len(hash1) == 64  # SHA-256 hex length
        assert hash1 == hash2  # Consistent
    
    def test_cache_hit(self, mock_dynamodb_client):
        """Test cache hit returns cached embedding."""
        mock_dynamodb_client.get_cache.return_value = {
            "docHash": "abc123",
            "embedding": [0.1] * 1024,
            "hitCount": 5
        }
        
        service = CacheService(mock_dynamodb_client)
        result = service.get("abc123")
        
        assert result == [0.1] * 1024
        mock_dynamodb_client.get_cache.assert_called_once_with("abc123")
    
    def test_cache_miss(self, mock_dynamodb_client):
        """Test cache miss returns None."""
        mock_dynamodb_client.get_cache.return_value = None
        
        service = CacheService(mock_dynamodb_client)
        result = service.get("missing")
        
        assert result is None
    
    def test_put_cache(self, mock_dynamodb_client):
        """Test putting embedding into cache."""
        service = CacheService(mock_dynamodb_client)
        embedding = [0.1] * 1024
        
        result = service.put("abc123", embedding)
        
        assert result is True
        mock_dynamodb_client.put_cache.assert_called_once()
    
    def test_get_or_generate_cache_hit(self, mock_dynamodb_client):
        """Test get_or_generate with cache hit."""
        mock_dynamodb_client.get_cache.return_value = {
            "docHash": "abc123",
            "embedding": [0.1] * 1024,
            "hitCount": 5
        }
        
        service = CacheService(mock_dynamodb_client)
        generator = Mock(return_value=[0.2] * 1024)
        
        embedding, was_cached = service.get_or_generate("document", generator)
        
        assert was_cached is True
        assert embedding == [0.1] * 1024
        generator.assert_not_called()  # Should not generate on cache hit
    
    def test_get_or_generate_cache_miss(self, mock_dynamodb_client):
        """Test get_or_generate with cache miss."""
        mock_dynamodb_client.get_cache.return_value = None
        
        service = CacheService(mock_dynamodb_client)
        generator = Mock(return_value=[0.2] * 1024)
        
        embedding, was_cached = service.get_or_generate("document", generator)
        
        assert was_cached is False
        assert embedding == [0.2] * 1024
        generator.assert_called_once()  # Should generate on cache miss
        mock_dynamodb_client.put_cache.assert_called_once()  # Should cache result
