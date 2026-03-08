"""
AWS Bedrock Client Service

This module provides clients for AWS Bedrock models (Claude and Titan).
Includes retry logic and error handling.
"""

import os
import json
import time
import logging
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class BedrockClient:
    """Base Bedrock client with retry logic."""
    
    def __init__(self):
        """Initialize Bedrock runtime client."""
        endpoint_url = os.getenv('BEDROCK_ENDPOINT_URL')
        
        if endpoint_url:
            # Local development with LocalStack
            self.client = boto3.client(
                'bedrock-runtime',
                endpoint_url=endpoint_url,
                region_name=os.getenv('AWS_REGION', 'us-east-1'),
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
        else:
            # Production with real AWS
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=os.getenv('AWS_REGION', 'us-east-1')
            )
        
        logger.info(f"Bedrock client initialized (endpoint: {endpoint_url or 'AWS'})")
    
    def _retry_with_backoff(
        self,
        operation,
        max_retries: int = 3,
        initial_delay: float = 0.5
    ):
        """
        Execute operation with exponential backoff retry logic.
        
        Args:
            operation: Callable to execute
            max_retries: Maximum number of retry attempts
            initial_delay: Initial delay in seconds
            
        Returns:
            Result of operation
            
        Raises:
            Exception: If all retries fail
        """
        delay = initial_delay
        
        for attempt in range(max_retries):
            try:
                return operation()
            except ClientError as e:
                error_code = e.response['Error']['Code']
                
                # Retry on throttling or service errors
                if error_code in ['ThrottlingException', 
                                 'ServiceUnavailableException',
                                 'ModelTimeoutException']:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"Bedrock {error_code}, retrying in {delay}s "
                            f"(attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                        continue
                
                # Don't retry on other errors
                logger.error(f"Bedrock error: {error_code} - {str(e)}")
                raise
            except Exception as e:
                logger.error(f"Unexpected Bedrock error: {str(e)}")
                raise
        
        raise Exception(f"Bedrock operation failed after {max_retries} attempts")


class ClaudeService(BedrockClient):
    """
    Service for Claude 3.5 Sonnet model.
    
    Handles text generation for quiz questions, DNA profiles, growth paths,
    and analytics.
    """
    
    def __init__(self):
        """Initialize Claude service."""
        super().__init__()
        self.model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
    
    def invoke(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        system_prompt: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Invoke Claude model with prompt.
        
        Args:
            prompt: User prompt text
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            system_prompt: Optional system prompt
            
        Returns:
            Dictionary with response content
            
        Raises:
            Exception: If invocation fails after retries
        """
        def operation():
            # Build request body
            messages = [{"role": "user", "content": prompt}]
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            if system_prompt:
                body["system"] = system_prompt
            
            # Invoke model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            return response_body
        
        try:
            logger.info(f"Invoking Claude (temp={temperature}, max_tokens={max_tokens})")
            result = self._retry_with_backoff(operation, max_retries=3)
            logger.info("Claude invocation successful")
            return result
        except Exception as e:
            logger.error(f"Claude invocation failed: {str(e)}")
            raise Exception("AI service temporarily unavailable")


class TitanEmbeddingService(BedrockClient):
    """
    Service for Titan v2 embedding model.
    
    Handles generation of 1024-dimensional embedding vectors.
    """
    
    def __init__(self):
        """Initialize Titan embedding service."""
        super().__init__()
        self.model_id = "amazon.titan-embed-text-v2:0"
    
    def generate_embedding(
        self,
        text: str,
        dimensions: int = 1024,
        normalize: bool = True
    ) -> List[float]:
        """
        Generate embedding vector for text.
        
        Args:
            text: Input text to embed
            dimensions: Number of dimensions (default 1024)
            normalize: Whether to normalize the vector
            
        Returns:
            List of float values representing the embedding vector
            
        Raises:
            Exception: If generation fails after retries
            ValueError: If dimensions are invalid
        """
        if dimensions != 1024:
            raise ValueError("Titan v2 only supports 1024 dimensions")
        
        def operation():
            # Build request body
            body = {
                "inputText": text,
                "dimensions": dimensions,
                "normalize": normalize
            }
            
            # Invoke model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(body)
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract embedding vector
            embedding = response_body.get('embedding')
            if not embedding:
                raise Exception("No embedding in Titan response")
            
            # Validate dimensions
            if len(embedding) != dimensions:
                raise Exception(
                    f"Invalid embedding dimensions: expected {dimensions}, "
                    f"got {len(embedding)}"
                )
            
            return embedding
        
        try:
            logger.info(f"Generating Titan embedding (dimensions={dimensions})")
            result = self._retry_with_backoff(operation, max_retries=2)
            logger.info("Titan embedding generation successful")
            return result
        except Exception as e:
            logger.error(f"Titan embedding generation failed: {str(e)}")
            raise Exception("Failed to generate taste profile")


# Singleton instances
_claude_service = None
_titan_service = None


def get_claude_service() -> ClaudeService:
    """Get singleton Claude service instance."""
    global _claude_service
    if _claude_service is None:
        _claude_service = ClaudeService()
    return _claude_service


def get_titan_service() -> TitanEmbeddingService:
    """Get singleton Titan embedding service instance."""
    global _titan_service
    if _titan_service is None:
        _titan_service = TitanEmbeddingService()
    return _titan_service
