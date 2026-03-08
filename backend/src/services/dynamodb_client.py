"""
DynamoDB Client

Provides wrapper methods for DynamoDB operations with retry logic
and error handling.
"""

import boto3
import os
import time
import logging
from decimal import Decimal
from typing import Dict, List, Any, Optional
from botocore.exceptions import ClientError, BotoCoreError

logger = logging.getLogger(__name__)


def convert_floats_to_decimal(obj):
    """
    Recursively convert float values to Decimal for DynamoDB compatibility.
    
    Args:
        obj: Object to convert (dict, list, float, or other)
        
    Returns:
        Converted object with Decimals instead of floats
    """
    if isinstance(obj, list):
        return [convert_floats_to_decimal(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_floats_to_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj


def convert_decimal_to_float(obj):
    """
    Recursively convert Decimal values to float for JSON serialization.
    
    Args:
        obj: Object to convert (dict, list, Decimal, or other)
        
    Returns:
        Converted object with floats instead of Decimals
    """
    if isinstance(obj, list):
        return [convert_decimal_to_float(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: convert_decimal_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        return obj


class DynamoDBClient:
    """
    DynamoDB client with retry logic and error handling.
    
    Supports both AWS DynamoDB and DynamoDB Local for development.
    """
    
    def __init__(
        self,
        endpoint_url: Optional[str] = None,
        region_name: str = "us-east-1",
        max_retries: int = 3,
        retry_delay: float = 0.1
    ):
        """
        Initialize DynamoDB client.
        
        Args:
            endpoint_url: DynamoDB endpoint (None for AWS, http://localhost:8000 for local)
            region_name: AWS region
            max_retries: Maximum number of retry attempts
            retry_delay: Initial retry delay in seconds (exponential backoff)
        """
        self.endpoint_url = endpoint_url or os.getenv("DYNAMODB_ENDPOINT")
        self.region_name = region_name
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Initialize boto3 client
        client_kwargs = {
            "service_name": "dynamodb",
            "region_name": self.region_name
        }
        
        if self.endpoint_url:
            client_kwargs["endpoint_url"] = self.endpoint_url
            logger.info(f"Using DynamoDB endpoint: {self.endpoint_url}")
        
        self.client = boto3.client(**client_kwargs)
        self.resource = boto3.resource(**client_kwargs)
        
        # Table names from environment
        self.users_table = os.getenv("USERS_TABLE", "vibegraph-users")
        self.sessions_table = os.getenv("SESSIONS_TABLE", "vibegraph-sessions")
        self.cache_table = os.getenv("CACHE_TABLE", "vibegraph-embedding-cache")
        
        logger.info(
            f"DynamoDB client initialized: "
            f"users={self.users_table}, "
            f"sessions={self.sessions_table}, "
            f"cache={self.cache_table}"
        )
    
    def _retry_with_backoff(self, operation, *args, **kwargs):
        """
        Execute operation with exponential backoff retry logic.
        
        Args:
            operation: Function to execute
            *args: Positional arguments for operation
            **kwargs: Keyword arguments for operation
            
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
                if error_code in ["ProvisionedThroughputExceededException", "ThrottlingException", "ServiceUnavailable"]:
                    if attempt < self.max_retries - 1:
                        logger.warning(
                            f"DynamoDB {error_code}, retrying in {delay}s "
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
                        f"BotoCore error, retrying in {delay}s "
                        f"(attempt {attempt + 1}/{self.max_retries}): {e}"
                    )
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise
        
        # All retries failed
        raise last_error
    
    def put(self, table_name: str, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Put item into DynamoDB table.
        
        Args:
            table_name: Name of table
            item: Item to put
            
        Returns:
            Response from DynamoDB
            
        Raises:
            ClientError: If operation fails after retries
        """
        table = self.resource.Table(table_name)
        
        # Convert floats to Decimal for DynamoDB compatibility
        item = convert_floats_to_decimal(item)
        
        def _put():
            return table.put_item(Item=item)
        
        response = self._retry_with_backoff(_put)
        logger.debug(f"Put item to {table_name}: {item.get('userId') or item.get('sessionId')}")
        return response
    
    def get(
        self,
        table_name: str,
        key: Dict[str, Any],
        consistent_read: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Get item from DynamoDB table.
        
        Args:
            table_name: Name of table
            key: Primary key of item
            consistent_read: Whether to use consistent read
            
        Returns:
            Item if found, None otherwise (with Decimals converted to floats)
            
        Raises:
            ClientError: If operation fails after retries
        """
        table = self.resource.Table(table_name)
        
        def _get():
            return table.get_item(Key=key, ConsistentRead=consistent_read)
        
        response = self._retry_with_backoff(_get)
        item = response.get("Item")
        
        if item:
            # Convert Decimals to floats for JSON serialization
            item = convert_decimal_to_float(item)
            logger.debug(f"Got item from {table_name}: {key}")
        else:
            logger.debug(f"Item not found in {table_name}: {key}")
        
        return item
    
    def update(
        self,
        table_name: str,
        key: Dict[str, Any],
        update_expression: str,
        expression_values: Dict[str, Any],
        expression_names: Optional[Dict[str, str]] = None,
        return_values: str = "ALL_NEW"
    ) -> Dict[str, Any]:
        """
        Update item in DynamoDB table.
        
        Args:
            table_name: Name of table
            key: Primary key of item
            update_expression: Update expression
            expression_values: Expression attribute values
            expression_names: Expression attribute names (optional)
            return_values: What to return (ALL_NEW, ALL_OLD, etc.)
            
        Returns:
            Updated item attributes
            
        Raises:
            ClientError: If operation fails after retries
        """
        table = self.resource.Table(table_name)
        
        # Convert floats to Decimal for DynamoDB compatibility
        expression_values = convert_floats_to_decimal(expression_values)
        
        def _update():
            kwargs = {
                "Key": key,
                "UpdateExpression": update_expression,
                "ExpressionAttributeValues": expression_values,
                "ReturnValues": return_values
            }
            if expression_names:
                kwargs["ExpressionAttributeNames"] = expression_names
            return table.update_item(**kwargs)
        
        response = self._retry_with_backoff(_update)
        logger.debug(f"Updated item in {table_name}: {key}")
        return response.get("Attributes", {})
    
    def scan(
        self,
        table_name: str,
        filter_expression: Optional[str] = None,
        expression_values: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan DynamoDB table.
        
        Args:
            table_name: Name of table
            filter_expression: Filter expression (optional)
            expression_values: Expression attribute values (optional)
            limit: Maximum number of items to return (optional)
            
        Returns:
            List of items (with Decimals converted to floats)
            
        Raises:
            ClientError: If operation fails after retries
        """
        table = self.resource.Table(table_name)
        
        def _scan():
            kwargs = {}
            if filter_expression:
                kwargs["FilterExpression"] = filter_expression
            if expression_values:
                kwargs["ExpressionAttributeValues"] = expression_values
            if limit:
                kwargs["Limit"] = limit
            
            response = table.scan(**kwargs)
            items = response.get("Items", [])
            
            # Handle pagination if needed
            while "LastEvaluatedKey" in response and (not limit or len(items) < limit):
                kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
                response = table.scan(**kwargs)
                items.extend(response.get("Items", []))
                
                if limit and len(items) >= limit:
                    items = items[:limit]
                    break
            
            return items
        
        items = self._retry_with_backoff(_scan)
        
        # Convert Decimals to floats for JSON serialization
        items = convert_decimal_to_float(items)
        
        logger.debug(f"Scanned {table_name}: found {len(items)} items")
        return items
    
    def delete(self, table_name: str, key: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete item from DynamoDB table.
        
        Args:
            table_name: Name of table
            key: Primary key of item
            
        Returns:
            Response from DynamoDB
            
        Raises:
            ClientError: If operation fails after retries
        """
        table = self.resource.Table(table_name)
        
        def _delete():
            return table.delete_item(Key=key)
        
        response = self._retry_with_backoff(_delete)
        logger.debug(f"Deleted item from {table_name}: {key}")
        return response
    
    # Convenience methods for specific tables
    
    def put_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Put user data into Users table."""
        return self.put(self.users_table, user_data)
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user from Users table."""
        return self.get(self.users_table, {"userId": user_id})
    
    def put_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """Put session data into Sessions table."""
        return self.put(self.sessions_table, session_data)
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session from Sessions table."""
        return self.get(self.sessions_table, {"sessionId": session_id})
    
    def put_cache(self, cache_data: Dict[str, Any]) -> Dict[str, Any]:
        """Put cache entry into Cache table."""
        return self.put(self.cache_table, cache_data)
    
    def get_cache(self, doc_hash: str) -> Optional[Dict[str, Any]]:
        """Get cache entry from Cache table."""
        return self.get(self.cache_table, {"docHash": doc_hash})
    
    def scan_users(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Scan all users from Users table."""
        return self.scan(self.users_table, limit=limit)
