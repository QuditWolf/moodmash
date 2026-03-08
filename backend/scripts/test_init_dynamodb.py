#!/usr/bin/env python3
"""
Test script for init-dynamodb.py

This script verifies that the DynamoDB initialization script works correctly
by checking that all tables are created with the correct schema.
"""

import boto3
import os
import sys
from botocore.exceptions import ClientError

# Configuration
DYNAMODB_ENDPOINT = os.environ.get('DYNAMODB_ENDPOINT', 'http://localhost:8000')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'test')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'test')

# Table names
USERS_TABLE = os.environ.get('USERS_TABLE', 'vibegraph-users')
SESSIONS_TABLE = os.environ.get('SESSIONS_TABLE', 'vibegraph-sessions')
CACHE_TABLE = os.environ.get('CACHE_TABLE', 'vibegraph-embedding-cache')


def get_dynamodb_client():
    """Create and return a DynamoDB client."""
    return boto3.client(
        'dynamodb',
        endpoint_url=DYNAMODB_ENDPOINT,
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )


def verify_table_exists(client, table_name):
    """Verify that a table exists and is active."""
    try:
        response = client.describe_table(TableName=table_name)
        status = response['Table']['TableStatus']
        
        if status == 'ACTIVE':
            print(f"✓ Table {table_name} exists and is active")
            return True
        else:
            print(f"✗ Table {table_name} exists but status is {status}")
            return False
            
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print(f"✗ Table {table_name} does not exist")
            return False
        raise


def verify_users_table_schema(client):
    """Verify Users table has correct schema."""
    try:
        response = client.describe_table(TableName=USERS_TABLE)
        table = response['Table']
        
        # Check primary key
        key_schema = table['KeySchema']
        if len(key_schema) == 1 and key_schema[0]['AttributeName'] == 'userId':
            print(f"✓ Users table has correct primary key (userId)")
        else:
            print(f"✗ Users table has incorrect primary key")
            return False
        
        # Check GSI
        gsi = table.get('GlobalSecondaryIndexes', [])
        if len(gsi) == 1 and gsi[0]['IndexName'] == 'embeddingId-index':
            print(f"✓ Users table has embeddingId-index GSI")
        else:
            print(f"✗ Users table missing embeddingId-index GSI")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error verifying Users table schema: {e}")
        return False


def verify_sessions_table_schema(client):
    """Verify Sessions table has correct schema."""
    try:
        response = client.describe_table(TableName=SESSIONS_TABLE)
        table = response['Table']
        
        # Check primary key
        key_schema = table['KeySchema']
        if len(key_schema) == 1 and key_schema[0]['AttributeName'] == 'sessionId':
            print(f"✓ Sessions table has correct primary key (sessionId)")
        else:
            print(f"✗ Sessions table has incorrect primary key")
            return False
        
        # Verify no TTL configured (as per requirements)
        ttl_status = table.get('TimeToLiveDescription', {}).get('TimeToLiveStatus', 'DISABLED')
        if ttl_status == 'DISABLED':
            print(f"✓ Sessions table has no TTL configured (as required)")
        else:
            print(f"✗ Sessions table has TTL configured (should be disabled)")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error verifying Sessions table schema: {e}")
        return False


def verify_cache_table_schema(client):
    """Verify EmbeddingCache table has correct schema."""
    try:
        response = client.describe_table(TableName=CACHE_TABLE)
        table = response['Table']
        
        # Check primary key
        key_schema = table['KeySchema']
        if len(key_schema) == 1 and key_schema[0]['AttributeName'] == 'docHash':
            print(f"✓ EmbeddingCache table has correct primary key (docHash)")
        else:
            print(f"✗ EmbeddingCache table has incorrect primary key")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Error verifying EmbeddingCache table schema: {e}")
        return False


def main():
    """Main test function."""
    print("=" * 60)
    print("DynamoDB Initialization Test")
    print("=" * 60)
    print(f"Endpoint: {DYNAMODB_ENDPOINT}")
    print(f"Region: {AWS_REGION}")
    print("=" * 60)
    
    client = get_dynamodb_client()
    
    all_passed = True
    
    # Test 1: Verify all tables exist
    print("\nTest 1: Verify tables exist")
    print("-" * 60)
    all_passed &= verify_table_exists(client, USERS_TABLE)
    all_passed &= verify_table_exists(client, SESSIONS_TABLE)
    all_passed &= verify_table_exists(client, CACHE_TABLE)
    
    # Test 2: Verify Users table schema
    print("\nTest 2: Verify Users table schema")
    print("-" * 60)
    all_passed &= verify_users_table_schema(client)
    
    # Test 3: Verify Sessions table schema
    print("\nTest 3: Verify Sessions table schema")
    print("-" * 60)
    all_passed &= verify_sessions_table_schema(client)
    
    # Test 4: Verify EmbeddingCache table schema
    print("\nTest 4: Verify EmbeddingCache table schema")
    print("-" * 60)
    all_passed &= verify_cache_table_schema(client)
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        sys.exit(1)


if __name__ == '__main__':
    main()
