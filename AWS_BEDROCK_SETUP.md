# AWS Bedrock Setup Guide

This guide explains how to set up AWS Bedrock to test the VibeGraph backend with real AI capabilities.

## Prerequisites

- AWS Account (free tier or paid)
- AWS CLI installed (optional but recommended)
- Docker and Docker Compose installed

## Step 1: Create AWS Account

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow the registration process
4. Add payment method (required even for free tier)

## Step 2: Enable AWS Bedrock Access

### 2.1 Request Model Access

1. Log in to AWS Console
2. Navigate to **AWS Bedrock** service
3. Go to **Model access** in the left sidebar
4. Click **Manage model access** or **Request model access**
5. Enable the following models:

   **Required Models:**
   - ✅ **Claude 3.5 Sonnet** (anthropic.claude-3-5-sonnet-20241022-v2:0)
     - Used for: Quiz questions, DNA generation, growth paths, analytics
   - ✅ **Titan Embeddings G1 - Text v2** (amazon.titan-embed-text-v2:0)
     - Used for: Generating taste embeddings
   
   **For DNA Card Images (choose one):**
   - ✅ **Amazon Titan Image Generator** (amazon.titan-image-generator-v1)
     - Faster, good quality, lower cost
   - ✅ **Stable Diffusion XL** (stability.stable-diffusion-xl-v1)
     - Slower, higher quality, higher cost

6. Click **Request model access**
7. Wait for approval (usually instant for most models)

### 2.2 Verify Model Access

```bash
aws bedrock list-foundation-models --region us-east-1
```

You should see the models listed above in the output.

## Step 3: Create IAM User with Bedrock Permissions

### 3.1 Create IAM User

1. Go to **IAM** service in AWS Console
2. Click **Users** → **Add users**
3. User name: `vibegraph-bedrock-user`
4. Select **Access key - Programmatic access**
5. Click **Next: Permissions**

### 3.2 Attach Policies

Attach the following policies:

1. **AmazonBedrockFullAccess** (for Bedrock access)
2. **AmazonDynamoDBFullAccess** (for DynamoDB access)

Or create a custom policy with minimal permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListFoundationModels"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem",
        "dynamodb:Scan",
        "dynamodb:Query",
        "dynamodb:DescribeTable",
        "dynamodb:CreateTable",
        "dynamodb:DeleteTable"
      ],
      "Resource": "arn:aws:dynamodb:*:*:table/vibegraph-*"
    }
  ]
}
```

### 3.3 Save Credentials

1. Click **Create user**
2. **IMPORTANT:** Save the **Access Key ID** and **Secret Access Key**
3. You won't be able to see the secret key again!

Example:
```
Access Key ID: AKIAIOSFODNN7EXAMPLE
Secret Access Key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

## Step 4: Configure VibeGraph Backend

### 4.1 Create `.env` File

Create a `.env` file in the project root:

```bash
# AWS Credentials
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1

# Bedrock Models
CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
TITAN_MODEL=amazon.titan-embed-text-v2:0
TITAN_IMAGE_MODEL=amazon.titan-image-generator-v1
SDXL_MODEL=stability.stable-diffusion-xl-v1

# DynamoDB Tables
USERS_TABLE=vibegraph-users
SESSIONS_TABLE=vibegraph-sessions
CACHE_TABLE=vibegraph-embedding-cache

# Logging
LOG_LEVEL=INFO
```

### 4.2 Update Docker Compose for Real AWS

Edit `docker-compose.override.yml` and **comment out or remove** the `BEDROCK_ENDPOINT` override:

```yaml
backend-api:
  environment:
    # Comment out LocalStack endpoint to use real AWS
    # - BEDROCK_ENDPOINT=http://localstack:4566
    
    # Add real AWS credentials from .env
    - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
    - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    - AWS_REGION=${AWS_REGION}
```

Do the same for `backend-handlers` service.

### 4.3 Use Real DynamoDB (Optional)

If you want to use real AWS DynamoDB instead of DynamoDB Local:

1. Create tables in AWS DynamoDB Console or use AWS CLI
2. Update `docker-compose.override.yml`:

```yaml
backend-api:
  environment:
    # Comment out DynamoDB Local endpoint
    # - DYNAMODB_ENDPOINT=http://dynamodb-local:8000
    
    # Tables will use real AWS DynamoDB
    - USERS_TABLE=vibegraph-users
    - SESSIONS_TABLE=vibegraph-sessions
    - CACHE_TABLE=vibegraph-embedding-cache
```

## Step 5: Test the Setup

### 5.1 Restart Containers

```bash
# Stop containers
docker-compose down

# Rebuild with new configuration
docker-compose build backend-api

# Start containers
docker-compose up -d

# Check logs
docker-compose logs -f backend-api
```

### 5.2 Test Health Check

```bash
curl http://localhost:8000/health/ready | jq .
```

You should see:
```json
{
  "status": "ready",
  "dependencies": {
    "bedrock": {
      "status": "healthy"
    }
  }
}
```

### 5.3 Test Quiz Generation (Claude)

```bash
curl -X POST http://localhost:8000/quiz/section1/start \
  -H "Content-Type: application/json" \
  -d '{}' | jq .
```

Expected response:
```json
{
  "sessionId": "uuid-here",
  "questions": [
    {
      "id": "q1",
      "text": "What type of content do you...",
      "options": ["Option 1", "Option 2", ...]
    }
  ]
}
```

### 5.4 Test DNA Card Image Generation

First, complete a quiz to create a user with DNA profile, then:

```bash
curl -X POST "http://localhost:8000/profile/dna-card/test-user-123?model=titan" \
  -H "Content-Type: application/json" | jq .
```

Expected response:
```json
{
  "imageId": "dna-card-test-user-123-1234567890",
  "imageData": "base64-encoded-image-data...",
  "format": "png",
  "width": 1024,
  "height": 1024,
  "model": "amazon.titan-image-generator-v1",
  "userId": "test-user-123",
  "archetype": "Dream Liminalist"
}
```

### 5.5 Run Full Integration Test

```bash
bash backend/scripts/test_api_flow.sh
```

All tests should pass!

## Step 6: Cost Estimation

### Bedrock Pricing (us-east-1, as of 2024)

**Claude 3.5 Sonnet:**
- Input: $3.00 per 1M tokens
- Output: $15.00 per 1M tokens
- Typical quiz generation: ~500 tokens = $0.0075

**Titan Embeddings v2:**
- $0.0001 per 1K tokens
- Typical embedding: ~200 tokens = $0.00002

**Titan Image Generator:**
- $0.008 per image (1024x1024)

**Stable Diffusion XL:**
- $0.04 per image (1024x1024)

### Example Usage with 100 Credits

With $100 AWS credits, you can generate approximately:
- **33,000 quiz sessions** (Claude)
- **5,000,000 embeddings** (Titan)
- **12,500 DNA card images** (Titan Image)
- **2,500 DNA card images** (Stable Diffusion XL)

## Troubleshooting

### Error: "Model access denied"

**Solution:** Go to AWS Bedrock Console → Model access → Request access for the specific model.

### Error: "Throttling exception"

**Solution:** You're hitting rate limits. Wait a few seconds and retry. Consider implementing exponential backoff (already built into the code).

### Error: "Invalid credentials"

**Solution:** 
1. Verify AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in `.env`
2. Check IAM user has correct permissions
3. Ensure credentials are not expired

### Error: "Region not supported"

**Solution:** Bedrock is not available in all regions. Use `us-east-1` (recommended) or check https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html

### LocalStack Still Being Used

**Solution:**
1. Check `docker-compose.override.yml` - ensure `BEDROCK_ENDPOINT` is commented out
2. Restart containers: `docker-compose restart backend-api`
3. Check logs: `docker-compose logs backend-api | grep -i bedrock`

## Security Best Practices

1. **Never commit `.env` file** - it's already in `.gitignore`
2. **Rotate credentials regularly** - every 90 days
3. **Use IAM roles** in production instead of access keys
4. **Enable CloudTrail** to monitor API usage
5. **Set up billing alerts** to avoid unexpected charges

## Next Steps

1. ✅ Test all 8 API endpoints with real AWS Bedrock
2. ✅ Generate DNA card images and verify quality
3. ✅ Monitor costs in AWS Billing Dashboard
4. 🚀 Deploy to production (Lambda + API Gateway)

## Support

If you encounter issues:
1. Check AWS Bedrock service health: https://status.aws.amazon.com/
2. Review CloudWatch logs in AWS Console
3. Check container logs: `docker-compose logs -f backend-api`
4. Verify model access in Bedrock Console

---

**Ready to test!** Follow the steps above and your VibeGraph backend will be powered by real AWS Bedrock AI. 🚀
