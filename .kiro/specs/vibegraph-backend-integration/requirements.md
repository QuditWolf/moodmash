# Requirements Document: VibeGraph Backend Integration

## Introduction

This document specifies the functional and non-functional requirements for integrating the VibeGraph serverless backend with the existing React frontend. The system provides an adaptive quiz experience that generates AI-powered taste profiles, DNA archetypes, personalized growth paths, and taste-based matching. The architecture maintains strict privacy-first principles by storing only embeddings rather than raw quiz responses, while leveraging AWS Bedrock (Claude 3.5 Sonnet and Titan v2) for all AI processing.

## Glossary

- **API_Service**: Frontend service layer that handles all HTTP communication with backend endpoints
- **Quiz_System**: The complete adaptive quiz flow including Section 1 and Section 2 question generation
- **Session**: A temporary quiz session with 1-hour TTL that tracks user progress through the quiz
- **Embedding_Generator**: Lambda function that creates 1024-dimensional vectors from quiz answers using Titan v2
- **DNA_Generator**: Lambda function that creates taste DNA archetypes and traits using Claude
- **Path_Generator**: Lambda function that creates personalized growth paths with Absorb/Create/Reflect structure
- **Match_Finder**: Lambda function that finds taste matches using cosine similarity on embedding vectors
- **Analytics_Generator**: Lambda function that generates behavioral insights using Claude
- **Embedding_Cache**: DynamoDB table that stores embedding vectors keyed by document hash to minimize Titan API calls
- **Vector**: A 1024-dimensional normalized array of floating-point numbers representing taste embeddings
- **Cosine_Similarity**: A measure of similarity between two vectors, ranging from -1 to 1
- **TasteDNA**: A user's taste archetype including personality type, traits, and category preferences
- **Growth_Path**: Personalized recommendations organized into Absorb, Create, and Reflect categories
- **Onboarding_UI**: React component that orchestrates the multi-phase quiz flow
- **Claude**: AWS Bedrock's Claude 3.5 Sonnet model used for adaptive question generation and analysis
- **Titan**: AWS Bedrock's Titan v2 embedding model used for generating 1024-dimensional vectors

## Requirements

### Requirement 1: Adaptive Quiz Section 1 Generation

**User Story:** As a new user, I want to answer foundational questions about my taste preferences, so that the system can understand my baseline interests.

#### Acceptance Criteria

1. WHEN a user starts the onboarding flow, THE Quiz_System SHALL generate 5 foundational questions using Claude
2. WHEN Section 1 questions are generated, THE Quiz_System SHALL create a session with 1-hour expiration
3. WHEN Section 1 questions are returned, THE Quiz_System SHALL include a unique sessionId for tracking
4. THE Quiz_System SHALL ensure each Section 1 question has a title, category, options array, and multiSelect flag
5. WHEN Section 1 generation fails, THE Quiz_System SHALL return an error message and allow retry

### Requirement 2: Adaptive Quiz Section 2 Generation

**User Story:** As a user completing Section 1, I want to receive personalized follow-up questions, so that the system can deeply understand my unique taste profile.

#### Acceptance Criteria

1. WHEN a user submits Section 1 answers, THE Quiz_System SHALL retrieve the session from storage
2. WHEN the session is expired or not found, THE Quiz_System SHALL return a 404 error with message "Session expired or not found"
3. WHEN Section 1 answers are valid, THE Quiz_System SHALL generate 5 adaptive Section 2 questions using Claude based on Section 1 responses
4. WHEN Section 2 questions are generated, THE Quiz_System SHALL update the session with Section 1 answers and Section 2 questions
5. WHEN Section 2 generation completes, THE Quiz_System SHALL update session status to "section2_complete"

### Requirement 3: Quiz Completion and Embedding Generation

**User Story:** As a user completing the quiz, I want my taste profile to be processed and stored securely, so that I can receive personalized recommendations without exposing my raw answers.

#### Acceptance Criteria

1. WHEN a user submits all quiz answers, THE Embedding_Generator SHALL build a structured embedding document from the responses
2. WHEN an embedding document is created, THE Embedding_Generator SHALL check the cache using SHA-256 hash
3. WHEN a cache hit occurs, THE Embedding_Generator SHALL retrieve the cached vector without calling Titan
4. WHEN a cache miss occurs, THE Embedding_Generator SHALL generate a 1024-dimensional vector using Titan v2
5. WHEN a new embedding is generated, THE Embedding_Generator SHALL store it in the cache with the document hash
6. WHEN an embedding vector is created, THE Embedding_Generator SHALL apply weighting based on answer patterns
7. WHEN weighting is applied, THE Embedding_Generator SHALL normalize the vector to unit length
8. WHEN the embedding is complete, THE Embedding_Generator SHALL store the vector in the Users table
9. THE Embedding_Generator SHALL NOT store raw quiz answers in any database table
10. WHEN embedding generation fails, THE Embedding_Generator SHALL return a 500 error and NOT store partial data

### Requirement 4: Taste DNA Profile Generation

**User Story:** As a user completing the quiz, I want to receive a personalized taste DNA archetype, so that I can understand my unique taste personality.

#### Acceptance Criteria

1. WHEN quiz completion is triggered, THE DNA_Generator SHALL generate a taste archetype using Claude based on quiz answers
2. WHEN DNA generation completes, THE DNA_Generator SHALL include an archetype name, trait scores, category profiles, and description
3. THE DNA_Generator SHALL ensure each trait has a name, score between 0-10, and description
4. THE DNA_Generator SHALL ensure each category profile has a category name, preferences array, and intensity value
5. WHEN DNA is generated, THE DNA_Generator SHALL store the profile in the Users table
6. WHEN DNA generation fails, THE DNA_Generator SHALL return an error and allow retry

### Requirement 5: Growth Path Generation

**User Story:** As a user with a taste DNA profile, I want to receive personalized growth recommendations, so that I can explore content aligned with my taste preferences.

#### Acceptance Criteria

1. WHEN a user requests a growth path, THE Path_Generator SHALL retrieve the user's DNA profile from storage
2. WHEN the user or DNA profile is not found, THE Path_Generator SHALL return a 404 error
3. WHEN DNA profile exists, THE Path_Generator SHALL generate personalized recommendations using Claude
4. WHEN recommendations are generated, THE Path_Generator SHALL organize them into Absorb, Create, and Reflect categories
5. THE Path_Generator SHALL ensure each category contains 3-5 recommendations
6. THE Path_Generator SHALL ensure each recommendation has id, title, description, category, estimatedTime, and difficulty
7. WHEN path generation completes, THE Path_Generator SHALL store the path in the Users table with timestamp

### Requirement 6: Taste Matching

**User Story:** As a user with a taste profile, I want to find other users with similar tastes, so that I can discover like-minded individuals.

#### Acceptance Criteria

1. WHEN a user requests matches, THE Match_Finder SHALL retrieve the user's embedding vector from storage
2. WHEN the user or embedding is not found, THE Match_Finder SHALL return a 404 error
3. WHEN the embedding exists, THE Match_Finder SHALL calculate cosine similarity with all other user embeddings
4. WHEN calculating similarity, THE Match_Finder SHALL exclude the requesting user from results
5. WHEN similarity is calculated, THE Match_Finder SHALL only include matches with similarity greater than 0.7
6. WHEN matches are found, THE Match_Finder SHALL identify shared traits between users
7. WHEN matches are returned, THE Match_Finder SHALL sort them by similarity score in descending order
8. WHEN a limit parameter is provided, THE Match_Finder SHALL return at most that many matches
9. THE Match_Finder SHALL enforce a maximum limit of 50 matches per request

### Requirement 7: Behavioral Analytics Generation

**User Story:** As a user with a taste profile, I want to receive insights about my content consumption patterns, so that I can understand and optimize my taste development.

#### Acceptance Criteria

1. WHEN a user requests analytics, THE Analytics_Generator SHALL retrieve the user's DNA profile and growth path
2. WHEN the user is not found, THE Analytics_Generator SHALL return a 404 error
3. WHEN user data exists, THE Analytics_Generator SHALL generate analytics using Claude
4. WHEN analytics are generated, THE Analytics_Generator SHALL include passive vs intentional ratio, goal alignment score, content balance, insights, and recommendations
5. THE Analytics_Generator SHALL ensure each insight has a type (strength, opportunity, or pattern), title, and description
6. THE Analytics_Generator SHALL ensure each content balance entry has category, percentage, and trend
7. WHEN analytics generation completes, THE Analytics_Generator SHALL store the analytics in the Users table with timestamp

### Requirement 8: Frontend API Service Layer

**User Story:** As a frontend developer, I want a centralized API service, so that I can easily integrate backend functionality without managing HTTP details in UI components.

#### Acceptance Criteria

1. THE API_Service SHALL provide methods for all quiz operations (startSection1, generateSection2, completeQuiz)
2. THE API_Service SHALL provide methods for all profile operations (getTasteDNA, getGrowthPath, getMatches, getAnalytics)
3. WHEN making API requests, THE API_Service SHALL include authentication tokens from local storage
4. WHEN API requests fail, THE API_Service SHALL parse error messages and throw descriptive errors
5. WHEN responses are received, THE API_Service SHALL parse JSON and return typed data structures
6. THE API_Service SHALL set Content-Type header to "application/json" for all requests
7. THE API_Service SHALL construct URLs using the configured API base URL from environment variables

### Requirement 9: Enhanced Onboarding Flow

**User Story:** As a user, I want a smooth multi-phase onboarding experience, so that I can complete the quiz and see my results without confusion.

#### Acceptance Criteria

1. WHEN onboarding starts, THE Onboarding_UI SHALL display Section 1 questions retrieved from the API
2. WHEN Section 1 is completed, THE Onboarding_UI SHALL transition to Section 2 phase
3. WHEN Section 2 is completed, THE Onboarding_UI SHALL transition to processing phase with loading indicator
4. WHEN quiz processing completes, THE Onboarding_UI SHALL transition to complete phase displaying TasteDNACard
5. WHEN any API call fails, THE Onboarding_UI SHALL display an error message with retry option
6. THE Onboarding_UI SHALL preserve sessionId across all phases
7. THE Onboarding_UI SHALL collect and store answers for both sections before final submission

### Requirement 10: Session Management

**User Story:** As a system administrator, I want quiz sessions to expire after 1 hour, so that we don't accumulate stale session data.

#### Acceptance Criteria

1. WHEN a session is created, THE Quiz_System SHALL set expiresAt to createdAt plus 3600 seconds
2. WHEN a session is retrieved, THE Quiz_System SHALL check if current time exceeds expiresAt
3. WHEN a session is expired, THE Quiz_System SHALL return a 404 error
4. THE Quiz_System SHALL store session status as one of: "section1_complete", "section2_complete", or "quiz_complete"
5. WHEN Section 1 completes, THE Quiz_System SHALL ensure the session contains exactly 5 Section 1 questions

### Requirement 11: Vector Operations

**User Story:** As a backend developer, I want reliable vector operations, so that embedding and matching functionality works correctly.

#### Acceptance Criteria

1. WHEN normalizing a vector, THE Embedding_Generator SHALL calculate the magnitude as the square root of the sum of squared elements
2. WHEN normalizing a vector, THE Embedding_Generator SHALL divide each element by the magnitude
3. WHEN normalization completes, THE Embedding_Generator SHALL ensure the resulting vector has magnitude approximately equal to 1.0 within 0.0001 tolerance
4. WHEN calculating cosine similarity, THE Match_Finder SHALL compute the dot product of two normalized vectors
5. WHEN cosine similarity is calculated, THE Match_Finder SHALL ensure the result is between -1 and 1
6. WHEN comparing a vector to itself, THE Match_Finder SHALL return similarity of 1.0
7. WHEN comparing a vector to its negation, THE Match_Finder SHALL return similarity of -1.0

### Requirement 12: Data Validation

**User Story:** As a security engineer, I want all inputs validated, so that the system rejects malformed or malicious data.

#### Acceptance Criteria

1. WHEN receiving Section 1 answers, THE Quiz_System SHALL validate that exactly 5 answers are provided
2. WHEN receiving quiz answers, THE Quiz_System SHALL validate that each answer has a questionId and selectedOptions array
3. WHEN receiving quiz answers, THE Quiz_System SHALL validate that each answer has at least one selected option
4. WHEN receiving quiz answers, THE Quiz_System SHALL validate that each option string is at most 500 characters
5. WHEN receiving a sessionId, THE Quiz_System SHALL validate that it is a valid UUID format
6. WHEN receiving a userId, THE Quiz_System SHALL validate that it is a valid UUID format
7. WHEN validation fails, THE Quiz_System SHALL return a 400 error with a specific validation message
8. WHEN receiving embedding vectors, THE Quiz_System SHALL validate that the array length is exactly 1024
9. WHEN receiving embedding vectors, THE Quiz_System SHALL validate that all values are between -1 and 1

### Requirement 13: Error Handling and Recovery

**User Story:** As a user, I want clear error messages and recovery options, so that I can complete the quiz even when issues occur.

#### Acceptance Criteria

1. WHEN Claude API fails, THE Quiz_System SHALL retry the request up to 3 times with exponential backoff
2. WHEN all Claude retries fail, THE Quiz_System SHALL return a 500 error with message "AI service temporarily unavailable"
3. WHEN Titan API fails, THE Embedding_Generator SHALL retry the request up to 2 times
4. WHEN all Titan retries fail, THE Embedding_Generator SHALL return a 500 error with message "Failed to generate taste profile"
5. WHEN DynamoDB operations fail, THE Quiz_System SHALL retry up to 3 times with exponential backoff (100ms, 200ms, 400ms)
6. WHEN all DynamoDB retries fail, THE Quiz_System SHALL return a 503 error with message "Service temporarily unavailable"
7. WHEN the frontend receives a 500 or 503 error, THE Onboarding_UI SHALL display a retry button
8. WHEN the frontend receives a 404 session error, THE Onboarding_UI SHALL redirect to onboarding start

### Requirement 14: Authentication and Authorization

**User Story:** As a security engineer, I want all API endpoints protected, so that users can only access their own data.

#### Acceptance Criteria

1. WHEN an API request is received, THE Quiz_System SHALL validate the JWT token in the Authorization header
2. WHEN no token is provided, THE Quiz_System SHALL return a 401 error
3. WHEN an invalid token is provided, THE Quiz_System SHALL return a 401 error
4. WHEN a valid token is provided, THE Quiz_System SHALL extract the userId from the token
5. WHEN accessing profile data, THE Quiz_System SHALL ensure the requesting user matches the profile userId
6. WHEN a user attempts to access another user's data, THE Quiz_System SHALL return a 403 error
7. THE Quiz_System SHALL enforce rate limiting of 100 requests per minute per user

### Requirement 15: Privacy and Data Protection

**User Story:** As a privacy-conscious user, I want my quiz answers kept private, so that my raw responses are never stored or exposed.

#### Acceptance Criteria

1. THE Embedding_Generator SHALL NOT store raw quiz answers in the Users table
2. THE Embedding_Generator SHALL NOT store raw quiz answers in any DynamoDB table
3. THE Embedding_Generator SHALL only store the 1024-dimensional embedding vector
4. WHEN storing user data, THE Quiz_System SHALL encrypt data at rest using DynamoDB encryption
5. WHEN transmitting data, THE Quiz_System SHALL use TLS 1.3 encryption
6. WHEN a user requests data deletion, THE Quiz_System SHALL remove all user records from DynamoDB
7. THE Quiz_System SHALL implement a 2-year data retention policy for inactive users

### Requirement 16: Performance and Caching

**User Story:** As a system administrator, I want efficient caching, so that we minimize API costs and response times.

#### Acceptance Criteria

1. WHEN generating an embedding, THE Embedding_Generator SHALL compute a SHA-256 hash of the embedding document
2. WHEN the hash is computed, THE Embedding_Generator SHALL check the Embedding_Cache for an existing entry
3. WHEN a cache hit occurs, THE Embedding_Generator SHALL retrieve the cached vector and increment hitCount
4. WHEN a cache hit occurs, THE Embedding_Generator SHALL update lastAccessedAt timestamp
5. WHEN a cache miss occurs, THE Embedding_Generator SHALL call Titan v2 to generate the embedding
6. WHEN a new embedding is generated, THE Embedding_Generator SHALL store it in the cache with the document hash
7. WHEN using Lambda provisioned concurrency, THE Quiz_System SHALL maintain warm instances for Section 1 and Complete Quiz endpoints
8. THE Quiz_System SHALL target a 40% cache hit rate for embedding generation

### Requirement 17: API Response Formats

**User Story:** As a frontend developer, I want consistent API response formats, so that I can reliably parse and display data.

#### Acceptance Criteria

1. WHEN Section 1 starts, THE Quiz_System SHALL return sessionId, questions array, and expiresAt timestamp
2. WHEN Section 2 is generated, THE Quiz_System SHALL return questions array
3. WHEN quiz completes, THE Quiz_System SHALL return embeddingId and tasteDNA object
4. WHEN DNA is retrieved, THE Quiz_System SHALL return tasteDNA with archetype, traits, categories, and description
5. WHEN growth path is retrieved, THE Quiz_System SHALL return path with absorb, create, reflect arrays and generatedAt timestamp
6. WHEN matches are retrieved, THE Quiz_System SHALL return matches array with userId, username, similarity, sharedTraits, and archetype for each match
7. WHEN analytics are retrieved, THE Quiz_System SHALL return analytics with passiveVsIntentionalRatio, goalAlignment, contentBalance, insights, and recommendations
8. WHEN errors occur, THE Quiz_System SHALL return JSON with message field describing the error
9. THE Quiz_System SHALL include CORS headers with Access-Control-Allow-Origin set to allowed origins

### Requirement 18: Logging and Monitoring

**User Story:** As a system administrator, I want comprehensive logging, so that I can troubleshoot issues and monitor system health.

#### Acceptance Criteria

1. WHEN Section 1 is generated, THE Quiz_System SHALL log the sessionId and question count to CloudWatch
2. WHEN API errors occur, THE Quiz_System SHALL log the error message, stack trace, and request context
3. WHEN embedding cache hits occur, THE Quiz_System SHALL log the cache hit event
4. WHEN Titan API calls are made, THE Quiz_System SHALL log the request timestamp and response time
5. THE Quiz_System SHALL NOT log sensitive data including JWT tokens, raw quiz answers, or embedding vectors
6. WHEN Lambda cold starts occur, THE Quiz_System SHALL log the cold start duration
7. THE Quiz_System SHALL log all authentication failures with userId and timestamp
