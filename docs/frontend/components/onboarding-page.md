# OnboardingPage Component

## Overview

The `OnboardingPage` component orchestrates the multi-phase adaptive quiz flow, integrating with the VibeGraph backend API to generate personalized taste profiles. It manages the complete onboarding experience from Section 1 questions through Section 2 adaptive questions to final Taste DNA generation.

## Location

`frontend/src/components/onboarding/OnboardingPage.jsx`

## Purpose

- Manage multi-phase quiz flow (Section 1 → Section 2 → Processing → Complete)
- Integrate with VibeGraph API service for question generation and profile creation
- Handle session state management across quiz phases
- Provide error handling and retry functionality
- Display loading states during API operations
- Present final Taste DNA results

## Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `onComplete` | `function` | Yes | Callback function invoked when user completes onboarding and clicks "Enter Feed" |

## State Management

### Phase State

The component uses a phase-based state machine with four phases:

- **`section1`**: Initial phase, displaying Section 1 foundational questions
- **`section2`**: Second phase, displaying adaptive Section 2 questions
- **`processing`**: Transition phase while generating Taste DNA
- **`complete`**: Final phase, displaying TasteDNACard with results

### Session State

| State Variable | Type | Description |
|----------------|------|-------------|
| `sessionId` | `string \| null` | Unique session identifier from backend, persists across both sections |
| `section1Questions` | `Array<Question>` | Array of 5 foundational questions from Section 1 |
| `section2Questions` | `Array<Question>` | Array of 5 adaptive questions from Section 2 |
| `currentQuestionIndex` | `number` | Index of current question within current section (0-4) |

### Answer State

| State Variable | Type | Description |
|----------------|------|-------------|
| `section1Answers` | `Array<Answer>` | Array of answer objects for Section 1 |
| `section2Answers` | `Array<Answer>` | Array of answer objects for Section 2 |

**Answer Object Structure:**
```javascript
{
  questionId: string,
  selectedOptions: string[]
}
```

### Results State

| State Variable | Type | Description |
|----------------|------|-------------|
| `tasteDNA` | `object \| null` | Generated Taste DNA profile from backend |

### UI State

| State Variable | Type | Description |
|----------------|------|-------------|
| `loading` | `boolean` | Indicates active API operation |
| `error` | `string \| null` | Error message to display to user |

## API Integration

### Section 1 Initialization

On component mount, the component calls `vibeGraphAPI.quiz.startSection1()` to:
- Generate a new session with unique `sessionId`
- Retrieve 5 foundational questions
- Initialize the quiz flow

```javascript
useEffect(() => {
  const loadSection1 = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await vibeGraphAPI.quiz.startSection1();
      setSessionId(response.sessionId);
      setSection1Questions(response.questions);
    } catch (err) {
      setError(err.message || 'Failed to load questions. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  loadSection1();
}, []);
```

### Section 2 Generation

When user completes Section 1, the component calls `vibeGraphAPI.quiz.generateSection2()` to:
- Send Section 1 answers to backend
- Receive 5 adaptive questions based on Section 1 responses
- Transition to Section 2 phase

```javascript
const loadSection2 = async () => {
  setLoading(true);
  setError(null);
  
  try {
    const response = await vibeGraphAPI.quiz.generateSection2(sessionId, section1Answers);
    setSection2Questions(response.questions);
    setPhase('section2');
    setCurrentQuestionIndex(0);
  } catch (err) {
    setError(err.message || 'Failed to load next section. Please try again.');
  } finally {
    setLoading(false);
  }
};
```

### Quiz Completion

When user completes Section 2, the component calls `vibeGraphAPI.quiz.completeQuiz()` to:
- Submit all answers (Section 1 + Section 2)
- Generate embedding vector and Taste DNA profile
- Store results in localStorage
- Transition to complete phase

```javascript
const completeQuiz = async () => {
  setPhase('processing');
  setLoading(true);
  setError(null);
  
  try {
    const userId = localStorage.getItem('userId') || `temp-${Date.now()}`;
    
    const allAnswers = {
      section1: section1Answers,
      section2: section2Answers
    };
    
    const response = await vibeGraphAPI.quiz.completeQuiz(sessionId, userId, allAnswers);
    setTasteDNA(response.tasteDNA);
    setPhase('complete');
    
    // Store in localStorage
    localStorage.setItem('taste_profile', JSON.stringify({
      userId,
      tasteDNA: response.tasteDNA,
      embeddingId: response.embeddingId,
      completedAt: new Date().toISOString()
    }));
  } catch (err) {
    setError(err.message || 'Failed to complete quiz. Please try again.');
    setPhase('section2');
  } finally {
    setLoading(false);
  }
};
```

## User Interactions

### Option Selection

Users can select/deselect options for each question. The component maintains separate answer arrays for Section 1 and Section 2:

```javascript
const handleToggleOption = (option) => {
  const updateAnswers = phase === 'section1' ? setSection1Answers : setSection2Answers;
  
  updateAnswers(prev => {
    const existingAnswer = prev.find(a => a.questionId === currentQuestion.id);
    
    if (existingAnswer) {
      // Update existing answer
      const isSelected = existingAnswer.selectedOptions.includes(option);
      return prev.map(a => 
        a.questionId === currentQuestion.id
          ? {
              ...a,
              selectedOptions: isSelected
                ? a.selectedOptions.filter(o => o !== option)
                : [...a.selectedOptions, option]
            }
          : a
      );
    } else {
      // Create new answer
      return [...prev, {
        questionId: currentQuestion.id,
        selectedOptions: [option]
      }];
    }
  });
};
```

### Navigation

The "Next" button behavior depends on the current phase and question:

- **Within Section 1**: Advances to next question
- **Last question of Section 1**: Triggers Section 2 generation
- **Within Section 2**: Advances to next question
- **Last question of Section 2**: Triggers quiz completion

```javascript
const handleNext = async () => {
  const isLastQuestion = currentQuestionIndex === currentQuestions.length - 1;
  
  if (isLastQuestion) {
    if (phase === 'section1') {
      await loadSection2();
    } else if (phase === 'section2') {
      await completeQuiz();
    }
  } else {
    setCurrentQuestionIndex(prev => prev + 1);
  }
};
```

## Error Handling

The component provides comprehensive error handling with user-friendly messages and retry functionality:

### Error Display

When an error occurs, the component displays an error screen with:
- Clear error message
- "Try Again" button to retry the failed operation
- Appropriate styling to indicate error state

```javascript
if (error) {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">
      <div className="w-full max-w-md text-center">
        <div className="bg-surface/50 border border-red-500/20 rounded-lg p-8">
          <h2 className="text-20 font-medium text-foreground mb-3">Something went wrong</h2>
          <p className="text-13 text-muted-foreground mb-6">{error}</p>
          <button
            onClick={handleRetry}
            className="px-6 py-3 rounded-lg text-13 font-medium bg-white text-black hover:bg-white/90 transition-all duration-180"
          >
            Try Again
          </button>
        </div>
      </div>
    </div>
  );
}
```

### Retry Logic

The retry handler determines the appropriate action based on the current phase:

```javascript
const handleRetry = () => {
  setError(null);
  
  if (phase === 'section1' && section1Questions.length === 0) {
    // Retry loading Section 1
    window.location.reload();
  } else if (phase === 'section1') {
    // Retry loading Section 2
    loadSection2();
  } else if (phase === 'section2' || phase === 'processing') {
    // Retry completing quiz
    completeQuiz();
  }
};
```

### Error Scenarios

| Scenario | Error Message | Retry Action |
|----------|---------------|--------------|
| Section 1 load failure | "Failed to load questions. Please try again." | Reload page |
| Section 2 generation failure | "Failed to load next section. Please try again." | Retry `loadSection2()` |
| Quiz completion failure | "Failed to complete quiz. Please try again." | Retry `completeQuiz()` |
| Network error | API error message | Context-appropriate retry |

## Loading States

The component displays loading indicators during API operations:

### Initial Load

When loading Section 1 questions on mount:

```javascript
if (loading && currentQuestions.length === 0) {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto mb-4"></div>
        <p className="text-13 text-muted-foreground">Loading questions...</p>
      </div>
    </div>
  );
}
```

### Processing State

When generating Taste DNA after Section 2 completion:

```javascript
if (phase === 'processing') {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6">
      <div className="text-center">
        <div className="w-12 h-12 border-4 border-white/20 border-t-white rounded-full animate-spin mx-auto mb-4"></div>
        <p className="text-13 text-muted-foreground">Generating your Taste DNA...</p>
      </div>
    </div>
  );
}
```

### Button Loading

The "Next" button shows a loading spinner during transitions:

```javascript
{loading ? (
  <>
    <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
    Loading...
  </>
) : (
  <>
    {currentIndex === totalQuestions - 1 ? 'Finish' : 'Next'}
    <ArrowRight className="w-4 h-4" strokeWidth={2} />
  </>
)}
```

## Progress Tracking

The component tracks progress across both sections:

```javascript
const totalQuestions = section1Questions.length + section2Questions.length;
const currentAbsoluteIndex = phase === 'section1' 
  ? currentQuestionIndex 
  : section1Questions.length + currentQuestionIndex;
```

This provides accurate progress indication (e.g., "Question 7 of 10") across both sections.

## Data Persistence

### localStorage Storage

On quiz completion, the component stores the profile in localStorage:

```javascript
localStorage.setItem('taste_profile', JSON.stringify({
  userId,
  tasteDNA: response.tasteDNA,
  embeddingId: response.embeddingId,
  completedAt: new Date().toISOString()
}));
```

### User ID Management

The component retrieves or generates a user ID:

```javascript
const userId = localStorage.getItem('userId') || `temp-${Date.now()}`;
```

## Child Components

### QuestionScreen

Displays individual questions with options and navigation:

```javascript
<QuestionScreen
  question={currentQuestion}
  currentIndex={currentAbsoluteIndex}
  totalQuestions={totalQuestions}
  selectedOptions={selectedOptions}
  onToggleOption={handleToggleOption}
  onNext={handleNext}
  loading={loading}
/>
```

### TasteDNACard

Displays final Taste DNA results:

```javascript
<TasteDNACard 
  tasteDNA={tasteDNA} 
  answers={answersForCard} 
  onContinue={handleComplete} 
/>
```

The component transforms answers into the format expected by TasteDNACard:

```javascript
const answersForCard = {};
[...section1Answers, ...section2Answers].forEach(answer => {
  const question = [...section1Questions, ...section2Questions].find(q => q.id === answer.questionId);
  if (question && question.category) {
    answersForCard[question.category] = answer.selectedOptions;
  }
});
```

## Usage Example

```jsx
import OnboardingPage from './components/onboarding/OnboardingPage';

function App() {
  const handleOnboardingComplete = () => {
    // Navigate to main feed
    navigate('/feed');
  };

  return (
    <OnboardingPage onComplete={handleOnboardingComplete} />
  );
}
```

## Dependencies

- `vibeGraphAPI` - API service for backend communication
- `QuestionScreen` - Component for displaying questions
- `TasteDNACard` - Component for displaying results
- React hooks: `useState`, `useEffect`

## Related Documentation

- [VibeGraph API Service](../services/vibegraph-api.md)
- [QuestionScreen Component](./question-screen.md)
- [TasteDNACard Component](./taste-dna-card.md)
- [API Endpoints](../../api/quiz-endpoints.md)

## Notes

- Session expiration handling has been removed per requirements (no 1-hour TTL)
- The component handles both authenticated and unauthenticated users
- All API errors are caught and displayed with retry options
- Progress is tracked across both sections for accurate user feedback
- Answers are stored in structured format for backend processing
