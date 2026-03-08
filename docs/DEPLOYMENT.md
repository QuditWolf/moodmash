# Deployment Guide

This guide covers production deployment of the VibeGraph application, including security considerations, environment configuration, health monitoring, and backup/recovery procedures.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Deployment Architecture](#deployment-architecture)
- [Pre-Deployment Checklist](#pre-deployment-checklist)
- [Production Deployment Steps](#production-deployment-steps)
- [Environment Configuration](#environment-configuration)
- [Security Considerations](#security-considerations)
- [Health Check Monitoring](#health-check-monitoring)
- [Backup and Recovery](#backup-and-recovery)
- [Scaling and Performance](#scaling-and-performance)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Infrastructure Requirements

- **Container Orchestration**: Kubernetes, ECS, or Docker Swarm
- **Load Balancer**: Application Load Balancer (ALB) or equivalent
- **Database**: AWS DynamoDB (production) or DynamoDB-compatible service
- **AI Services**: AWS Bedrock with Claude 3.5 Sonnet and Titan v2 access
- **Storage**: S3 or equivalent for logs and backups
- **Monitoring**: CloudWatch, Datadog, or equivalent
- **Secrets Management**: AWS Secrets Manager, HashiCorp Vault, or equivalent

### Access Requirements

- AWS account with appropriate IAM permissions
- Container registry access (ECR, Docker Hub, etc.)
- Domain name and SSL certificate
- CI/CD pipeline configured

### Software Requirements

- Docker 20.10+
- kubectl (for Kubernetes) or AWS CLI (for ECS)
- Terraform or CloudFormation (for infrastructure as code)

## Deployment Architecture

### Production Architecture

```
                    ┌─────────────┐
                    │   Route 53  │
                    │     DNS     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │     ALB     │
                    │  (SSL/TLS)  │
                    └──────┬──────┘
                           │
        ┏━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━┓
        ▼                                    ▼
┌───────────────┐                   ┌───────────────┐
│   Frontend    │                   │  Backend API  │
│   (ECS/K8s)   │                   │   (ECS/K8s)   │
│   Port 3000   │                   │   Port 8000   │
└───────────────┘                   └───────┬───────┘
                                            │
                        ┏━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━┓
                        ▼                                        ▼
                ┌───────────────┐                       ┌───────────────┐
                │   DynamoDB    │                       │  AWS Bedrock  │
                │  (Production) │                       │ Claude+Titan  │
                └───────────────┘                       └───────────────┘
```

### High Availability Setup

- **Multi-AZ Deployment**: Deploy containers across multiple availability zones
- **Auto-Scaling**: Configure auto-scaling based on CPU/memory/request metrics
- **Load Balancing**: Use ALB with health checks and sticky sessions
- **Database Replication**: Enable DynamoDB global tables for multi-region
- **Failover**: Configure automatic failover for critical services

## Pre-Deployment Checklist

### Code and Configuration

- [ ] All tests pass: `make test`
- [ ] Code reviewed and approved
- [ ] Version tagged in Git: `git tag v1.0.0`
- [ ] Docker images built and tagged
- [ ] Images pushed to container registry
- [ ] Environment variables configured
- [ ] Secrets stored in secrets manager
- [ ] Database migrations prepared (if any)

### Security

- [ ] Security scan completed on Docker images
- [ ] Dependency vulnerabilities addressed
- [ ] SSL/TLS certificates obtained and configured
- [ ] IAM roles and policies configured
- [ ] CORS settings reviewed and restricted
- [ ] Rate limiting configured
- [ ] API authentication enabled
- [ ] Secrets rotated and secured

### Infrastructure

- [ ] Infrastructure provisioned (VPC, subnets, security groups)
- [ ] Load balancer configured with health checks
- [ ] Auto-scaling policies defined
- [ ] Monitoring and alerting configured
- [ ] Log aggregation set up
- [ ] Backup procedures tested
- [ ] Disaster recovery plan documented

### Documentation

- [ ] Deployment runbook updated
- [ ] Architecture diagrams current
- [ ] API documentation published
- [ ] Monitoring dashboards created
- [ ] Incident response procedures documented

## Production Deployment Steps

### Step 1: Build and Tag Images

```bash
# Set version
export VERSION=1.0.0

# Build images with production optimizations
docker build -t vibegraph-frontend:${VERSION} \
  --target production \
  --build-arg NODE_ENV=production \
  ./frontend

docker build -t vibegraph-backend:${VERSION} \
  --target production \
  --build-arg PYTHON_ENV=production \
  ./backend

# Tag for registry
docker tag vibegraph-frontend:${VERSION} your-registry/vibegraph-frontend:${VERSION}
docker tag vibegraph-backend:${VERSION} your-registry/vibegraph-backend:${VERSION}

# Push to registry
docker push your-registry/vibegraph-frontend:${VERSION}
docker push your-registry/vibegraph-backend:${VERSION}
```

### Step 2: Configure Environment Variables

Create production environment configuration:

**Frontend Environment** (`frontend/.env.production`):
```env
VITE_API_BASE_URL=https://api.vibegraph.com
VITE_ENV=production
VITE_ENABLE_ANALYTICS=true
VITE_LOG_LEVEL=error
```

**Backend Environment** (stored in AWS Secrets Manager):
```env
AWS_REGION=us-east-1
DYNAMODB_ENDPOINT=https://dynamodb.us-east-1.amazonaws.com
BEDROCK_ENDPOINT=https://bedrock-runtime.us-east-1.amazonaws.com
USERS_TABLE=vibegraph-prod-users
SESSIONS_TABLE=vibegraph-prod-sessions
CACHE_TABLE=vibegraph-prod-embedding-cache
LOG_LEVEL=info
JWT_SECRET=<stored-in-secrets-manager>
CORS_ORIGINS=https://vibegraph.com,https://www.vibegraph.com
RATE_LIMIT_PER_MINUTE=100
```

### Step 3: Deploy Database Tables

```bash
# Create DynamoDB tables (using AWS CLI or Terraform)
aws dynamodb create-table \
  --table-name vibegraph-prod-users \
  --attribute-definitions \
    AttributeName=userId,AttributeType=S \
  --key-schema \
    AttributeName=userId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true \
  --sse-specification Enabled=true

# Create Sessions table
aws dynamodb create-table \
  --table-name vibegraph-prod-sessions \
  --attribute-definitions \
    AttributeName=sessionId,AttributeType=S \
  --key-schema \
    AttributeName=sessionId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --sse-specification Enabled=true

# Create Embedding Cache table
aws dynamodb create-table \
  --table-name vibegraph-prod-embedding-cache \
  --attribute-definitions \
    AttributeName=docHash,AttributeType=S \
  --key-schema \
    AttributeName=docHash,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --sse-specification Enabled=true
```

### Step 4: Deploy Containers (ECS Example)

```bash
# Update ECS task definition
aws ecs register-task-definition \
  --cli-input-json file://ecs-task-definition.json

# Update ECS service
aws ecs update-service \
  --cluster vibegraph-prod \
  --service vibegraph-backend \
  --task-definition vibegraph-backend:${VERSION} \
  --desired-count 3 \
  --force-new-deployment

aws ecs update-service \
  --cluster vibegraph-prod \
  --service vibegraph-frontend \
  --task-definition vibegraph-frontend:${VERSION} \
  --desired-count 2 \
  --force-new-deployment

# Wait for deployment to complete
aws ecs wait services-stable \
  --cluster vibegraph-prod \
  --services vibegraph-backend vibegraph-frontend
```

### Step 5: Verify Deployment

```bash
# Check service health
curl https://api.vibegraph.com/health
curl https://api.vibegraph.com/health/ready
curl https://api.vibegraph.com/health/status

# Test API endpoints
curl -X POST https://api.vibegraph.com/api/quiz/section1/start

# Check frontend
curl https://vibegraph.com

# Verify SSL certificate
openssl s_client -connect api.vibegraph.com:443 -servername api.vibegraph.com
```

### Step 6: Enable Monitoring

```bash
# Create CloudWatch alarms
aws cloudwatch put-metric-alarm \
  --alarm-name vibegraph-backend-high-cpu \
  --alarm-description "Alert when CPU exceeds 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold \
  --evaluation-periods 2

# Set up log aggregation
aws logs create-log-group --log-group-name /ecs/vibegraph-prod
```

## Environment Configuration

### Production Environment Variables

#### Frontend Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API URL | `https://api.vibegraph.com` |
| `VITE_ENV` | Environment name | `production` |
| `VITE_ENABLE_ANALYTICS` | Enable analytics | `true` |
| `VITE_LOG_LEVEL` | Logging level | `error` |

#### Backend Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `AWS_REGION` | AWS region | `us-east-1` |
| `DYNAMODB_ENDPOINT` | DynamoDB endpoint | `https://dynamodb.us-east-1.amazonaws.com` |
| `BEDROCK_ENDPOINT` | Bedrock endpoint | `https://bedrock-runtime.us-east-1.amazonaws.com` |
| `USERS_TABLE` | Users table name | `vibegraph-prod-users` |
| `SESSIONS_TABLE` | Sessions table name | `vibegraph-prod-sessions` |
| `CACHE_TABLE` | Cache table name | `vibegraph-prod-embedding-cache` |
| `LOG_LEVEL` | Logging level | `info` |
| `JWT_SECRET` | JWT signing secret | `<from-secrets-manager>` |
| `CORS_ORIGINS` | Allowed CORS origins | `https://vibegraph.com` |
| `RATE_LIMIT_PER_MINUTE` | Rate limit | `100` |

### Secrets Management

Store sensitive values in AWS Secrets Manager:

```bash
# Store JWT secret
aws secretsmanager create-secret \
  --name vibegraph/prod/jwt-secret \
  --secret-string "your-secure-random-secret"

# Store database credentials (if using RDS)
aws secretsmanager create-secret \
  --name vibegraph/prod/db-credentials \
  --secret-string '{"username":"admin","password":"secure-password"}'

# Retrieve secrets in application
aws secretsmanager get-secret-value \
  --secret-id vibegraph/prod/jwt-secret \
  --query SecretString \
  --output text
```

## Security Considerations

### Network Security

1. **VPC Configuration**
   - Deploy containers in private subnets
   - Use NAT Gateway for outbound internet access
   - Configure security groups with least privilege
   - Enable VPC Flow Logs

2. **Load Balancer Security**
   - Enable HTTPS only (redirect HTTP to HTTPS)
   - Use TLS 1.3 minimum
   - Configure security headers (HSTS, CSP, X-Frame-Options)
   - Enable WAF for DDoS protection

3. **CORS Configuration**
   ```python
   # backend/api/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://vibegraph.com", "https://www.vibegraph.com"],
       allow_credentials=True,
       allow_methods=["GET", "POST", "PUT", "DELETE"],
       allow_headers=["*"],
       max_age=3600,
   )
   ```

### Application Security

1. **Authentication and Authorization**
   - Implement JWT token validation
   - Use short-lived tokens (1 hour)
   - Implement refresh token rotation
   - Validate user permissions on all endpoints

2. **Input Validation**
   - Validate all user inputs
   - Sanitize data before processing
   - Use parameterized queries
   - Implement request size limits

3. **Rate Limiting**
   ```python
   # Implement rate limiting per user
   @app.middleware("http")
   async def rate_limit_middleware(request: Request, call_next):
       user_id = get_user_id_from_token(request)
       if not check_rate_limit(user_id, limit=100, window=60):
           raise HTTPException(status_code=429, detail="Rate limit exceeded")
       return await call_next(request)
   ```

4. **Data Encryption**
   - Enable DynamoDB encryption at rest
   - Use TLS for data in transit
   - Encrypt sensitive data in application layer
   - Rotate encryption keys regularly

### Container Security

1. **Image Security**
   - Scan images for vulnerabilities
   - Use minimal base images (Alpine)
   - Run containers as non-root user
   - Keep base images updated

2. **Runtime Security**
   - Use read-only file systems where possible
   - Drop unnecessary Linux capabilities
   - Implement resource limits (CPU, memory)
   - Enable security profiles (AppArmor, SELinux)

### Secrets Management

1. **Never commit secrets to Git**
2. **Use AWS Secrets Manager or equivalent**
3. **Rotate secrets regularly (90 days)**
4. **Audit secret access**
5. **Use IAM roles instead of access keys**

## Health Check Monitoring

### Health Check Endpoints

Configure load balancer health checks:

**Primary Health Check**: `/health`
- **Interval**: 30 seconds
- **Timeout**: 5 seconds
- **Healthy Threshold**: 2 consecutive successes
- **Unhealthy Threshold**: 3 consecutive failures

**Readiness Check**: `/health/ready`
- Checks all dependencies (DynamoDB, Bedrock)
- Used for container readiness probes

**Detailed Status**: `/health/status`
- Returns comprehensive status JSON
- Used for monitoring dashboards

### Monitoring Setup

#### CloudWatch Metrics

Monitor key metrics:

```bash
# CPU Utilization
aws cloudwatch put-metric-alarm \
  --alarm-name vibegraph-high-cpu \
  --metric-name CPUUtilization \
  --threshold 80

# Memory Utilization
aws cloudwatch put-metric-alarm \
  --alarm-name vibegraph-high-memory \
  --metric-name MemoryUtilization \
  --threshold 85

# Request Count
aws cloudwatch put-metric-alarm \
  --alarm-name vibegraph-high-requests \
  --metric-name RequestCount \
  --threshold 10000

# Error Rate
aws cloudwatch put-metric-alarm \
  --alarm-name vibegraph-high-errors \
  --metric-name 5XXError \
  --threshold 50
```

#### Custom Metrics

Log custom application metrics:

```python
# backend/src/utils/metrics.py
import boto3

cloudwatch = boto3.client('cloudwatch')

def log_metric(metric_name, value, unit='Count'):
    cloudwatch.put_metric_data(
        Namespace='VibeGraph',
        MetricData=[{
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit,
            'Timestamp': datetime.utcnow()
        }]
    )

# Usage
log_metric('QuizCompletions', 1)
log_metric('EmbeddingCacheHitRate', 0.75, 'Percent')
log_metric('APIResponseTime', 250, 'Milliseconds')
```

#### Alerting

Configure alerts for critical issues:

1. **Service Down**: Alert when health checks fail
2. **High Error Rate**: Alert when 5XX errors exceed threshold
3. **High Latency**: Alert when P99 latency exceeds 2 seconds
4. **Database Issues**: Alert on DynamoDB throttling or errors
5. **AI Service Issues**: Alert on Bedrock API failures

### Monitoring Dashboard

Create CloudWatch dashboard with:

- Service health status
- Request rate and latency
- Error rates by endpoint
- CPU and memory utilization
- Database performance metrics
- Cache hit rates
- Active user count

## Backup and Recovery

### Database Backup

#### Point-in-Time Recovery

Enable PITR for all DynamoDB tables:

```bash
aws dynamodb update-continuous-backups \
  --table-name vibegraph-prod-users \
  --point-in-time-recovery-specification PointInTimeRecoveryEnabled=true
```

Recovery window: 35 days

#### On-Demand Backups

Create manual backups before major changes:

```bash
# Create backup
aws dynamodb create-backup \
  --table-name vibegraph-prod-users \
  --backup-name vibegraph-users-backup-$(date +%Y%m%d)

# List backups
aws dynamodb list-backups --table-name vibegraph-prod-users

# Restore from backup
aws dynamodb restore-table-from-backup \
  --target-table-name vibegraph-prod-users-restored \
  --backup-arn arn:aws:dynamodb:us-east-1:123456789012:table/vibegraph-prod-users/backup/01234567890123-abcdefgh
```

#### Automated Backup Schedule

Use AWS Backup for automated backups:

```bash
# Create backup plan
aws backup create-backup-plan \
  --backup-plan file://backup-plan.json

# Backup plan configuration
{
  "BackupPlanName": "vibegraph-daily-backup",
  "Rules": [{
    "RuleName": "DailyBackup",
    "TargetBackupVaultName": "vibegraph-backup-vault",
    "ScheduleExpression": "cron(0 2 * * ? *)",
    "StartWindowMinutes": 60,
    "CompletionWindowMinutes": 120,
    "Lifecycle": {
      "DeleteAfterDays": 30
    }
  }]
}
```

### Disaster Recovery

#### Recovery Time Objective (RTO)

Target: 1 hour

#### Recovery Point Objective (RPO)

Target: 5 minutes (using PITR)

#### Disaster Recovery Procedure

1. **Assess the Situation**
   - Identify the scope of the outage
   - Determine if it's a partial or complete failure
   - Check monitoring dashboards and logs

2. **Activate DR Plan**
   - Notify stakeholders
   - Assemble incident response team
   - Document all actions taken

3. **Restore Services**

   **Option A: Restore from Backup**
   ```bash
   # Restore DynamoDB tables
   aws dynamodb restore-table-to-point-in-time \
     --source-table-name vibegraph-prod-users \
     --target-table-name vibegraph-prod-users-restored \
     --restore-date-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%S)
   
   # Update application to use restored table
   aws ecs update-service \
     --cluster vibegraph-prod \
     --service vibegraph-backend \
     --force-new-deployment
   ```

   **Option B: Failover to Secondary Region**
   ```bash
   # Update Route 53 to point to secondary region
   aws route53 change-resource-record-sets \
     --hosted-zone-id Z1234567890ABC \
     --change-batch file://failover-config.json
   ```

4. **Verify Recovery**
   - Test all critical endpoints
   - Verify data integrity
   - Check monitoring dashboards
   - Perform smoke tests

5. **Post-Incident Review**
   - Document root cause
   - Identify improvements
   - Update runbooks
   - Implement preventive measures

### Data Export and Migration

Export data for backup or migration:

```bash
# Export DynamoDB table to S3
aws dynamodb export-table-to-point-in-time \
  --table-arn arn:aws:dynamodb:us-east-1:123456789012:table/vibegraph-prod-users \
  --s3-bucket vibegraph-backups \
  --s3-prefix exports/users/ \
  --export-format DYNAMODB_JSON

# Import data from S3
aws dynamodb import-table \
  --s3-bucket-source vibegraph-backups \
  --input-format DYNAMODB_JSON \
  --table-creation-parameters file://table-config.json
```

## Scaling and Performance

### Auto-Scaling Configuration

#### ECS Auto-Scaling

```bash
# Register scalable target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/vibegraph-prod/vibegraph-backend \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 2 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --service-namespace ecs \
  --resource-id service/vibegraph-prod/vibegraph-backend \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-name vibegraph-backend-cpu-scaling \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

Scaling policy configuration:
```json
{
  "TargetValue": 70.0,
  "PredefinedMetricSpecification": {
    "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
  },
  "ScaleInCooldown": 300,
  "ScaleOutCooldown": 60
}
```

#### DynamoDB Auto-Scaling

```bash
# Enable auto-scaling for table
aws application-autoscaling register-scalable-target \
  --service-namespace dynamodb \
  --resource-id table/vibegraph-prod-users \
  --scalable-dimension dynamodb:table:ReadCapacityUnits \
  --min-capacity 5 \
  --max-capacity 100

# Or use on-demand billing mode (recommended)
aws dynamodb update-table \
  --table-name vibegraph-prod-users \
  --billing-mode PAY_PER_REQUEST
```

### Performance Optimization

1. **Caching Strategy**
   - Implement embedding cache (already in design)
   - Cache frequently accessed user profiles
   - Use CloudFront for static assets
   - Implement API response caching

2. **Database Optimization**
   - Use DynamoDB on-demand billing for variable workloads
   - Create appropriate indexes for query patterns
   - Implement batch operations where possible
   - Monitor and optimize hot partitions

3. **API Optimization**
   - Enable gzip compression
   - Implement pagination for large result sets
   - Use connection pooling
   - Optimize Lambda cold starts (if using Lambda)

4. **Frontend Optimization**
   - Enable CDN for static assets
   - Implement code splitting
   - Use lazy loading for components
   - Optimize bundle size

## Troubleshooting

### Common Production Issues

#### High Latency

**Symptoms**: API responses taking >2 seconds

**Diagnosis**:
```bash
# Check CloudWatch metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name TargetResponseTime \
  --dimensions Name=LoadBalancer,Value=app/vibegraph-alb/1234567890abcdef \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Average

# Check application logs
aws logs tail /ecs/vibegraph-prod --follow --filter-pattern "duration > 2000"
```

**Solutions**:
- Scale up containers if CPU/memory is high
- Check database performance and add indexes
- Review slow queries in logs
- Enable caching for expensive operations

#### High Error Rate

**Symptoms**: Increased 5XX errors

**Diagnosis**:
```bash
# Check error logs
aws logs filter-log-events \
  --log-group-name /ecs/vibegraph-prod \
  --filter-pattern "ERROR" \
  --start-time $(date -u -d '1 hour ago' +%s)000

# Check health endpoints
curl https://api.vibegraph.com/health/status
```

**Solutions**:
- Check for recent deployments and rollback if needed
- Verify database connectivity
- Check Bedrock API status
- Review error logs for patterns

#### Database Throttling

**Symptoms**: DynamoDB throttling errors

**Diagnosis**:
```bash
# Check throttling metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/DynamoDB \
  --metric-name UserErrors \
  --dimensions Name=TableName,Value=vibegraph-prod-users \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 \
  --statistics Sum
```

**Solutions**:
- Switch to on-demand billing mode
- Increase provisioned capacity
- Implement exponential backoff in application
- Review and optimize query patterns

#### Container Crashes

**Symptoms**: Containers restarting frequently

**Diagnosis**:
```bash
# Check container logs
aws ecs describe-tasks \
  --cluster vibegraph-prod \
  --tasks $(aws ecs list-tasks --cluster vibegraph-prod --service-name vibegraph-backend --query 'taskArns[0]' --output text)

# View logs
aws logs tail /ecs/vibegraph-prod --follow
```

**Solutions**:
- Check for memory leaks (increase memory limit)
- Review application logs for errors
- Check health check configuration
- Verify environment variables are correct

### Rollback Procedure

If deployment causes issues:

```bash
# Rollback to previous task definition
aws ecs update-service \
  --cluster vibegraph-prod \
  --service vibegraph-backend \
  --task-definition vibegraph-backend:PREVIOUS_VERSION \
  --force-new-deployment

# Wait for rollback to complete
aws ecs wait services-stable \
  --cluster vibegraph-prod \
  --services vibegraph-backend

# Verify health
curl https://api.vibegraph.com/health/status
```

## Post-Deployment

### Smoke Tests

Run smoke tests after deployment:

```bash
# Test critical endpoints
./scripts/smoke-tests.sh

# Test quiz flow
./scripts/test-quiz-flow.sh

# Test profile endpoints
./scripts/test-profile-endpoints.sh
```

### Performance Testing

Run load tests to verify performance:

```bash
# Using Apache Bench
ab -n 1000 -c 10 https://api.vibegraph.com/health

# Using k6
k6 run load-test.js
```

### Monitoring

Monitor for 24 hours after deployment:

- Check error rates
- Monitor latency metrics
- Review logs for anomalies
- Verify auto-scaling works
- Check cost metrics

## Additional Resources

- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)

## Support

For deployment issues:

1. Check this guide and troubleshooting section
2. Review CloudWatch logs and metrics
3. Consult the development team
4. Open an incident ticket for critical issues

---

**Last Updated**: [Date]  
**Version**: 1.0.0  
**Maintained By**: DevOps Team
