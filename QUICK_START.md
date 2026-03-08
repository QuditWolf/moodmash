# VibeGraph Backend - Quick Start Guide

## 🚀 Test with Real AWS in 5 Minutes

### Prerequisites
- Docker & Docker Compose installed
- AWS account with Bedrock access

### Step 1: Get AWS Credentials (2 min)

1. Go to AWS Console → IAM → Users → Create User
2. Name: `vibegraph-user`
3. Attach policy: `AmazonBedrockFullAccess`
4. Create access key → Save credentials

### Step 2: Enable Bedrock Models (1 min)

1. Go to AWS Console → Bedrock → Model access
2. Enable these models:
   - ✅ Claude 3.5 Sonnet
   - ✅ Titan Embeddings v2
   - ✅ Titan Image Generator

### Step 3: Configure Backend (1 min)

```bash
# Copy environment template
cp .env.example .env

# Edit .env - add your credentials
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=wJal...
AWS_REGION=us-east-1
```

Edit `docker-compose.override.yml` - comment out line 18:
```yaml
# - BEDROCK_ENDPOINT=http://localstack:4566
```

### Step 4: Test Everything (1 min)

```bash
# Restart containers
docker-compose restart backend-api

# Run test script
bash backend/scripts/test_with_real_aws.sh
```

## ✅ Expected Output

```
✓ Health check passed
✓ Bedrock connection healthy
✓ Section 1 generated successfully
  Questions: 5
✓ Section 2 generated successfully
  Questions: 5
✓ Quiz completed successfully
  Archetype: Dream Liminalist
✓ DNA card image generated successfully
  Image saved to: dna-card-user123.png

All core tests passed!
Cost estimate: ~$0.03
```

## 🎨 View Your DNA Card

Open the generated image:
```bash
open dna-card-*.png
```

You'll see a stunning 1024x1024 collage with:
- Personalized visual style
- Username and archetype
- Taste signals integrated
- Indie zine aesthetic
- Moodmash branding

## 📊 What You Can Do Now

### Test Individual Endpoints

```bash
# Generate quiz questions
curl -X POST http://localhost:8000/quiz/section1/start \
  -H "Content-Type: application/json" -d '{}' | jq .

# Generate DNA card image
curl -X POST "http://localhost:8000/profile/dna-card/user123?model=titan" | jq .
```

### Check Costs

Go to AWS Console → Billing Dashboard

Expected costs per test:
- Quiz flow: $0.02
- DNA card: $0.008
- Total: ~$0.03

With $100 credits = 3,000+ complete tests!

## 🆘 Troubleshooting

### "Model access denied"
→ Enable models in Bedrock Console

### "Invalid credentials"
→ Check `.env` file has correct AWS keys

### "LocalStack error"
→ Ensure `BEDROCK_ENDPOINT` is commented out in docker-compose.override.yml

### "Throttling exception"
→ Wait 10 seconds and retry (built-in retry logic)

## 📚 Full Documentation

- `AWS_BEDROCK_SETUP.md` - Complete AWS setup
- `READY_FOR_AWS_TESTING.md` - Detailed testing guide
- `IMPLEMENTATION_SUMMARY.md` - Full implementation details

## 🎯 Next Steps

1. ✅ Test all 8 endpoints
2. ✅ Generate multiple DNA cards
3. ✅ Integrate with frontend
4. ✅ Deploy to production

---

**That's it!** Your VibeGraph backend is now powered by real AWS Bedrock AI. 🚀

Questions? Check the full documentation or container logs:
```bash
docker-compose logs -f backend-api
```
