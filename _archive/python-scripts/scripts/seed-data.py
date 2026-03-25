#!/usr/bin/env python3
"""
DynamoDB Seed Data Script

This script creates sample users, embeddings, and DNA profiles for testing
the VibeGraph matching functionality. It supports a --reset flag to clear
existing data before seeding.

Usage:
    python seed-data.py              # Add seed data
    python seed-data.py --reset      # Clear existing data and add seed data
"""

import boto3
import os
import sys
import time
import argparse
import random
import math
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


def normalize_vector(vector):
    """Normalize a vector to unit length."""
    magnitude = math.sqrt(sum(x * x for x in vector))
    if magnitude == 0:
        return vector
    return [x / magnitude for x in vector]


def generate_random_embedding(seed=None):
    """Generate a random 1024-dimensional normalized embedding vector."""
    if seed is not None:
        random.seed(seed)
    
    # Generate random vector
    vector = [random.uniform(-1, 1) for _ in range(1024)]
    
    # Normalize to unit length
    return normalize_vector(vector)


def clear_table_data(client, table_name):
    """Clear all data from a table."""
    print(f"Clearing data from {table_name}...")
    
    try:
        # Scan all items
        response = client.scan(TableName=table_name)
        items = response.get('Items', [])
        
        # Get the key schema to determine partition key
        table_info = client.describe_table(TableName=table_name)
        key_schema = table_info['Table']['KeySchema']
        partition_key = next(k['AttributeName'] for k in key_schema if k['KeyType'] == 'HASH')
        
        # Delete each item
        for item in items:
            key = {partition_key: item[partition_key]}
            client.delete_item(TableName=table_name, Key=key)
        
        print(f"Cleared {len(items)} items from {table_name}")
        
    except ClientError as e:
        print(f"Error clearing table {table_name}: {e}")
        raise


def create_sample_users(client):
    """Create sample users with embeddings and DNA profiles."""
    print("\nCreating sample users...")
    
    timestamp = int(time.time())
    
    # Sample user profiles with different archetypes
    users = [
        {
            'userId': 'user-001',
            'username': 'Alex Chen',
            'email': 'alex.chen@example.com',
            'archetype': 'The Explorer',
            'traits': [
                {'name': 'Curiosity', 'score': 9},
                {'name': 'Openness', 'score': 8},
                {'name': 'Adventurousness', 'score': 9}
            ],
            'seed': 42
        },
        {
            'userId': 'user-002',
            'username': 'Jordan Smith',
            'email': 'jordan.smith@example.com',
            'archetype': 'The Minimalist',
            'traits': [
                {'name': 'Simplicity', 'score': 9},
                {'name': 'Focus', 'score': 8},
                {'name': 'Intentionality', 'score': 9}
            ],
            'seed': 123
        },
        {
            'userId': 'user-003',
            'username': 'Sam Rivera',
            'email': 'sam.rivera@example.com',
            'archetype': 'The Curator',
            'traits': [
                {'name': 'Discernment', 'score': 8},
                {'name': 'Appreciation', 'score': 9},
                {'name': 'Refinement', 'score': 7}
            ],
            'seed': 456
        },
        {
            'userId': 'user-004',
            'username': 'Taylor Kim',
            'email': 'taylor.kim@example.com',
            'archetype': 'The Creator',
            'traits': [
                {'name': 'Creativity', 'score': 9},
                {'name': 'Expression', 'score': 8},
                {'name': 'Innovation', 'score': 8}
            ],
            'seed': 789
        },
        {
            'userId': 'user-005',
            'username': 'Morgan Lee',
            'email': 'morgan.lee@example.com',
            'archetype': 'The Analyst',
            'traits': [
                {'name': 'Logic', 'score': 9},
                {'name': 'Precision', 'score': 8},
                {'name': 'Depth', 'score': 9}
            ],
            'seed': 101
        }
    ]
    
    for user_data in users:
        # Generate embedding vector
        vector = generate_random_embedding(user_data['seed'])
        embedding_id = f"emb-{user_data['userId']}"
        
        # Create user item
        item = {
            'userId': {'S': user_data['userId']},
            'username': {'S': user_data['username']},
            'email': {'S': user_data['email']},
            'createdAt': {'N': str(timestamp)},
            'updatedAt': {'N': str(timestamp)},
            'embeddingId': {'S': embedding_id},
            'vector': {'L': [{'N': str(v)} for v in vector]},
            'dimension': {'N': '1024'},
            'quizVersion': {'S': 'v1'},
            'tasteDNA': {
                'M': {
                    'archetype': {'S': user_data['archetype']},
                    'traits': {
                        'L': [
                            {
                                'M': {
                                    'name': {'S': trait['name']},
                                    'score': {'N': str(trait['score'])},
                                    'description': {'S': f"Strong {trait['name'].lower()} trait"}
                                }
                            }
                            for trait in user_data['traits']
                        ]
                    },
                    'categories': {
                        'L': [
                            {
                                'M': {
                                    'category': {'S': 'Music'},
                                    'preferences': {'L': [{'S': 'Indie'}, {'S': 'Electronic'}]},
                                    'intensity': {'N': '8'}
                                }
                            },
                            {
                                'M': {
                                    'category': {'S': 'Art'},
                                    'preferences': {'L': [{'S': 'Contemporary'}, {'S': 'Abstract'}]},
                                    'intensity': {'N': '7'}
                                }
                            }
                        ]
                    },
                    'description': {'S': f"A {user_data['archetype']} with unique taste preferences"}
                }
            }
        }
        
        try:
            client.put_item(TableName=USERS_TABLE, Item=item)
            print(f"  ✓ Created user: {user_data['username']} ({user_data['archetype']})")
        except ClientError as e:
            print(f"  ✗ Error creating user {user_data['username']}: {e}")
            raise


def create_sample_embeddings_cache(client):
    """Create sample embedding cache entries."""
    print("\nCreating sample embedding cache entries...")
    
    timestamp = int(time.time())
    
    # Sample cache entries
    cache_entries = [
        {
            'docHash': 'a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2',
            'hitCount': 5,
            'seed': 111
        },
        {
            'docHash': 'b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3',
            'hitCount': 3,
            'seed': 222
        },
        {
            'docHash': 'c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2g3h4',
            'hitCount': 8,
            'seed': 333
        }
    ]
    
    for entry in cache_entries:
        vector = generate_random_embedding(entry['seed'])
        
        item = {
            'docHash': {'S': entry['docHash']},
            'vector': {'L': [{'N': str(v)} for v in vector]},
            'createdAt': {'N': str(timestamp - 3600)},  # 1 hour ago
            'hitCount': {'N': str(entry['hitCount'])},
            'lastAccessedAt': {'N': str(timestamp)}
        }
        
        try:
            client.put_item(TableName=CACHE_TABLE, Item=item)
            print(f"  ✓ Created cache entry: {entry['docHash'][:16]}... (hits: {entry['hitCount']})")
        except ClientError as e:
            print(f"  ✗ Error creating cache entry: {e}")
            raise


def main():
    """Main seeding function."""
    parser = argparse.ArgumentParser(description='Seed DynamoDB with sample data')
    parser.add_argument('--reset', action='store_true', help='Clear existing data before seeding')
    args = parser.parse_args()
    
    print("=" * 60)
    print("DynamoDB Seed Data Script")
    print("=" * 60)
    print(f"Endpoint: {DYNAMODB_ENDPOINT}")
    print(f"Region: {AWS_REGION}")
    print(f"Reset mode: {'ON' if args.reset else 'OFF'}")
    print("=" * 60)
    
    # Create DynamoDB client
    client = get_dynamodb_client()
    
    try:
        # Clear existing data if reset flag is set
        if args.reset:
            print("\nClearing existing data...")
            clear_table_data(client, USERS_TABLE)
            clear_table_data(client, CACHE_TABLE)
            # Note: Not clearing sessions table as sessions are temporary
        
        # Create sample data
        create_sample_users(client)
        create_sample_embeddings_cache(client)
        
        print("\n" + "=" * 60)
        print("Seed data created successfully!")
        print("=" * 60)
        print("\nSample users created:")
        print("  - user-001: Alex Chen (The Explorer)")
        print("  - user-002: Jordan Smith (The Minimalist)")
        print("  - user-003: Sam Rivera (The Curator)")
        print("  - user-004: Taylor Kim (The Creator)")
        print("  - user-005: Morgan Lee (The Analyst)")
        print("\nYou can now test matching functionality with these users!")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\nError during seeding: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
