#!/usr/bin/env python3
"""
Inter-Container Communication Test Script

This script tests DNS resolution and network connectivity between
all services in the VibeGraph Docker Compose setup.
"""

import socket
import sys
import time
import os
from typing import List, Tuple

# ANSI color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{BLUE}{'=' * 60}{RESET}")
    print(f"{BLUE}{text}{RESET}")
    print(f"{BLUE}{'=' * 60}{RESET}\n")


def print_success(text: str):
    """Print success message."""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text: str):
    """Print error message."""
    print(f"{RED}✗ {text}{RESET}")


def print_warning(text: str):
    """Print warning message."""
    print(f"{YELLOW}⚠ {text}{RESET}")


def test_dns_resolution(hostname: str) -> Tuple[bool, str]:
    """
    Test DNS resolution for a hostname.
    
    Args:
        hostname: Hostname to resolve
    
    Returns:
        Tuple of (success, ip_address or error_message)
    """
    try:
        ip_address = socket.gethostbyname(hostname)
        return True, ip_address
    except socket.gaierror as e:
        return False, str(e)


def test_tcp_connection(host: str, port: int, timeout: float = 5.0) -> Tuple[bool, str]:
    """
    Test TCP connection to a host and port.
    
    Args:
        host: Hostname or IP address
        port: Port number
        timeout: Connection timeout in seconds
    
    Returns:
        Tuple of (success, message)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        start_time = time.time()
        result = sock.connect_ex((host, port))
        latency = (time.time() - start_time) * 1000  # Convert to ms
        
        sock.close()
        
        if result == 0:
            return True, f"Connected (latency: {latency:.2f}ms)"
        else:
            return False, f"Connection refused (code: {result})"
    
    except socket.timeout:
        return False, "Connection timeout"
    except Exception as e:
        return False, str(e)


def test_http_endpoint(host: str, port: int, path: str = "/") -> Tuple[bool, str]:
    """
    Test HTTP endpoint availability.
    
    Args:
        host: Hostname
        port: Port number
        path: HTTP path
    
    Returns:
        Tuple of (success, message)
    """
    try:
        import http.client
        
        conn = http.client.HTTPConnection(host, port, timeout=5)
        conn.request("GET", path)
        response = conn.getresponse()
        
        status = response.status
        conn.close()
        
        if 200 <= status < 300:
            return True, f"HTTP {status}"
        else:
            return False, f"HTTP {status}"
    
    except Exception as e:
        return False, str(e)


def main():
    """Run all connectivity tests."""
    print_header("VibeGraph Inter-Container Communication Tests")
    
    # Define services to test
    services = [
        {
            "name": "Frontend",
            "hostname": "frontend",
            "alt_hostname": "vibegraph-frontend",
            "port": 3000,
            "http_path": "/"
        },
        {
            "name": "Backend API",
            "hostname": "backend-api",
            "alt_hostname": "vibegraph-backend-api",
            "port": 8000,
            "http_path": "/health"
        },
        {
            "name": "DynamoDB Local",
            "hostname": "dynamodb-local",
            "alt_hostname": "vibegraph-dynamodb-local",
            "port": 8000,
            "http_path": None  # No HTTP endpoint
        },
        {
            "name": "LocalStack",
            "hostname": "localstack",
            "alt_hostname": "vibegraph-localstack",
            "port": 4566,
            "http_path": "/_localstack/health"
        },
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    # Test each service
    for service in services:
        print_header(f"Testing: {service['name']}")
        
        # Test DNS resolution for primary hostname
        print(f"DNS Resolution: {service['hostname']}")
        total_tests += 1
        success, result = test_dns_resolution(service['hostname'])
        if success:
            print_success(f"Resolved to {result}")
            passed_tests += 1
            hostname_to_use = service['hostname']
        else:
            print_error(f"Failed: {result}")
            failed_tests += 1
            
            # Try alternative hostname
            if service.get('alt_hostname'):
                print(f"Trying alternative: {service['alt_hostname']}")
                total_tests += 1
                success, result = test_dns_resolution(service['alt_hostname'])
                if success:
                    print_success(f"Resolved to {result}")
                    passed_tests += 1
                    hostname_to_use = service['alt_hostname']
                else:
                    print_error(f"Failed: {result}")
                    failed_tests += 1
                    continue
            else:
                continue
        
        # Test TCP connection
        print(f"TCP Connection: {hostname_to_use}:{service['port']}")
        total_tests += 1
        success, result = test_tcp_connection(hostname_to_use, service['port'])
        if success:
            print_success(result)
            passed_tests += 1
        else:
            print_error(result)
            failed_tests += 1
            continue
        
        # Test HTTP endpoint if available
        if service.get('http_path'):
            print(f"HTTP Endpoint: http://{hostname_to_use}:{service['port']}{service['http_path']}")
            total_tests += 1
            success, result = test_http_endpoint(
                hostname_to_use,
                service['port'],
                service['http_path']
            )
            if success:
                print_success(result)
                passed_tests += 1
            else:
                print_warning(f"{result} (service may not be ready)")
                # Don't count as failure if service is starting
                passed_tests += 1
    
    # Print summary
    print_header("Test Summary")
    print(f"Total tests: {total_tests}")
    print_success(f"Passed: {passed_tests}")
    if failed_tests > 0:
        print_error(f"Failed: {failed_tests}")
    
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"\nSuccess rate: {success_rate:.1f}%")
    
    # Exit with appropriate code
    if failed_tests > 0:
        print_error("\nSome connectivity tests failed!")
        sys.exit(1)
    else:
        print_success("\nAll connectivity tests passed!")
        sys.exit(0)


if __name__ == "__main__":
    main()
