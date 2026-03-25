"""
DynamoDB Client Service

This module provides a wrapper around boto3 DynamoDB client with retry logic
and error handling.
"""

import os
import time
import logging
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class DynamoDBClient:
    """
    DynamoDB client with retry logic and error handling.
    
    Provides methods for common DynamoDB operations with exponential backoff
    retry logic for handling throttling and transient errors.
    """
    
    def __init__(self):
        """Initialize DynamoDB client."""
        # Get endpoint URL from environment (for local development)
        endpoint_url = os.getenv('DYNAMODB_ENDPOINT_URL')
        
        # Configure boto3 client
        if endpoint_url:
            # Local development with DynamoDB Local
            self.client = boto3.client(
                'dynamodb',
                endpoint_url=endpoint_url,
                region_name=os.getenv('AWS_REGION', 'us-east-1'),
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
            self.resource = boto3.resource(
                'dynamodb',
                endpoint_url=endpoint_url,
                region_name=os.getenv('AWS_REGION', 'us-east-1'),
                aws_access_key_id='dummy',
                aws_secret_access_key='dummy'
            )
        else:
            # Production with real AWS
            self.client = boto3.client('dynamodb')
            self.resource = boto3.resource('dynamodb')
        
        logger.info(f"DynamoDB client initialized (endpoint: {endpoint_url or 'AWS'})")
    
    def _retry_with_backoff(self, operation, max_retries: int = 3):
        """
        Execute operation with exponential backoff retry logic.
        
        Args:
            operation: Callable to execute
            max_retries: Maximum number of retry attempts
            
        Returns:
            Result of operation
            
        Raises:
            Exception: If all retries fail
        """
        delays = [0.1, 0.2, 0.4]  # 100ms, 200ms, 400ms
        
        for attempt in range(max_retries):
            try:
                return operation()
            except ClientError as e:
                error_code = e.response['Error']['Code']
                
                # Retry on throttling or service errors
                if error_code in ['ProvisionedThroughputExceededException', 
                                 'ThrottlingException',
                                 'ServiceUnavailable']:
                    if attempt < max_retries - 1:
                        delay = delays[attempt]
                        logger.warning(
                            f"DynamoDB {error_code}, retrying in {delay}s "
                            f"(attempt {attempt + 1}/{max_retries})"
                        )
                        time.sleep(delay)
                        continue
                
                # Don't retry on other errors
                raise
            except Exception as e:
                # Don't retry on unexpected errors
                logger.error(f"Unexpected error in DynamoDB operation: {str(e)}")
                raise
        
        # All retries failed
        raise Exception(f"DynamoDB operation failed after {max_retries} attempts")
    
    def get_item(self, table_name: str, key: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get item from DynamoDB table.
        
        Args:
            table_name: Name of the table
            key: Primary key of the item
            
        Returns:
            Item dictionary or None if not found
            
        Raises:
            Exception: If operation fails after retries
        """
        def operation():
            table = self.resource.Table(table_name)
            response = table.get_item(Key=key)
            return response.get('Item')
        
        try:
            return self._retry_with_backoff(operation)
        except Exception as e:
            logger.error(f"Failed to get item from {table_name}: {str(e)}")
            raise
    
    def put_item(self, table_name: str, item: Dict[str, Any]) -> bool:
        """
        Put item into DynamoDB table.
        
        Args:
            table_name: Name of the table
            item: Item to store
            
        Returns:
            True if successful
            
        Raises:
            Exception: If operation fails after retries
        """
        def operation():
            table = self.resource.Table(table_name)
            table.put_item(Item=item)
            return True
        
        try:
            return self._retry_with_backoff(operation)
        except Exception as e:
            logger.error(f"Failed to put item into {table_name}: {str(e)}")
            raise
    
    def update_item(
        self,
        table_name: str,
        key: Dict[str, Any],
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update item in DynamoDB table.
        
        Args:
            table_name: Name of the table
            key: Primary key of the item
            updates: Dictionary of attributes to update
            
        Returns:
            Updated item
            
        Raises:
            Exception: If operation fails after retries
        """
        def operation():
            table = self.resource.Table(table_name)
            
            # Build update expression
            update_expr_parts = []
            expr_attr_names = {}
            expr_attr_values = {}
            
            for i, (attr, value) in enumerate(updates.items()):
                placeholder = f"#attr{i}"
                value_placeholder = f":val{i}"
                update_expr_parts.append(f"{placeholder} = {value_placeholder}")
                expr_attr_names[placeholder] = attr
                expr_attr_values[value_placeholder] = value
            
            update_expression = "SET " + ", ".join(update_expr_parts)
            
            response = table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues='ALL_NEW'
            )
            
            return response.get('Attributes')
        
        try:
            return self._retry_with_backoff(operation)
        except Exception as e:
            logger.error(f"Failed to update item in {table_name}: {str(e)}")
            raise
    
    def scan(
        self,
        table_name: str,
        filter_expression: Optional[str] = None,
        expression_attr_values: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Scan DynamoDB table.
        
        Args:
            table_name: Name of the table
            filter_expression: Optional filter expression
            expression_attr_values: Optional expression attribute values
            
        Returns:
            List of items
            
        Raises:
            Exception: If operation fails after retries
        """
        def operation():
            table = self.resource.Table(table_name)
            
            scan_kwargs = {}
            if filter_expression:
                scan_kwargs['FilterExpression'] = filter_expression
            if expression_attr_values:
                scan_kwargs['ExpressionAttributeValues'] = expression_attr_values
            
            items = []
            response = table.scan(**scan_kwargs)
            items.extend(response.get('Items', []))
            
            # Handle pagination
            while 'LastEvaluatedKey' in response:
                scan_kwargs['ExclusiveStartKey'] = response['LastEvaluatedKey']
                response = table.scan(**scan_kwargs)
                items.extend(response.get('Items', []))
            
            return items
        
        try:
            return self._retry_with_backoff(operation)
        except Exception as e:
            logger.error(f"Failed to scan {table_name}: {str(e)}")
            raise
    
    def delete_item(self, table_name: str, key: Dict[str, Any]) -> bool:
        """
        Delete item from DynamoDB table.
        
        Args:
            table_name: Name of the table
            key: Primary key of the item
            
        Returns:
            True if successful
            
        Raises:
            Exception: If operation fails after retries
        """
        def operation():
            table = self.resource.Table(table_name)
            table.delete_item(Key=key)
            return True
        
        try:
            return self._retry_with_backoff(operation)
        except Exception as e:
            logger.error(f"Failed to delete item from {table_name}: {str(e)}")
            raise


# Singleton instance
_dynamodb_client = None


def get_dynamodb_client() -> DynamoDBClient:
    """Get singleton DynamoDB client instance."""
    global _dynamodb_client
    if _dynamodb_client is None:
        _dynamodb_client = DynamoDBClient()
    return _dynamodb_client
