# Enable Bedrock Models - Required Step

## Current Error

```
Model use case details have not been submitted for this account. 
Fill out the Anthropic use case details form before using the model.
```

## What You Need to Do

### Step 1: Go to Bedrock Console

1. Log into **AWS Console**
2. Search for **"Bedrock"** service
3. Make sure you're in **us-east-1** region (top right)

### Step 2: Request Model Access

1. Click **"Model access"** in the left sidebar
2. Click **"Manage model access"** or **"Request model access"** button (orange button)
3. You'll see a list of models

### Step 3: Enable Claude Models

1. Find **"Anthropic"** section
2. Check the boxes for:
   - ✅ **Claude 3 Haiku**
   - ✅ **Claude 3.5 Sonnet** (if available)
   - ✅ **Claude 3 Sonnet**

3. You may need to fill out a use case form:
   - **Use case**: Development/Testing
   - **Description**: "Building a cultural taste profiling application"
   - **Industry**: Technology/Software

### Step 4: Enable Titan Models

1. Find **"Amazon"** section
2. Check the boxes for:
   - ✅ **Titan Embeddings G1 - Text v2**
   - ✅ **Titan Image Generator** (optional, for DNA cards)

### Step 5: Submit Request

1. Click **"Request model access"** button at the bottom
2. Wait for approval (usually instant, but can take up to 15 minutes)
3. Refresh the page to see status change to "Access granted"

## After Enabling Models

Once models show "Access granted", run this test:

```bash
curl -X POST http://localhost:8000/quiz/section1/start \
  -H "Content-Type: application/json" -d '{}'
```

You should see quiz questions generated!

## Alternative: Use AWS CLI

You can also check available models with:

```bash
aws bedrock list-foundation-models --region us-east-1 \
  --by-provider anthropic
```

## Troubleshooting

### "Access denied" or "Legacy model"
→ Model not enabled. Go to Bedrock Console and enable it.

### "Use case form required"
→ Fill out the form in Bedrock Console when requesting access.

### "Still not working after 15 minutes"
→ Check AWS Support or try a different model (Claude 3 Haiku is usually fastest to approve).

## Models We're Using

- **Claude 3 Haiku**: Fast, cost-effective ($0.25/$1.25 per 1M tokens)
- **Titan Embeddings v2**: For taste embeddings ($0.0001 per 1K tokens)
- **Titan Image Generator**: For DNA cards ($0.008 per image)

Once enabled, everything will work!
