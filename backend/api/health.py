"""
Comprehensive Health Check System for VibeGraph Backend

This module provides detailed health check endpoints for monitoring
the status of all backend services and dependencies.
"""

import logging
import os
from typing import Dict, Any, Tuple
from datetime import datetime

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

logger = logging.getLogger(__name__)


class HealthChecker:
    """
    Health checker for backend services and dependencies.
    
    Provides methods to check the health of:
    - DynamoDB tables
    - AWS Bedrock (Claude and Titan)
    - Cache service
    - Overall system readiness
    """
    
    def __init__(self):
        """Initialize health checker with AWS clients."""
        self.dynamodb_endpoint = os.getenv("DYNAMODB_ENDPOINT")
        self.bedrock_endpoint = os.getenv("BEDROCK_ENDPOINT")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        # Table names
        self.users_table = os.getenv("USERS_TABLE", "vibegraph-users")
        self.sessions_table = os.getenv("SESSIONS_TABLE", "vibegraph-sessions")
        self.cache_table = os.getenv("CACHE_TABLE", "vibegraph-embedding-cache")
        
        # Initialize clients lazily
        self._dynamodb_client = None
        self._bedrock_client = None
    
    @property
    def dynamodb_client(self):
        """Lazy initialization of DynamoDB client."""
        if self._dynamodb_client is None:
            config = {
                "region_name": self.aws_region,
            }
            if self.dynamodb_endpoint:
                config["endpoint_url"] = self.dynamodb_endpoint
            
            self._dynamodb_client = boto3.client("dynamodb", **config)
        
        return self._dynamodb_client
    
    @property
    def bedrock_client(self):
        """Lazy initialization of Bedrock client."""
        if self._bedrock_client is None:
            config = {
                "region_name": self.aws_region,
            }
            if self.bedrock_endpoint:
                config["endpoint_url"] = self.bedrock_endpoint
            
            self._bedrock_client = boto3.client("bedrock-runtime", **config)
        
        return self._bedrock_client
    
    def check_dynamodb(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check DynamoDB connection and table availability.
        
        Returns:
            Tuple of (is_healthy, details_dict)
        """
        try:
            # Check if all required tables exist
            tables_status = {}
            all_healthy = True
            
            for table_name in [self.users_table, self.sessions_table, self.cache_table]:
                try:
                    response = self.dynamodb_client.describe_table(TableName=table_name)
                    table_status = response["Table"]["TableStatus"]
                    tables_status[table_name] = {
                        "status": table_status,
                        "healthy": table_status == "ACTIVE"
                    }
                    if table_status != "ACTIVE":
                        all_healthy = False
                except ClientError as e:
                    tables_status[table_name] = {
                        "status": "NOT_FOUND",
                        "healthy": False,
                        "error": str(e)
                    }
                    all_healthy = False
            
            return all_healthy, {
                "status": "healthy" if all_healthy else "unhealthy",
                "tables": tables_status,
                "endpoint": self.dynamodb_endpoint or "default"
            }
        
        except EndpointConnectionError as e:
            logger.error(f"DynamoDB connection error: {e}")
            return False, {
                "status": "unreachable",
                "error": "Cannot connect to DynamoDB endpoint",
                "endpoint": self.dynamodb_endpoint
            }
        except Exception as e:
            logger.error(f"DynamoDB health check failed: {e}")
            return False, {
                "status": "error",
                "error": str(e)
            }
    
    def check_bedrock(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check AWS Bedrock availability.
        
        Note: In local development with LocalStack, this may return
        unhealthy if Bedrock is not fully mocked.
        
        Returns:
            Tuple of (is_healthy, details_dict)
        """
        try:
            # Try to list foundation models as a connectivity check
            # This is a lightweight operation
            response = self.bedrock_client.list_foundation_models()
            
            return True, {
                "status": "healthy",
                "endpoint": self.bedrock_endpoint or "default",
                "models_available": len(response.get("modelSummaries", []))
            }
        
        except EndpointConnectionError as e:
            logger.warning(f"Bedrock connection error: {e}")
            return False, {
                "status": "unreachable",
                "error": "Cannot connect to Bedrock endpoint",
                "endpoint": self.bedrock_endpoint,
                "note": "This is expected in local development"
            }
        except Exception as e:
            logger.warning(f"Bedrock health check failed: {e}")
            return False, {
                "status": "error",
                "error": str(e),
                "note": "This is expected in local development"
            }
    
    def check_cache(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check cache service (embedding cache table) availability.
        
        Returns:
            Tuple of (is_healthy, details_dict)
        """
        try:
            # Check cache table specifically
            response = self.dynamodb_client.describe_table(TableName=self.cache_table)
            table_status = response["Table"]["TableStatus"]
            
            is_healthy = table_status == "ACTIVE"
            
            # Get item count if available
            item_count = response["Table"].get("ItemCount", "unknown")
            
            return is_healthy, {
                "status": "healthy" if is_healthy else "unhealthy",
                "table_status": table_status,
                "item_count": item_count,
                "table_name": self.cache_table
            }
        
        except ClientError as e:
            logger.error(f"Cache table not found: {e}")
            return False, {
                "status": "not_found",
                "error": str(e),
                "table_name": self.cache_table
            }
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
            return False, {
                "status": "error",
                "error": str(e)
            }
    
    def check_all(self) -> Tuple[bool, Dict[str, Any]]:
        """
        Check all services and return comprehensive status.
        
        Returns:
            Tuple of (all_healthy, status_dict)
        """
        db_healthy, db_status = self.check_dynamodb()
        bedrock_healthy, bedrock_status = self.check_bedrock()
        cache_healthy, cache_status = self.check_cache()
        
        # System is healthy if DynamoDB and cache are healthy
        # Bedrock is optional in local development
        all_healthy = db_healthy and cache_healthy
        
        return all_healthy, {
            "dynamodb": db_status,
            "bedrock": bedrock_status,
            "cache": cache_status,
            "overall_status": "healthy" if all_healthy else "degraded"
        }


# Global health checker instance
health_checker = HealthChecker()


def get_basic_health() -> Dict[str, Any]:
    """
    Get basic health status (liveness check).
    
    Returns:
        Dict with basic health information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "vibegraph-api"
    }


def get_readiness_status() -> Tuple[int, Dict[str, Any]]:
    """
    Get readiness status with dependency checks.
    
    Returns:
        Tuple of (status_code, status_dict)
        - 200 if ready
        - 503 if not ready
    """
    all_healthy, details = health_checker.check_all()
    
    status_code = 200 if all_healthy else 503
    
    return status_code, {
        "status": "ready" if all_healthy else "not_ready",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "vibegraph-api",
        "dependencies": details
    }


def get_db_health() -> Tuple[int, Dict[str, Any]]:
    """
    Get DynamoDB health status.
    
    Returns:
        Tuple of (status_code, status_dict)
    """
    is_healthy, details = health_checker.check_dynamodb()
    
    status_code = 200 if is_healthy else 503
    
    return status_code, {
        "status": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "dynamodb",
        "details": details
    }


def get_bedrock_health() -> Tuple[int, Dict[str, Any]]:
    """
    Get Bedrock health status.
    
    Returns:
        Tuple of (status_code, status_dict)
    """
    is_healthy, details = health_checker.check_bedrock()
    
    status_code = 200 if is_healthy else 503
    
    return status_code, {
        "status": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "bedrock",
        "details": details
    }


def get_cache_health() -> Tuple[int, Dict[str, Any]]:
    """
    Get cache service health status.
    
    Returns:
        Tuple of (status_code, status_dict)
    """
    is_healthy, details = health_checker.check_cache()
    
    status_code = 200 if is_healthy else 503
    
    return status_code, {
        "status": "healthy" if is_healthy else "unhealthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "cache",
        "details": details
    }


def get_comprehensive_status() -> Dict[str, Any]:
    """
    Get comprehensive service status for monitoring dashboard.
    
    Returns:
        Dict with detailed status of all services
    """
    all_healthy, details = health_checker.check_all()
    
    return {
        "status": "operational" if all_healthy else "degraded",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "vibegraph-api",
        "version": "1.0.0",
        "uptime": "N/A",  # TODO: Track actual uptime
        "dependencies": details,
        "health_summary": {
            "healthy": all_healthy,
            "critical_services": {
                "dynamodb": details["dynamodb"]["status"] == "healthy",
                "cache": details["cache"]["status"] == "healthy"
            },
            "optional_services": {
                "bedrock": details["bedrock"]["status"] == "healthy"
            }
        }
    }
