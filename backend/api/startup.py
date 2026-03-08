"""
Startup Dependency Checks for VibeGraph Backend

This module implements startup initialization checks with fail-fast logic
to ensure all required dependencies are available before accepting requests.
"""

import logging
import sys
import os
from typing import List, Tuple

# Ensure /app is in the path for imports
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from src.utils.connection_check import (
    connection_checker,
    ConnectionStatus
)

logger = logging.getLogger(__name__)


class StartupCheckError(Exception):
    """Exception raised when startup checks fail."""
    pass


class StartupChecker:
    """
    Startup checker with fail-fast logic.
    
    Validates all critical dependencies before the application
    starts accepting requests.
    """
    
    def __init__(self, fail_fast: bool = True):
        """
        Initialize startup checker.
        
        Args:
            fail_fast: If True, exit immediately on critical failures
        """
        self.fail_fast = fail_fast
        self.checks_passed = []
        self.checks_failed = []
    
    def check_dynamodb(self) -> bool:
        """
        Check DynamoDB connection and table availability.
        
        Returns:
            True if check passed, False otherwise
        """
        logger.info("Checking DynamoDB connection...")
        
        status, details = connection_checker.check_dynamodb_connection()
        
        if status == ConnectionStatus.CONNECTED:
            logger.info("✓ DynamoDB connection successful")
            logger.info(f"  Tables: {', '.join(details.get('tables', {}).keys())}")
            self.checks_passed.append("dynamodb")
            return True
        else:
            logger.error("✗ DynamoDB connection failed")
            logger.error(f"  Status: {status.value}")
            logger.error(f"  Details: {details}")
            self.checks_failed.append(("dynamodb", details))
            return False
    
    def check_bedrock(self) -> bool:
        """
        Check Bedrock connection (optional in local development).
        
        Returns:
            True if check passed, False otherwise
        """
        logger.info("Checking Bedrock connection...")
        
        status, details = connection_checker.check_bedrock_connection()
        
        if status == ConnectionStatus.CONNECTED:
            logger.info("✓ Bedrock connection successful")
            logger.info(f"  Models available: {details.get('models_available', 0)}")
            self.checks_passed.append("bedrock")
            return True
        else:
            logger.warning("⚠ Bedrock connection failed (expected in local dev)")
            logger.warning(f"  Status: {status.value}")
            logger.warning(f"  Details: {details}")
            # Don't add to checks_failed since this is optional
            return False
    
    def check_environment_variables(self) -> bool:
        """
        Check that all required environment variables are set.
        
        Returns:
            True if all required variables are set, False otherwise
        """
        logger.info("Checking environment variables...")
        
        required_vars = [
            "AWS_REGION",
            "USERS_TABLE",
            "SESSIONS_TABLE",
            "CACHE_TABLE",
        ]
        
        optional_vars = [
            "DYNAMODB_ENDPOINT",
            "BEDROCK_ENDPOINT",
            "CLAUDE_MODEL",
            "TITAN_MODEL",
        ]
        
        missing_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
                logger.error(f"✗ Missing required environment variable: {var}")
            else:
                logger.info(f"✓ {var}={value}")
        
        for var in optional_vars:
            value = os.getenv(var)
            if value:
                logger.info(f"  {var}={value}")
            else:
                logger.info(f"  {var}=<not set>")
        
        if missing_vars:
            self.checks_failed.append(("environment", {"missing": missing_vars}))
            return False
        else:
            self.checks_passed.append("environment")
            return True
    
    def check_network_connectivity(self) -> bool:
        """
        Check network connectivity to critical services.
        
        Returns:
            True if connectivity checks passed, False otherwise
        """
        logger.info("Checking network connectivity...")
        
        # Parse DynamoDB endpoint
        dynamodb_endpoint = os.getenv("DYNAMODB_ENDPOINT", "")
        if dynamodb_endpoint:
            # Extract host and port from endpoint URL
            # Format: http://host:port
            try:
                parts = dynamodb_endpoint.replace("http://", "").replace("https://", "").split(":")
                host = parts[0]
                port = int(parts[1]) if len(parts) > 1 else 8000
                
                status, details = connection_checker.check_network_connectivity(host, port)
                
                if status == ConnectionStatus.CONNECTED:
                    logger.info(f"✓ Network connectivity to DynamoDB ({host}:{port})")
                    logger.info(f"  Latency: {details.get('latency_ms', 'N/A')}ms")
                    self.checks_passed.append("network_dynamodb")
                    return True
                else:
                    logger.error(f"✗ Network connectivity to DynamoDB failed")
                    logger.error(f"  Details: {details}")
                    self.checks_failed.append(("network_dynamodb", details))
                    return False
            
            except Exception as e:
                logger.error(f"✗ Failed to parse DynamoDB endpoint: {e}")
                self.checks_failed.append(("network_dynamodb", {"error": str(e)}))
                return False
        else:
            logger.info("  DynamoDB endpoint not set, skipping network check")
            return True
    
    def run_all_checks(self) -> Tuple[bool, List[str], List[Tuple[str, dict]]]:
        """
        Run all startup checks.
        
        Returns:
            Tuple of (all_passed, passed_checks, failed_checks)
        """
        logger.info("=" * 60)
        logger.info("Running startup dependency checks...")
        logger.info("=" * 60)
        
        # Reset check results
        self.checks_passed = []
        self.checks_failed = []
        
        # Run checks
        env_ok = self.check_environment_variables()
        network_ok = self.check_network_connectivity()
        db_ok = self.check_dynamodb()
        bedrock_ok = self.check_bedrock()  # Optional
        
        # Determine overall status
        # Critical checks: environment, network, dynamodb
        critical_checks_passed = env_ok and network_ok and db_ok
        
        logger.info("=" * 60)
        if critical_checks_passed:
            logger.info("✓ All critical startup checks passed")
            logger.info(f"  Passed: {len(self.checks_passed)} checks")
            if not bedrock_ok:
                logger.info("  Note: Bedrock unavailable (expected in local dev)")
        else:
            logger.error("✗ Startup checks failed")
            logger.error(f"  Passed: {len(self.checks_passed)} checks")
            logger.error(f"  Failed: {len(self.checks_failed)} checks")
            
            for check_name, details in self.checks_failed:
                logger.error(f"    - {check_name}: {details}")
        
        logger.info("=" * 60)
        
        return critical_checks_passed, self.checks_passed, self.checks_failed
    
    def run_with_fail_fast(self) -> None:
        """
        Run all checks and exit if critical checks fail.
        
        Raises:
            StartupCheckError: If critical checks fail and fail_fast is True
        """
        all_passed, passed, failed = self.run_all_checks()
        
        if not all_passed:
            error_msg = (
                f"Startup checks failed. "
                f"Passed: {len(passed)}, Failed: {len(failed)}"
            )
            
            if self.fail_fast:
                logger.critical("FAIL-FAST: Exiting due to failed startup checks")
                raise StartupCheckError(error_msg)
            else:
                logger.warning("Continuing despite failed checks (fail_fast=False)")


# Global startup checker instance
startup_checker = StartupChecker(fail_fast=True)


def run_startup_checks(fail_fast: bool = True) -> bool:
    """
    Run startup dependency checks.
    
    Args:
        fail_fast: If True, raise exception on failure
    
    Returns:
        True if all critical checks passed, False otherwise
    
    Raises:
        StartupCheckError: If fail_fast is True and checks fail
    """
    checker = StartupChecker(fail_fast=fail_fast)
    
    if fail_fast:
        checker.run_with_fail_fast()
        return True
    else:
        all_passed, _, _ = checker.run_all_checks()
        return all_passed


def get_startup_status() -> dict:
    """
    Get the status of startup checks.
    
    Returns:
        Dict with startup check results
    """
    return {
        "checks_passed": startup_checker.checks_passed,
        "checks_failed": [
            {"check": name, "details": details}
            for name, details in startup_checker.checks_failed
        ],
        "all_passed": len(startup_checker.checks_failed) == 0
    }
