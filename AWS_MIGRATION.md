# AWS Migration Guide

Complete guide for migrating VibeGraph from local Docker development to AWS production infrastructure.

## Overview

This guide covers the migration path from the local Docker-based development environment to a production AWS deployment using:

- **AWS Lambda** for serverless compute (handlers)
- **Amazon DynamoDB** for database
- **Amazon Bedrock** for AI/ML models
- **AWS API Gateway** for API management
- **Amazon S3 + CloudFront** for frontend hosting
- **AWS CloudWatch** for logging and monitoring

## Architecture Comparison

### Local Development (Current)
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│  Backend API │────▶│  DynamoDB   │
│   (nginx)   │     │  (FastAPI)   │     │   Local     │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │  LocalStack  │
                    │  (Bedrock)   │
                    └──────────────┘
```

### AWS Production (Target)
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ CloudFront  │────▶│ API Gateway  │────▶│  DynamoDB   │
│  + S3       │     │  + Lambda    │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   Bedrock    │
                    │              │
                    └──────────────┘
```

## Prerequisites

### AWS Account Setup

1. **AWS Account** with appropriate permissions
2. **AWS CLI** installed and configured
3. **AWS SAM CLI** for Lambda deployment
4. **Terraform** or **AWS CDK** (optional, for IaC)

### Required AWS Services Access

- Lambda
- API Gateway
- DynamoDB
- Bedrock
- S3
- CloudFront
- CloudWatch
- IAM
- Systems Manager (Parameter Store)

### Install AWS CLI

```bash
# macOS
brew install awscli

# Linux
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure
aws configure
```

## Migration Steps

### Phase 1: AWS Account Preparation

#### 1.1 Create IAM Roles

**Lambda Execution Role:**

```bash
# Create Lambda execution role
aws iam create-role \
  --role-name VibegraphLambdaExecutionRole \
  --assume-role-policy-document file://policies/lambda-trust-policy.json

# Attach policies
aws iam attach-role-policy \
  --role-name VibegraphLambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
  --role-name VibegraphLambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess

aws iam attach-role-policy \
  --role-name VibegraphLambdaExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
```

**Trust Policy (lambda-trust-policy.json):**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### 1.2 Enable Bedrock Models

```bash
# Request access to Claude and Titan models in AWS Console
# Navigate to: Bedrock > Model access > Request model access
# Select:
# - Anthropic Claude 3.5 Sonnet
# - Amazon Titan Embeddings G1 - Text v2
```

### Phase 2: Database Migration

#### 2.1 Create DynamoDB Tables

**Users Table:**
```bash
aws dynamodb create-table \
  --table-name vibegraph-users-prod \
  --attribute-definitions \
    AttributeName=userId,AttributeType=S \
  --key-schema \
    AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --tags Key=Environment,Value=production Key=Application,Value=vibegraph
```

**Sessions Table:**
```bash
aws dynamodb create-table \
  --table-name vibegraph-sessions-prod \
  --attribute-definitions \
    AttributeName=sessionId,AttributeType=S \
    AttributeName=userId,AttributeType=S \
  --key-schema \
    AttributeName=sessionId,KeyType=HASH \
  --global-secondary-indexes \
    '[{
      "IndexName": "UserIdIndex",
      "KeySchema": [{"AttributeName":"userId","KeyType":"HASH"}],
      "Projection": {"ProjectionType":"ALL"}
    }]' \
  --billing-mode PAY_PER_REQUEST \
  --tags Key=Environment,Value=production Key=Application,Value=vibegraph
```

**Cache Table:**
```bash
aws dynamodb create-table \
  --table-name vibegraph-embedding-cache-prod \
  --attribute-definitions \
    AttributeName=cacheKey,AttributeType=S \
  --key-schema \
    AttributeName=cacheKey,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --time-to-live-specification \
    Enabled=true,AttributeName=ttl \
  --tags Key=Environment,Value=production Key=Application,Value=vibegraph
```

#### 2.2 Data Migration (if needed)

```bash
# Export from local DynamoDB
aws dynamodb scan \
  --table-name vibegraph-users \
  --endpoint-url http://localhost:8001 \
  --region us-east-1 \
  --no-sign-request \
  > users-export.json

# Import to AWS DynamoDB
# Use AWS Data Pipeline or custom script
python scripts/migrate-dynamodb-data.py \
  --source-file users-export.json \
  --target-table vibegraph-users-prod
```

### Phase 3: Backend Migration

#### 3.1 Package Lambda Functions

**Create deployment package:**
```bash
cd backend

# Install dependencies
pip install -r api/requirements.txt -t package/
pip install -r handlers/requirements.txt -t package/
pip install -r services/requirements.txt -t package/

# Copy source code
cp -r src/ package/
cp -r api/ package/
cp -r handlers/ package/
cp -r services/ package/

# Create ZIP
cd package
zip -r ../vibegraph-lambda.zip .
cd ..
```

#### 3.2 Deploy Lambda Functions

**API Handler Lambda:**
```bash
aws lambda create-function \
  --function-name vibegraph-api-handler \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/VibegraphLambdaExecutionRole \
  --handler api.main.handler \
  --zip-file fileb://vibegraph-lambda.zip \
  --timeout 30 \
  --memory-size 512 \
  --environment Variables="{
    USERS_TABLE=vibegraph-users-prod,
    SESSIONS_TABLE=vibegraph-sessions-prod,
    CACHE_TABLE=vibegraph-embedding-cache-prod,
    CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0,
    TITAN_MODEL=amazon.titan-embed-text-v2:0,
    LOG_LEVEL=INFO
  }"
```

**Quiz Handler Lambda:**
```bash
aws lambda create-function \
  --function-name vibegraph-quiz-handler \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/VibegraphLambdaExecutionRole \
  --handler handlers.generate_section1.handler \
  --zip-file fileb://vibegraph-lambda.zip \
  --timeout 60 \
  --memory-size 1024 \
  --environment Variables="{
    USERS_TABLE=vibegraph-users-prod,
    SESSIONS_TABLE=vibegraph-sessions-prod,
    CACHE_TABLE=vibegraph-embedding-cache-prod,
    CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0
  }"
```

#### 3.3 Create API Gateway

**REST API:**
```bash
# Create API
aws apigateway create-rest-api \
  --name vibegraph-api \
  --description "VibeGraph API Gateway" \
  --endpoint-configuration types=REGIONAL

# Get API ID
API_ID=$(aws apigateway get-rest-apis \
  --query "items[?name=='vibegraph-api'].id" \
  --output text)

# Create resources and methods
# (Use AWS Console or SAM template for easier configuration)
```

**Or use SAM template (recommended):**
```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  VibegraphApi:
    Type: AWS::Serverless::Api
    Properties:
      StageName: prod
      Cors:
        AllowOrigin: "'*'"
        AllowHeaders: "'*'"
        AllowMethods: "'GET,POST,PUT,DELETE,OPTIONS'"

  ApiHandlerFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: vibegraph-api-handler
      Runtime: python3.11
      Handler: api.main.handler
      CodeUri: ./package
      Timeout: 30
      MemorySize: 512
      Environment:
        Variables:
          USERS_TABLE: vibegraph-users-prod
          SESSIONS_TABLE: vibegraph-sessions-prod
          CACHE_TABLE: vibegraph-embedding-cache-prod
      Events:
        ApiEvent:
          Type: Api
          Properties:
            RestApiId: !Ref VibegraphApi
            Path: /{proxy+}
            Method: ANY
```

Deploy with SAM:
```bash
sam build
sam deploy --guided
```

### Phase 4: Frontend Migration

#### 4.1 Build Frontend for Production

```bash
cd frontend

# Update API URL for production
echo "VITE_API_URL=https://api.vibegraph.com" > .env.production

# Build
npm run build

# Output will be in dist/
```

#### 4.2 Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://vibegraph-frontend-prod

# Enable static website hosting
aws s3 website s3://vibegraph-frontend-prod \
  --index-document index.html \
  --error-document index.html

# Upload build
aws s3 sync dist/ s3://vibegraph-frontend-prod/ \
  --delete \
  --cache-control "public, max-age=31536000, immutable"

# Set index.html cache
aws s3 cp dist/index.html s3://vibegraph-frontend-prod/index.html \
  --cache-control "public, max-age=0, must-revalidate"
```

#### 4.3 Configure CloudFront

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name vibegraph-frontend-prod.s3.amazonaws.com \
  --default-root-object index.html

# Get distribution ID
DIST_ID=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?Origins.Items[0].DomainName=='vibegraph-frontend-prod.s3.amazonaws.com'].Id" \
  --output text)

# Configure custom error responses for SPA routing
aws cloudfront update-distribution \
  --id $DIST_ID \
  --distribution-config file://cloudfront-config.json
```

**CloudFront Configuration (cloudfront-config.json):**
```json
{
  "CustomErrorResponses": {
    "Items": [
      {
        "ErrorCode": 404,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200",
        "ErrorCachingMinTTL": 300
      },
      {
        "ErrorCode": 403,
        "ResponsePagePath": "/index.html",
        "ResponseCode": "200",
        "ErrorCachingMinTTL": 300
      }
    ]
  }
}
```

### Phase 5: Configuration & Secrets

#### 5.1 Store Secrets in Parameter Store

```bash
# Store sensitive configuration
aws ssm put-parameter \
  --name /vibegraph/prod/api-key \
  --value "your-api-key" \
  --type SecureString

aws ssm put-parameter \
  --name /vibegraph/prod/jwt-secret \
  --value "your-jwt-secret" \
  --type SecureString

# Update Lambda to read from Parameter Store
```

#### 5.2 Environment Variables

Update Lambda environment variables:
```bash
aws lambda update-function-configuration \
  --function-name vibegraph-api-handler \
  --environment Variables="{
    ENVIRONMENT=production,
    USERS_TABLE=vibegraph-users-prod,
    SESSIONS_TABLE=vibegraph-sessions-prod,
    CACHE_TABLE=vibegraph-embedding-cache-prod,
    CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0,
    TITAN_MODEL=amazon.titan-embed-text-v2:0,
    LOG_LEVEL=INFO,
    CORS_ORIGINS=https://vibegraph.com
  }"
```

### Phase 6: Monitoring & Logging

#### 6.1 CloudWatch Logs

Lambda functions automatically log to CloudWatch. Configure log retention:

```bash
# Set log retention
aws logs put-retention-policy \
  --log-group-name /aws/lambda/vibegraph-api-handler \
  --retention-in-days 30

aws logs put-retention-policy \
  --log-group-name /aws/lambda/vibegraph-quiz-handler \
  --retention-in-days 30
```

#### 6.2 CloudWatch Alarms

```bash
# Create alarm for Lambda errors
aws cloudwatch put-metric-alarm \
  --alarm-name vibegraph-lambda-errors \
  --alarm-description "Alert on Lambda errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 10 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=vibegraph-api-handler

# Create alarm for DynamoDB throttling
aws cloudwatch put-metric-alarm \
  --alarm-name vibegraph-dynamodb-throttles \
  --alarm-description "Alert on DynamoDB throttling" \
  --metric-name UserErrors \
  --namespace AWS/DynamoDB \
  --statistic Sum \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=TableName,Value=vibegraph-users-prod
```

#### 6.3 X-Ray Tracing

Enable X-Ray for Lambda:
```bash
aws lambda update-function-configuration \
  --function-name vibegraph-api-handler \
  --tracing-config Mode=Active
```

### Phase 7: Domain & SSL

#### 7.1 Request SSL Certificate

```bash
# Request certificate in us-east-1 (required for CloudFront)
aws acm request-certificate \
  --domain-name vibegraph.com \
  --subject-alternative-names www.vibegraph.com api.vibegraph.com \
  --validation-method DNS \
  --region us-east-1

# Validate via DNS (follow instructions in ACM console)
```

#### 7.2 Configure Custom Domain

**For CloudFront (Frontend):**
```bash
# Update CloudFront distribution with custom domain
aws cloudfront update-distribution \
  --id $DIST_ID \
  --aliases vibegraph.com,www.vibegraph.com \
  --viewer-certificate ACMCertificateArn=arn:aws:acm:...,SSLSupportMethod=sni-only
```

**For API Gateway:**
```bash
# Create custom domain
aws apigateway create-domain-name \
  --domain-name api.vibegraph.com \
  --certificate-arn arn:aws:acm:...

# Create base path mapping
aws apigateway create-base-path-mapping \
  --domain-name api.vibegraph.com \
  --rest-api-id $API_ID \
  --stage prod
```

#### 7.3 Update DNS

Add CNAME records in your DNS provider:
```
vibegraph.com       CNAME  d123456.cloudfront.net
www.vibegraph.com   CNAME  d123456.cloudfront.net
api.vibegraph.com   CNAME  d-abc123.execute-api.us-east-1.amazonaws.com
```

## Cost Optimization

### DynamoDB

- Use **On-Demand** billing for unpredictable workloads
- Switch to **Provisioned** capacity with auto-scaling for predictable traffic
- Enable **Point-in-Time Recovery** for production data

### Lambda

- Right-size memory allocation (test different sizes)
- Use **Provisioned Concurrency** for latency-sensitive functions
- Enable **Lambda SnapStart** for faster cold starts (Java only)

### S3 & CloudFront

- Use **S3 Intelligent-Tiering** for automatic cost optimization
- Enable **CloudFront compression**
- Set appropriate **cache TTLs**

### Bedrock

- Cache embeddings in DynamoDB to reduce API calls
- Use **batch processing** where possible
- Monitor token usage and optimize prompts

## Security Best Practices

### IAM

- Follow **principle of least privilege**
- Use **IAM roles** instead of access keys
- Enable **MFA** for console access
- Rotate credentials regularly

### API Security

- Enable **API Gateway throttling**
- Use **AWS WAF** for DDoS protection
- Implement **request validation**
- Use **API keys** or **Cognito** for authentication

### Data Security

- Enable **DynamoDB encryption at rest**
- Use **VPC endpoints** for private connectivity
- Enable **CloudTrail** for audit logging
- Implement **backup strategy**

### Network Security

- Use **Security Groups** to restrict access
- Enable **VPC Flow Logs**
- Use **AWS Shield** for DDoS protection
- Implement **rate limiting**

## Deployment Automation

### CI/CD Pipeline

**GitHub Actions Example:**
```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy Lambda
        run: |
          cd backend
          pip install -r requirements.txt -t package/
          cp -r src/ package/
          cd package && zip -r ../lambda.zip . && cd ..
          aws lambda update-function-code \
            --function-name vibegraph-api-handler \
            --zip-file fileb://lambda.zip
      
      - name: Deploy Frontend
        run: |
          cd frontend
          npm install
          npm run build
          aws s3 sync dist/ s3://vibegraph-frontend-prod/ --delete
          aws cloudfront create-invalidation \
            --distribution-id ${{ secrets.CLOUDFRONT_DIST_ID }} \
            --paths "/*"
```

### Infrastructure as Code

**Terraform Example:**
```hcl
# main.tf
provider "aws" {
  region = "us-east-1"
}

resource "aws_dynamodb_table" "users" {
  name           = "vibegraph-users-prod"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "userId"

  attribute {
    name = "userId"
    type = "S"
  }

  tags = {
    Environment = "production"
    Application = "vibegraph"
  }
}

resource "aws_lambda_function" "api_handler" {
  filename      = "lambda.zip"
  function_name = "vibegraph-api-handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "api.main.handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 512

  environment {
    variables = {
      USERS_TABLE = aws_dynamodb_table.users.name
    }
  }
}
```

## Testing in AWS

### Integration Testing

```bash
# Test API Gateway endpoint
curl https://api.vibegraph.com/health

# Test Lambda directly
aws lambda invoke \
  --function-name vibegraph-api-handler \
  --payload '{"httpMethod":"GET","path":"/health"}' \
  response.json

# Test DynamoDB
aws dynamodb get-item \
  --table-name vibegraph-users-prod \
  --key '{"userId":{"S":"test-user"}}'
```

### Load Testing

```bash
# Use Apache Bench
ab -n 1000 -c 10 https://api.vibegraph.com/health

# Use Artillery
artillery quick --count 10 --num 100 https://api.vibegraph.com/health
```

## Rollback Strategy

### Lambda Versions

```bash
# Publish version
aws lambda publish-version \
  --function-name vibegraph-api-handler

# Create alias
aws lambda create-alias \
  --function-name vibegraph-api-handler \
  --name prod \
  --function-version 1

# Rollback by updating alias
aws lambda update-alias \
  --function-name vibegraph-api-handler \
  --name prod \
  --function-version 1
```

### Frontend Rollback

```bash
# Keep previous build
aws s3 sync s3://vibegraph-frontend-prod/ s3://vibegraph-frontend-backup/

# Rollback
aws s3 sync s3://vibegraph-frontend-backup/ s3://vibegraph-frontend-prod/
aws cloudfront create-invalidation --distribution-id $DIST_ID --paths "/*"
```

## Monitoring & Maintenance

### Daily Checks

- Review CloudWatch dashboards
- Check error rates and latency
- Monitor DynamoDB capacity
- Review cost reports

### Weekly Tasks

- Review CloudWatch Logs Insights
- Analyze X-Ray traces
- Check security advisories
- Review backup status

### Monthly Tasks

- Review and optimize costs
- Update dependencies
- Review IAM policies
- Conduct security audit

## Troubleshooting

### Lambda Issues

```bash
# View logs
aws logs tail /aws/lambda/vibegraph-api-handler --follow

# Check metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=vibegraph-api-handler \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

### DynamoDB Issues

```bash
# Check table status
aws dynamodb describe-table --table-name vibegraph-users-prod

# View metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name ConsumedReadCapacityUnits \
  --dimensions Name=TableName,Value=vibegraph-users-prod \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z \
  --period 3600 \
  --statistics Sum
```

## Additional Resources

- [AWS Lambda Best Practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [API Gateway Best Practices](https://docs.aws.amazon.com/apigateway/latest/developerguide/best-practices.html)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)

## Support

For migration assistance:
- AWS Support (if you have a support plan)
- AWS Professional Services
- Development team documentation
- Community forums

## Conclusion

This migration guide provides a comprehensive path from local Docker development to AWS production. Follow the phases sequentially, test thoroughly at each step, and monitor closely after deployment.

Remember to:
- Start with a staging environment
- Test thoroughly before production
- Have a rollback plan ready
- Monitor costs and performance
- Keep documentation updated
