#!/usr/bin/env python3
"""Check available Bedrock image generation models"""

import boto3
import os

# Set AWS credentials from environment or .env file
# Make sure to set these in your environment:
# export AWS_ACCESS_KEY_ID=your-key
# export AWS_SECRET_ACCESS_KEY=your-secret
# export AWS_REGION=us-east-1

try:
    client = boto3.client('bedrock', region_name='us-east-1')
    
    # List all foundation models
    response = client.list_foundation_models()
    
    # Filter for image generation models
    image_models = []
    for model in response['modelSummaries']:
        if 'IMAGE' in model.get('outputModalities', []):
            status = model.get('modelLifecycle', {}).get('status', 'UNKNOWN')
            image_models.append({
                'id': model['modelId'],
                'name': model['modelName'],
                'provider': model['providerName'],
                'status': status
            })
    
    print("Available Image Generation Models in us-east-1:")
    print("=" * 80)
    
    if image_models:
        for model in image_models:
            print(f"Provider: {model['provider']}")
            print(f"Model ID: {model['id']}")
            print(f"Name: {model['name']}")
            print(f"Status: {model['status']}")
            print("-" * 80)
    else:
        print("No image generation models found or available")
        print("\nNote: You may need to enable models in the AWS Bedrock console:")
        print("https://console.aws.amazon.com/bedrock/home?region=us-east-1#/modelaccess")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
