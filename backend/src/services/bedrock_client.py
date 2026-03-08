"""
AWS Bedrock Client

Provides access to Claude (text generation) and Titan (embeddings) models.
"""

import boto3
import json
import os
import time
import logging
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)


class BedrockClient:
    """
    AWS Bedrock client for Claude and Titan models.
    
    Supports both AWS Bedrock and LocalStack for development.
    """
    
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        region_name: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 0.5
    ):
        """
        Initialize Bedrock client.
        
        Args:
            endpoint_url: Bedrock endpoint (None for AWS, http://localhost:4566 for LocalStack)
            region_name: AWS region (defaults to AWS_REGION env var or us-east-1)
            max_retries: Maximum number of retry attempts
            retry_delay: Initial retry delay in seconds
        """
        self.endpoint_url = endpoint_url or os.getenv("BEDROCK_ENDPOINT")
        self.region_name = region_name or os.getenv("AWS_REGION", "us-east-1")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize boto3 client
        client_kwargs = {
            "service_name": "bedrock-runtime",
            "region_name": self.region_name
        }
        
        if self.endpoint_url:
            client_kwargs["endpoint_url"] = self.endpoint_url
            logger.info(f"Using Bedrock endpoint: {self.endpoint_url}")
        
        self.client = boto3.client(**client_kwargs)
        
        # Model IDs from environment
        self.claude_model = os.getenv(
            "CLAUDE_MODEL",
            "anthropic.claude-3-5-sonnet-20241022-v2:0"
        )
        self.titan_model = os.getenv(
            "TITAN_MODEL",
            "amazon.titan-embed-text-v2:0"
        )
        
        logger.info(
            f"Bedrock client initialized: "
            f"claude={self.claude_model}, "
            f"titan={self.titan_model}"
        )
    
    def _retry_with_backoff(self, operation, *args, **kwargs):
        """
        Execute operation with exponential backoff retry logic.
        
        Args:
            operation: Function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Operation result
            
        Raises:
            ClientError: If all retries fail
        """
        last_error = None
        delay = self.retry_delay
        
        for attempt in range(self.max_retries):
            try:
                return operation(*args, **kwargs)
            except ClientError as e:
                error_code = e.response.get("Error", {}).get("Code", "Unknown")
                last_error = e
                
                # Retry on throttling or service errors
                if error_code in ["ThrottlingException", "ServiceUnavailable", "ModelTimeoutException"]:
                    if attempt < self.max_retries - 1:
                        logger.warning(
                            f"Bedrock {error_code}, retrying in {delay}s "
                            f"(attempt {attempt + 1}/{self.max_retries})"
                        )
                        time.sleep(delay)
                        delay *= 2  # Exponential backoff
                        continue
                
                # Don't retry on other errors
                raise
            except BotoCoreError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    logger.warning(
                        f"BotoCore error, retrying in {delay}s: {e}"
                    )
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise
        
        raise last_error
    
    def invoke_claude(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Invoke Claude or Nova model for text generation.
        
        Args:
            prompt: User prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)
            system_prompt: System prompt (optional)
            
        Returns:
            Generated text
            
        Raises:
            ClientError: If invocation fails after retries
            
        Example:
            >>> client = BedrockClient()
            >>> response = client.invoke_claude("Generate 5 quiz questions about art")
            >>> print(response)
        """
        # Check if using Nova model
        is_nova = "nova" in self.claude_model.lower()
        
        if is_nova:
            # Nova API format
            body = {
                "messages": [
                    {
                        "role": "user",
                        "content": [{"text": prompt}]
                    }
                ],
                "inferenceConfig": {
                    "max_new_tokens": max_tokens,
                    "temperature": temperature
                }
            }
            
            if system_prompt:
                body["system"] = [{"text": system_prompt}]
        else:
            # Claude API format
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            if system_prompt:
                body["system"] = system_prompt
        
        def _invoke():
            response = self.client.invoke_model(
                modelId=self.claude_model,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response["body"].read())
            
            if is_nova:
                # Nova response format
                output = response_body.get("output", {})
                message = output.get("message", {})
                content = message.get("content", [])
                if content and len(content) > 0:
                    return content[0].get("text", "")
            else:
                # Claude response format
                content = response_body.get("content", [])
                if content and len(content) > 0:
                    return content[0].get("text", "")
            
            return ""
        
        start_time = time.time()
        result = self._retry_with_backoff(_invoke)
        elapsed = time.time() - start_time
        
        logger.info(
            f"Model invocation completed in {elapsed:.2f}s, "
            f"generated {len(result)} characters"
        )
        
        return result
    
    def generate_embedding(
        self,
        text: str,
        normalize: bool = True
    ) -> List[float]:
        """
        Generate embedding using Titan v2 model.
        
        Args:
            text: Input text to embed
            normalize: Whether to normalize the embedding (default: True)
            
        Returns:
            1024-dimensional embedding vector
            
        Raises:
            ClientError: If generation fails after retries
            ValueError: If embedding dimensions are incorrect
            
        Example:
            >>> client = BedrockClient()
            >>> embedding = client.generate_embedding("User taste profile...")
            >>> len(embedding)
            1024
        """
        # Build request body for Titan v2
        body = {
            "inputText": text,
            "dimensions": 1024,
            "normalize": normalize
        }
        
        def _invoke():
            response = self.client.invoke_model(
                modelId=self.titan_model,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json"
            )
            
            response_body = json.loads(response["body"].read())
            
            # Extract embedding from response
            embedding = response_body.get("embedding", [])
            
            if not embedding:
                raise ValueError("No embedding returned from Titan")
            
            if len(embedding) != 1024:
                raise ValueError(
                    f"Expected 1024-dimensional embedding, got {len(embedding)}"
                )
            
            return embedding
        
        start_time = time.time()
        result = self._retry_with_backoff(_invoke)
        elapsed = time.time() - start_time
        
        logger.info(
            f"Titan embedding generated in {elapsed:.2f}s, "
            f"dimensions={len(result)}"
        )
        
        return result


class ClaudeService:
    """
    High-level service for Claude text generation.
    
    Provides convenient methods for specific use cases.
    """
    
    def __init__(self, bedrock_client: Optional[BedrockClient] = None):
        """
        Initialize Claude service.
        
        Args:
            bedrock_client: BedrockClient instance (creates new if None)
        """
        self.client = bedrock_client or BedrockClient()
    
    def generate_questions(
        self,
        prompt: str,
        num_questions: int = 5,
        context: Optional[str] = None
    ) -> str:
        """
        Generate quiz questions using Claude.
        
        Args:
            prompt: Question generation prompt
            num_questions: Number of questions to generate
            context: Additional context (e.g., previous answers)
            
        Returns:
            Generated questions as JSON string
        """
        full_prompt = prompt
        if context:
            full_prompt = f"{context}\n\n{prompt}"
        
        return self.client.invoke_claude(
            prompt=full_prompt,
            max_tokens=4096,
            temperature=0.8
        )
    
    def generate_taste_dna(
        self,
        prompt: str,
        quiz_summary: str
    ) -> str:
        """
        Generate taste DNA profile using Claude.
        
        Args:
            prompt: DNA generation prompt
            quiz_summary: Summary of quiz answers
            
        Returns:
            Generated DNA profile as JSON string
        """
        full_prompt = f"{prompt}\n\nQuiz Summary:\n{quiz_summary}"
        
        return self.client.invoke_claude(
            prompt=full_prompt,
            max_tokens=2048,
            temperature=0.7
        )
    
    def generate_growth_path(
        self,
        prompt: str,
        dna_profile: str
    ) -> str:
        """
        Generate growth path recommendations using Claude.
        
        Args:
            prompt: Path generation prompt
            dna_profile: User's taste DNA profile
            
        Returns:
            Generated growth path as JSON string
        """
        full_prompt = f"{prompt}\n\nTaste DNA:\n{dna_profile}"
        
        return self.client.invoke_claude(
            prompt=full_prompt,
            max_tokens=3072,
            temperature=0.7
        )
    
    def generate_analytics(
        self,
        prompt: str,
        user_data: str
    ) -> str:
        """
        Generate behavioral analytics using Claude.
        
        Args:
            prompt: Analytics generation prompt
            user_data: User's DNA and path data
            
        Returns:
            Generated analytics as JSON string
        """
        full_prompt = f"{prompt}\n\nUser Data:\n{user_data}"
        
        return self.client.invoke_claude(
            prompt=full_prompt,
            max_tokens=2048,
            temperature=0.6
        )


class TitanService:
    """
    High-level service for Titan embeddings.
    
    Provides convenient methods for embedding generation.
    """
    
    def __init__(self, bedrock_client: Optional[BedrockClient] = None):
        """
        Initialize Titan service.
        
        Args:
            bedrock_client: BedrockClient instance (creates new if None)
        """
        self.client = bedrock_client or BedrockClient()
    
    def embed_text(
        self,
        text: str,
        normalize: bool = True
    ) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
            normalize: Whether to normalize embedding
            
        Returns:
            1024-dimensional embedding vector
        """
        return self.client.generate_embedding(text, normalize=normalize)
