# claudeService

## Purpose

High-level service for Claude 3.5 Sonnet interactions. Handles prompt formatting, response parsing, and model-specific configurations for quiz generation, DNA creation, path recommendations, and analytics.

## Location

`backend/src/services/claudeService.js`

## Interface

```javascript
async function generateQuestions(prompt, context, options)
async function generateDNA(answers, options)
async function generatePath(dnaProfile, options)
async function generateAnalytics(userProfile, options)
```

## Methods

### generateQuestions(prompt, context, options)

Generates quiz questions using Claude.

**Parameters**:
- `prompt` (string): Base prompt template
- `context` (object): Section 1 answers for adaptive generation (optional)
- `options` (object): Temperature, max_tokens

**Returns**: Array of Question objects

**Example**:
```javascript
const questions = await claudeService.generateQuestions(
  adaptiveQuizPrompt,
  { section1Answers: [...] },
  { temperature: 0.7, max_tokens: 2000 }
)
```

### generateDNA(answers, options)

Creates taste DNA profile from quiz answers.

**Parameters**:
- `answers` (object): Complete quiz responses
- `options` (object): Model parameters

**Returns**: TasteDNA object

### generatePath(dnaProfile, options)

Generates growth path recommendations.

**Parameters**:
- `dnaProfile` (object): User's taste DNA
- `options` (object): Model parameters

**Returns**: GrowthPath object

### generateAnalytics(userProfile, options)

Creates behavioral analytics.

**Parameters**:
- `userProfile` (object): DNA + growth path data
- `options` (object): Model parameters

**Returns**: Analytics object

## Configuration

```javascript
{
  modelId: 'anthropic.claude-3-5-sonnet-20241022-v2:0',
  defaultTemperature: 0.7,
  defaultMaxTokens: 2000,
  retries: 3
}
```

## Related

- [bedrockClient](./bedrockClient.md) - Underlying API client
