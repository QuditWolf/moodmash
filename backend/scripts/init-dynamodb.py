#!/usr/bin/env python3
"""
DynamoDB Local Initialization Script

This script creates the required DynamoDB tables for the VibeGraph application:
- Users table: Stores user profiles, embeddings, DNA profiles, and growth paths
- Sessions table: Stores quiz sessions with 1-hour TTL
- EmbeddingCache table: Caches Titan embeddings to minimize API calls

The script is designed to run automatically when the DynamoDB Local container starts.
"""

import boto3
import os
import sys
import time
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


def wait_for_dynamodb(client, max_retries=30, retry_interval=2):
    """Wait for DynamoDB Local to be ready."""
    print(f"Waiting for DynamoDB at {DYNAMODB_ENDPOINT}...")
    
    for attempt in range(max_retries):
        try:
            client.list_tables()
            print("DynamoDB is ready!")
            return True
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt + 1}/{max_retries}: DynamoDB not ready yet, retrying in {retry_interval}s...")
                time.sleep(retry_interval)
            else:
                print(f"Failed to connect to DynamoDB after {max_retries} attempts: {e}")
                return False
    
    return False


def table_exists(client, table_name):
    """Check if a table already exists."""
    try:
        client.describe_table(TableName=table_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            return False
        raise


def create_users_table(client):
    """
    Create the Users table.
    
    Schema:
    - userId (String): Primary key - unique user identifier
    - username (String): User's display name
    - email (String): User's email address
    - createdAt (Number): Unix timestamp of user creation
    - updatedAt (Number): Unix timestamp of last update
    - embeddingId (String): Unique identifier for the embedding
    - vector (List): 1024-dimensional Titan v2 embedding vector
    - dimension (Number): Always 1024
    - quizVersion (String): Version of the quiz (e.g., "v1")
    - tasteDNA (Map): Taste DNA profile with archetype, traits, categories
    - growthPath (Map): Personalized growth path with absorb/create/reflect
    - analytics (Map): Behavioral analytics and insights
    
    Note: No TTL for this table - user data persists indefinitely
    """
    table_name = USERS_TABLE
    
    if table_exists(client, table_name):
        print(f"Table {table_name} already exists, skipping creation.")
        return
    
    print(f"Creating table {table_name}...")
    
    try:
        client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'userId',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'userId',
                    'AttributeType': 'S'  # String
                },
                {
                    'AttributeName': 'embeddingId',
                    'AttributeType': 'S'  # String
                }
            ],
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'embeddingId-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'embeddingId',
                            'KeyType': 'HASH'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        print(f"Table {table_name} created successfully!")
        
    except ClientError as e:
        print(f"Error creating table {table_name}: {e}")
        raise


def create_sessions_table(client):
    """
    Create the Sessions table.
    
    Schema:
    - sessionId (String): Primary key - unique session identifier
    - userId (String): Optional - user ID for authenticated users
    - createdAt (Number): Unix timestamp of session creation
    - expiresAt (Number): Unix timestamp when session expires (createdAt + 3600)
    - status (String): Session status - "section1_complete", "section2_complete", "quiz_complete"
    - section1Questions (List): Array of Section 1 questions
    - section1Answers (List): Array of Section 1 answers
    - section2Questions (List): Array of Section 2 questions
    - section2Answers (List): Array of Section 2 answers
    
    Note: Sessions expire after 1 hour (expiresAt = createdAt + 3600 seconds)
    Note: No TTL attribute configured as per task requirements
    """
    table_name = SESSIONS_TABLE
    
    if table_exists(client, table_name):
        print(f"Table {table_name} already exists, skipping creation.")
        return
    
    print(f"Creating table {table_name}...")
    
    try:
        client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'sessionId',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'sessionId',
                    'AttributeType': 'S'  # String
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        print(f"Table {table_name} created successfully!")
        
    except ClientError as e:
        print(f"Error creating table {table_name}: {e}")
        raise


def create_embedding_cache_table(client):
    """
    Create the EmbeddingCache table.
    
    Schema:
    - docHash (String): Primary key - SHA-256 hash of the embedding document
    - vector (List): 1024-dimensional Titan v2 embedding vector
    - createdAt (Number): Unix timestamp of cache entry creation
    - hitCount (Number): Number of times this cached embedding was retrieved
    - lastAccessedAt (Number): Unix timestamp of last cache access
    
    Purpose: Cache Titan embeddings to minimize API calls and reduce costs
    Target cache hit rate: 40%
    """
    table_name = CACHE_TABLE
    
    if table_exists(client, table_name):
        print(f"Table {table_name} already exists, skipping creation.")
        return
    
    print(f"Creating table {table_name}...")
    
    try:
        client.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'docHash',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'docHash',
                    'AttributeType': 'S'  # String (SHA-256 hash)
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        
        print(f"Table {table_name} created successfully!")
        
    except ClientError as e:
        print(f"Error creating table {table_name}: {e}")
        raise


def wait_for_table_active(client, table_name, max_retries=30, retry_interval=2):
    """Wait for a table to become active."""
    print(f"Waiting for table {table_name} to become active...")
    
    for attempt in range(max_retries):
        try:
            response = client.describe_table(TableName=table_name)
            status = response['Table']['TableStatus']
            
            if status == 'ACTIVE':
                print(f"Table {table_name} is now active!")
                return True
            
            print(f"Table {table_name} status: {status}, waiting...")
            time.sleep(retry_interval)
            
        except ClientError as e:
            print(f"Error checking table status: {e}")
            return False
    
    print(f"Table {table_name} did not become active within the timeout period.")
    return False


def main():
    """Main initialization function."""
    print("=" * 60)
    print("DynamoDB Local Initialization Script")
    print("=" * 60)
    print(f"Endpoint: {DYNAMODB_ENDPOINT}")
    print(f"Region: {AWS_REGION}")
    print(f"Users Table: {USERS_TABLE}")
    print(f"Sessions Table: {SESSIONS_TABLE}")
    print(f"Cache Table: {CACHE_TABLE}")
    print("=" * 60)
    
    # Create DynamoDB client
    client = get_dynamodb_client()
    
    # Wait for DynamoDB to be ready
    if not wait_for_dynamodb(client):
        print("Failed to connect to DynamoDB. Exiting.")
        sys.exit(1)
    
    # Create tables
    try:
        # Create Users table
        create_users_table(client)
        wait_for_table_active(client, USERS_TABLE)
        
        # Create Sessions table
        create_sessions_table(client)
        wait_for_table_active(client, SESSIONS_TABLE)
        
        # Create EmbeddingCache table
        create_embedding_cache_table(client)
        wait_for_table_active(client, CACHE_TABLE)
        
        print("\n" + "=" * 60)
        print("All tables created successfully!")
        print("=" * 60)
        
        # List all tables
        response = client.list_tables()
        print("\nExisting tables:")
        for table in response['TableNames']:
            print(f"  - {table}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\nError during initialization: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
