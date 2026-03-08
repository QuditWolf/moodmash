"""
Connection Validation Utilities for VibeGraph Backend

This module provides utilities for validating connections to external services
with retry logic and exponential backoff.
"""

import logging
import time
import os
from typing import Optional, Tuple, Dict, Any
from enum import Enum

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

logger = logging.getLogger(__name__)


class ConnectionStatus(Enum):
    """Connection status enumeration."""
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class ConnectionChecker:
    """
    Connection checker with retry logic and exponential backoff.
    
    Provides methods to validate connections to:
    - DynamoDB
    - AWS Bedrock
    - Network connectivity between services
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        initial_backoff: float = 0.1,
        max_backoff: float = 2.0,
        backoff_multiplier: float = 2.0
    ):
        """
        Initialize connection checker.
        
        Args:
            max_retries: Maximum number of retry attempts
            initial_backoff: Initial backoff delay in seconds
            max_backoff: Maximum backoff delay in seconds
            backoff_multiplier: Multiplier for exponential backoff
        """
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.max_backoff = max_backoff
        self.backoff_multiplier = backoff_multiplier
        
        # AWS configuration
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.dynamodb_endpoint = os.getenv("DYNAMODB_ENDPOINT")
        self.bedrock_endpoint = os.getenv("BEDROCK_ENDPOINT")
        
        # Table names
        self.users_table = os.getenv("USERS_TABLE", "vibegraph-users")
        self.sessions_table = os.getenv("SESSIONS_TABLE", "vibegraph-sessions")
        self.cache_table = os.getenv("CACHE_TABLE", "vibegraph-embedding-cache")
    
    def _exponential_backoff(self, attempt: int) -> float:
        """
        Calculate exponential backoff delay.
        
        Args:
            attempt: Current attempt number (0-indexed)
        
        Returns:
            Delay in seconds
        """
        delay = self.initial_backoff * (self.backoff_multiplier ** attempt)
        return min(delay, self.max_backoff)
    
    def check_dynamodb_connection(
        self,
        table_name: Optional[str] = None
    ) -> Tuple[ConnectionStatus, Dict[str, Any]]:
        """
        Check DynamoDB connection with retry logic.
        
        Args:
            table_name: Optional specific table to check. If None, checks all tables.
        
        Returns:
            Tuple of (ConnectionStatus, details_dict)
        """
        tables_to_check = [table_name] if table_name else [
            self.users_table,
            self.sessions_table,
            self.cache_table
        ]
        
        for attempt in range(self.max_retries):
            try:
                # Create DynamoDB client
                config = {"region_name": self.aws_region}
                if self.dynamodb_endpoint:
                    config["endpoint_url"] = self.dynamodb_endpoint
                
                client = boto3.client("dynamodb", **config)
                
                # Check each table
                table_statuses = {}
                all_active = True
                
                for table in tables_to_check:
                    try:
                        response = client.describe_table(TableName=table)
                        status = response["Table"]["TableStatus"]
                        table_statuses[table] = status
                        
                        if status != "ACTIVE":
                            all_active = False
                    
                    except ClientError as e:
                        error_code = e.response.get("Error", {}).get("Code", "Unknown")
                        table_statuses[table] = f"ERROR: {error_code}"
                        all_active = False
                
                # Determine overall status
                if all_active:
                    return ConnectionStatus.CONNECTED, {
                        "tables": table_statuses,
                        "endpoint": self.dynamodb_endpoint or "default",
                        "attempts": attempt + 1
                    }
                else:
                    return ConnectionStatus.DEGRADED, {
                        "tables": table_statuses,
                        "endpoint": self.dynamodb_endpoint or "default",
                        "attempts": attempt + 1
                    }
            
            except EndpointConnectionError as e:
                logger.warning(
                    f"DynamoDB connection attempt {attempt + 1}/{self.max_retries} failed: {e}"
                )
                
                if attempt < self.max_retries - 1:
                    delay = self._exponential_backoff(attempt)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    return ConnectionStatus.DISCONNECTED, {
                        "error": "Connection failed after all retries",
                        "endpoint": self.dynamodb_endpoint,
                        "attempts": attempt + 1
                    }
            
            except Exception as e:
                logger.error(f"DynamoDB connection check failed: {e}")
                return ConnectionStatus.UNKNOWN, {
                    "error": str(e),
                    "attempts": attempt + 1
                }
        
        return ConnectionStatus.UNKNOWN, {
            "error": "Unexpected error in connection check"
        }
    
    def check_bedrock_connection(self) -> Tuple[ConnectionStatus, Dict[str, Any]]:
        """
        Check AWS Bedrock connection with retry logic.
        
        Returns:
            Tuple of (ConnectionStatus, details_dict)
        """
        for attempt in range(self.max_retries):
            try:
                # Create Bedrock client
                config = {"region_name": self.aws_region}
                if self.bedrock_endpoint:
                    config["endpoint_url"] = self.bedrock_endpoint
                
                client = boto3.client("bedrock-runtime", **config)
                
                # Try to list models as a connectivity check
                response = client.list_foundation_models()
                
                return ConnectionStatus.CONNECTED, {
                    "endpoint": self.bedrock_endpoint or "default",
                    "models_available": len(response.get("modelSummaries", [])),
                    "attempts": attempt + 1
                }
            
            except EndpointConnectionError as e:
                logger.warning(
                    f"Bedrock connection attempt {attempt + 1}/{self.max_retries} failed: {e}"
                )
                
                if attempt < self.max_retries - 1:
                    delay = self._exponential_backoff(attempt)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                else:
                    return ConnectionStatus.DISCONNECTED, {
                        "error": "Connection failed after all retries",
                        "endpoint": self.bedrock_endpoint,
                        "attempts": attempt + 1,
                        "note": "This is expected in local development"
                    }
            
            except Exception as e:
                logger.error(f"Bedrock connection check failed: {e}")
                return ConnectionStatus.UNKNOWN, {
                    "error": str(e),
                    "attempts": attempt + 1,
                    "note": "This is expected in local development"
                }
        
        return ConnectionStatus.UNKNOWN, {
            "error": "Unexpected error in connection check"
        }
    
    def check_network_connectivity(
        self,
        host: str,
        port: int,
        timeout: float = 5.0
    ) -> Tuple[ConnectionStatus, Dict[str, Any]]:
        """
        Check network connectivity to a specific host and port.
        
        Args:
            host: Hostname or IP address
            port: Port number
            timeout: Connection timeout in seconds
        
        Returns:
            Tuple of (ConnectionStatus, details_dict)
        """
        import socket
        
        for attempt in range(self.max_retries):
            try:
                # Create socket and attempt connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                
                start_time = time.time()
                result = sock.connect_ex((host, port))
                latency = time.time() - start_time
                
                sock.close()
                
                if result == 0:
                    return ConnectionStatus.CONNECTED, {
                        "host": host,
                        "port": port,
                        "latency_ms": round(latency * 1000, 2),
                        "attempts": attempt + 1
                    }
                else:
                    logger.warning(
                        f"Network connection attempt {attempt + 1}/{self.max_retries} "
                        f"to {host}:{port} failed with code {result}"
                    )
                    
                    if attempt < self.max_retries - 1:
                        delay = self._exponential_backoff(attempt)
                        logger.info(f"Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                    else:
                        return ConnectionStatus.DISCONNECTED, {
                            "host": host,
                            "port": port,
                            "error": f"Connection refused (code {result})",
                            "attempts": attempt + 1
                        }
            
            except socket.timeout:
                logger.warning(
                    f"Network connection attempt {attempt + 1}/{self.max_retries} "
                    f"to {host}:{port} timed out"
                )
                
                if attempt < self.max_retries - 1:
                    delay = self._exponential_backoff(attempt)
                    time.sleep(delay)
                else:
                    return ConnectionStatus.DISCONNECTED, {
                        "host": host,
                        "port": port,
                        "error": "Connection timeout",
                        "attempts": attempt + 1
                    }
            
            except Exception as e:
                logger.error(f"Network connectivity check failed: {e}")
                return ConnectionStatus.UNKNOWN, {
                    "host": host,
                    "port": port,
                    "error": str(e),
                    "attempts": attempt + 1
                }
        
        return ConnectionStatus.UNKNOWN, {
            "error": "Unexpected error in connectivity check"
        }
    
    def check_all_connections(self) -> Dict[str, Any]:
        """
        Check all service connections.
        
        Returns:
            Dict with status of all connections
        """
        results = {}
        
        # Check DynamoDB
        db_status, db_details = self.check_dynamodb_connection()
        results["dynamodb"] = {
            "status": db_status.value,
            "details": db_details
        }
        
        # Check Bedrock
        bedrock_status, bedrock_details = self.check_bedrock_connection()
        results["bedrock"] = {
            "status": bedrock_status.value,
            "details": bedrock_details
        }
        
        # Determine overall health
        critical_services_healthy = (
            db_status == ConnectionStatus.CONNECTED
        )
        
        results["overall"] = {
            "healthy": critical_services_healthy,
            "status": "connected" if critical_services_healthy else "degraded"
        }
        
        return results


# Global connection checker instance
connection_checker = ConnectionChecker()


def validate_dynamodb_connection(table_name: Optional[str] = None) -> bool:
    """
    Validate DynamoDB connection.
    
    Args:
        table_name: Optional specific table to check
    
    Returns:
        True if connected, False otherwise
    """
    status, _ = connection_checker.check_dynamodb_connection(table_name)
    return status == ConnectionStatus.CONNECTED


def validate_bedrock_connection() -> bool:
    """
    Validate Bedrock connection.
    
    Returns:
        True if connected, False otherwise
    """
    status, _ = connection_checker.check_bedrock_connection()
    return status == ConnectionStatus.CONNECTED


def validate_network_connectivity(host: str, port: int) -> bool:
    """
    Validate network connectivity to a host.
    
    Args:
        host: Hostname or IP address
        port: Port number
    
    Returns:
        True if connected, False otherwise
    """
    status, _ = connection_checker.check_network_connectivity(host, port)
    return status == ConnectionStatus.CONNECTED
