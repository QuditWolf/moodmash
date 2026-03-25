# MoodMash Deployment Guide

This guide covers deploying MoodMash to production on AWS.

## Pre-Deployment Checklist

- [ ] All tests pass (`python3 test_api.py`)
- [ ] Frontend builds without errors (`cd frontend && npm run build`)
- [ ] Backend runs without errors
- [ ] Environment variables configured
- [ ] AWS credentials configured
- [ ] Domain name registered (optional)

## Architecture Overview

```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  AWS Amplify    │  ← Frontend (React)
│  (Static Host)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  API Gateway    │  ← REST API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AWS Lambda     │  ← Backend (FastAPI)
│  (Python 3.10)  │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│DynamoDB │ │ Bedrock  │
│(Storage)│ │   (AI)   │
└─────────┘ └──────────┘
```

## Step 1: Prepare Backend for Lambda

### 1.1 Update requirements.txt

Ensure `backend/requirements.txt` includes:
```
fastapi==0.115.0
uvicorn[standard]==0.30.1
mangum==0.17.0
pydantic==2.9.0
python-multipart==0.0.9
boto3==1.35.0
```

### 1.2 Uncomment Lambda Handler

In `backend/main.py`, uncomment:
```python
from mangum import Mangum
lambda_handler = Mangum(app)
```

### 1.3 Create SAM Template

The `backend/template.yaml` should define:
- Lambda function with Python 3.10 runtime
- API Gateway HTTP API
- DynamoDB tables (taste_profiles, path_completions)
- IAM roles with Bedrock + DynamoDB permissions
- Environment variables

## Step 2: Deploy Backend with SAM

### 2.1 Install SAM CLI

```bash
pip install aws-sam-cli
```

### 2.2 Configure AWS Credentials

```bash
aws configure
# Enter:
# - AWS Access Key ID
# - AWS Secret Access Key
# - Default region: ap-south-1
# - Default output format: json
```

### 2.3 Build and Deploy

```bash
cd backend

# Build
sam build

# Deploy (first time - guided)
sam deploy --guided

# Follow prompts:
# - Stack Name: moodmash-backend
# - AWS Region: ap-south-1
# - Confirm changes: Y
# - Allow SAM CLI IAM role creation: Y
# - Save arguments to config: Y

# Subsequent deploys
sam deploy
```

### 2.4 Get API Endpoint

After deployment, SAM will output the API Gateway URL:
```
Outputs:
  ApiUrl: https://xxxxxxxxxx.execute-api.ap-south-1.amazonaws.com/
```

Save this URL - you'll need it for frontend configuration.

## Step 3: Enable Bedrock

### 3.1 Request Model Access

1. Go to AWS Console → Bedrock
2. Navigate to "Model access"
3. Request access to:
   - Amazon Titan Embeddings G1 - Text
   - Anthropic Claude 3 Sonnet

### 3.2 Update Lambda Environment Variables

```bash
aws lambda update-function-configuration \
  --function-name moodmash-backend-Function \
  --environment Variables="{USE_MOCK=false,USE_DYNAMODB=true,AWS_REGION=ap-south-1}"
```

### 3.3 Implement Bedrock Calls

In `backend/lib/ai.py`, implement the `_bedrock_*` functions:

```python
import boto3
import json

bedrock_runtime = boto3.client('bedrock-runtime', region_name='ap-south-1')

def _bedrock_generate_archetype(taste_signals, quiz_answers):
    """Call Bedrock Claude to generate archetype."""
    # Load prompt from prompts/dna.prompt.md
    # Format with taste_signals
    # Call bedrock_runtime.invoke_model()
    # Parse response
    pass
```

## Step 4: Deploy Frontend to Amplify

### 4.1 Build Frontend

```bash
cd frontend

# Update .env.production
echo "VITE_API_URL=https://YOUR_API_GATEWAY_URL" > .env.production

# Build
npm run build
```

### 4.2 Create Amplify App

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize Amplify
amplify init

# Add hosting
amplify add hosting
# Choose: Hosting with Amplify Console
# Choose: Manual deployment

# Publish
amplify publish
```

### 4.3 Configure Amplify Console

1. Go to AWS Console → Amplify
2. Select your app
3. Go to "Build settings"
4. Update build spec:

```yaml
version: 1
frontend:
  phases:
    preBuild:
      commands:
        - cd frontend
        - npm ci
    build:
      commands:
        - npm run build
  artifacts:
    baseDirectory: frontend/dist
    files:
      - '**/*'
  cache:
    paths:
      - frontend/node_modules/**/*
```

5. Add environment variable:
   - Key: `VITE_API_URL`
   - Value: Your API Gateway URL

### 4.4 Set Up Custom Domain (Optional)

1. Go to Amplify Console → Domain management
2. Add domain
3. Follow DNS configuration steps

## Step 5: Configure DynamoDB

### 5.1 Verify Tables Created

```bash
aws dynamodb list-tables
```

Should show:
- `taste_profiles`
- `path_completions`

### 5.2 Enable TTL (Optional)

For auto-expiring sessions after 7 days:

```bash
aws dynamodb update-time-to-live \
  --table-name taste_profiles \
  --time-to-live-specification "Enabled=true, AttributeName=ttl"
```

### 5.3 Set Up Backups (Recommended)

```bash
aws dynamodb update-continuous-backups \
  --table-name taste_profiles \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true
```

## Step 6: Upload Knowledge Base to S3

### 6.1 Create S3 Bucket

```bash
aws s3 mb s3://moodmash-knowledge-base-ap-south-1
```

### 6.2 Upload Content

```bash
aws s3 cp knowledge-base/content.json s3://moodmash-knowledge-base-ap-south-1/content.json
```

### 6.3 Update Lambda to Read from S3

In `backend/functions/get_path.py`:

```python
import boto3
import json

s3 = boto3.client('s3')

def _load_content():
    """Load content from S3."""
    response = s3.get_object(
        Bucket='moodmash-knowledge-base-ap-south-1',
        Key='content.json'
    )
    return json.loads(response['Body'].read())
```

## Step 7: Set Up Monitoring

### 7.1 CloudWatch Logs

Lambda logs are automatically sent to CloudWatch. View them:

```bash
aws logs tail /aws/lambda/moodmash-backend-Function --follow
```

### 7.2 CloudWatch Alarms

Create alarms for:
- Lambda errors > 10 in 5 minutes
- API Gateway 5xx errors > 5 in 5 minutes
- DynamoDB throttling

### 7.3 X-Ray Tracing (Optional)

Enable in SAM template:
```yaml
Tracing: Active
```

## Step 8: Security Hardening

### 8.1 API Gateway Throttling

```yaml
ApiGatewayApi:
  Type: AWS::Serverless::HttpApi
  Properties:
    DefaultRouteSettings:
      ThrottlingBurstLimit: 100
      ThrottlingRateLimit: 50
```

### 8.2 CORS Configuration

In `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-amplify-domain.amplifyapp.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 8.3 DynamoDB Encryption

Enable encryption at rest (enabled by default).

### 8.4 Secrets Management

For sensitive data (API keys), use AWS Secrets Manager:

```bash
aws secretsmanager create-secret \
  --name moodmash/spotify-credentials \
  --secret-string '{"client_id":"xxx","client_secret":"yyy"}'
```

## Step 9: Testing Production

### 9.1 Smoke Test

```bash
# Health check
curl https://YOUR_API_URL/health

# Onboard
curl -X POST https://YOUR_API_URL/api/onboard \
  -H "Content-Type: application/json" \
  -d '{"quiz_answers":{"music_album":["test"]},"goal":"test"}'
```

### 9.2 Load Test (Optional)

Use Apache Bench or Artillery:

```bash
ab -n 1000 -c 10 https://YOUR_API_URL/health
```

### 9.3 End-to-End Test

1. Visit your Amplify URL
2. Complete full user flow
3. Verify all features work

## Step 10: Post-Deployment

### 10.1 Update README

Update README.md with production URLs:
- Frontend: `https://your-app.amplifyapp.com`
- API: `https://your-api.execute-api.ap-south-1.amazonaws.com`

### 10.2 Set Up CI/CD (Optional)

Connect GitHub to Amplify for auto-deploy on push:
1. Amplify Console → App settings → Build settings
2. Connect repository
3. Configure branch (main/master)

### 10.3 Monitor Costs

Set up billing alerts:
```bash
aws budgets create-budget \
  --account-id YOUR_ACCOUNT_ID \
  --budget file://budget.json
```

## Rollback Procedure

If deployment fails:

```bash
# Rollback backend
sam deploy --parameter-overrides Version=previous

# Rollback frontend
amplify console
# → Deployments → Select previous version → Redeploy
```

## Cost Estimation

Monthly costs (assuming 1000 users, 10 sessions/user):

| Service | Usage | Cost |
|---------|-------|------|
| Lambda | 10K invocations, 512MB, 1s avg | ~$0.20 |
| API Gateway | 10K requests | ~$0.04 |
| DynamoDB | 10K reads, 10K writes | ~$1.25 |
| Bedrock | 10K Claude calls | ~$30.00 |
| Amplify | Static hosting | ~$0.15 |
| S3 | 1GB storage, 10K requests | ~$0.03 |
| **Total** | | **~$31.67/month** |

Free tier covers most of this for first 12 months.

## Troubleshooting

### Lambda timeout
- Increase timeout in SAM template (default: 30s, max: 900s)
- Optimize cold start by reducing dependencies

### DynamoDB throttling
- Increase provisioned capacity
- Or switch to on-demand billing

### Bedrock rate limits
- Implement exponential backoff
- Cache responses when possible

### CORS errors
- Verify allow_origins matches Amplify domain
- Check API Gateway CORS configuration

## Support

For issues:
1. Check CloudWatch logs
2. Review SAM deployment logs
3. Test API endpoints directly
4. Verify environment variables

---

**Deployment Complete! 🚀**

Your MoodMash app is now live and serving users!
