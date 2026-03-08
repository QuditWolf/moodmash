# Onboarding Components Documentation

## Overview

The onboarding system guides new users through an adaptive quiz to build their taste profile. The system consists of multiple components that work together to create a smooth, engaging experience.

## Component Architecture

```
OnboardingPage (Container)
├── QuestionScreen
│   ├── ProgressBar
│   └── OptionTile (multiple)
└── TasteDNACard
```

---

## OnboardingPage

**Location:** `src/components/onboarding/OnboardingPage.jsx`

The main container component that orchestrates the entire onboarding flow, managing state and navigation between questions and the final Taste DNA display.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `onComplete` | `function` | Yes | Callback function called when user completes onboarding |

### State

```javascript
{
  currentQuestionIndex: number,    // Current question index (0-based)
  answers: object,                 // Map of questionId -> selected options array
  showTasteDNA: boolean,          // Whether to show DNA results
  tasteDNA: object | null         // Generated taste DNA profile
}
```

### State Structure

**answers object:**
```javascript
{
  "music": ["Jazz", "Classical", "Electronic"],
  "movies": ["Sci-Fi", "Drama"],
  "books": ["Fiction", "Philosophy"],
  // ... other question IDs
}
```

**tasteDNA object:**
```javascript
{
  archetype: string,              // e.g., "The Minimalist"
  music: string,                  // Top music preference
  movies: string,                 // Top movie preference
  books: string,                  // Top book preference
  art: string,                    // Top art preference
  podcasts: string                // Top podcast preference
}
```

### Methods

#### `handleToggleOption(option)`

Toggles selection of an option for the current question.

**Parameters:**
- `option` (string): The option text to toggle

**Behavior:**
- If option is already selected, removes it from selections
- If option is not selected, adds it to selections
- Supports multi-select (users can select multiple options per question)

#### `handleNext()`

Advances to the next question or completes the quiz.

**Behavior:**
- If on last question: generates Taste DNA and shows results
- Otherwise: advances to next question
- Calls `generateTasteDNA(answers)` to create profile

#### `handleComplete()`

Finalizes the onboarding process.

**Behavior:**
- Saves taste profile to localStorage
- Calls `onComplete()` callback prop
- Stores: answers, tasteDNA, and completion timestamp

### Usage Example

```javascript
import OnboardingPage from '@/components/onboarding/OnboardingPage';
import { useNavigate } from 'react-router-dom';

function OnboardingRoute() {
  const navigate = useNavigate();

  const handleComplete = () => {
    // User completed onboarding
    navigate('/feed');
  };

  return <OnboardingPage onComplete={handleComplete} />;
}
```

### Data Flow

1. User starts onboarding → `currentQuestionIndex = 0`
2. User selects options → Updates `answers` state
3. User clicks "Next" → Increments `currentQuestionIndex`
4. Repeat steps 2-3 until last question
5. User clicks "Finish" → Generates `tasteDNA`
6. Shows `TasteDNACard` component
7. User clicks "Enter Feed" → Saves to localStorage and calls `onComplete()`

---

## QuestionScreen

**Location:** `src/components/onboarding/QuestionScreen.jsx`

Displays a single question with selectable options and navigation controls.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `question` | `object` | Yes | Question object with title and options |
| `currentIndex` | `number` | Yes | Current question index (0-based) |
| `totalQuestions` | `number` | Yes | Total number of questions |
| `selectedOptions` | `array` | Yes | Array of currently selected option strings |
| `onToggleOption` | `function` | Yes | Callback when option is clicked |
| `onNext` | `function` | Yes | Callback when Next/Finish button is clicked |

### Question Object Structure

```javascript
{
  id: string,              // Unique question identifier
  title: string,           // Question text to display
  options: string[]        // Array of option strings
}
```

### Layout

- **Progress Bar**: Shows completion progress at top
- **Question Title**: Large, prominent question text
- **Options Grid**: Responsive grid of selectable tiles
  - 2 columns on mobile
  - 3 columns on tablet
  - 4 columns on desktop
- **Next Button**: Bottom-right, disabled until at least one option selected

### Button States

- **Enabled**: White background, black text, hover lift effect
- **Disabled**: Gray background, muted text, no interaction
- **Last Question**: Button text changes from "Next" to "Finish"

### Usage Example

```javascript
<QuestionScreen
  question={{
    id: 'music',
    title: 'What music genres do you enjoy?',
    options: ['Jazz', 'Rock', 'Classical', 'Electronic', 'Hip-Hop']
  }}
  currentIndex={0}
  totalQuestions={5}
  selectedOptions={['Jazz', 'Classical']}
  onToggleOption={(option) => console.log('Toggled:', option)}
  onNext={() => console.log('Next clicked')}
/>
```

---

## OptionTile

**Location:** `src/components/onboarding/OptionTile.jsx`

A selectable tile representing a single option in a question.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `label` | `string` | Yes | Option text to display |
| `selected` | `boolean` | Yes | Whether option is currently selected |
| `onClick` | `function` | Yes | Callback when tile is clicked |

### Visual States

- **Unselected**: 
  - Semi-transparent background
  - White border with low opacity
  - Muted text color
  - Hover: Slight lift and border brightening

- **Selected**:
  - White background
  - Black text
  - Prominent appearance
  - Hover: Slight lift

### Styling

```css
/* Unselected */
background: rgba(255, 255, 255, 0.05)
border: 1px solid rgba(255, 255, 255, 0.1)
color: rgba(255, 255, 255, 0.7)

/* Selected */
background: white
border: 1px solid white
color: black
```

### Usage Example

```javascript
<OptionTile
  label="Jazz"
  selected={true}
  onClick={() => handleToggle('Jazz')}
/>
```

---

## ProgressBar

**Location:** `src/components/onboarding/ProgressBar.jsx`

Displays visual progress through the question sequence.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `current` | `number` | Yes | Current question number (1-based) |
| `total` | `number` | Yes | Total number of questions |

### Visual Design

- Horizontal bar with filled and unfilled segments
- Text indicator: "Question X of Y"
- Smooth animation when progress updates
- Minimal, unobtrusive design

### Usage Example

```javascript
<ProgressBar current={3} total={5} />
// Displays: "Question 3 of 5" with 60% filled bar
```

---

## TasteDNACard

**Location:** `src/components/onboarding/TasteDNACard.jsx`

Displays the user's generated taste profile with visualizations and category breakdowns.

### Props

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `tasteDNA` | `object` | Yes | Generated taste DNA profile |
| `answers` | `object` | No | User's quiz answers (for scoring) |
| `onContinue` | `function` | Yes | Callback when user clicks "Enter Feed" |

### TasteDNA Object Structure

```javascript
{
  archetype: string,              // Archetype name
  music: string,                  // Top music preference
  movies: string,                 // Top movie preference
  books: string,                  // Top book preference
  art: string,                    // Top art preference
  podcasts: string                // Top podcast preference
}
```

### Visual Components

#### 1. Archetype Hero Section
- Large archetype name (e.g., "The Minimalist")
- Descriptive text explaining the archetype
- Centered, prominent placement

#### 2. Category Grid
- 2-column grid showing top preference per category
- Icons for each category (Headphones, Film, BookOpen, etc.)
- Color-coded dots matching radar chart colors

#### 3. Radar Chart
- 5-axis radar chart showing taste distribution
- Categories: Music, Movies, Books, Art, Podcasts
- Normalized scores (0-10 scale)
- Semi-transparent fill with white stroke

#### 4. Horizontal Taste Bars
- Progress bars for each category
- Shows normalized score (0-10)
- Color-coded to match category colors
- Animated fill on mount

#### 5. Action Buttons
- **Share Button**: Copies taste DNA to clipboard or uses Web Share API
- **Enter Feed Button**: Primary CTA to complete onboarding

### Category Configuration

```javascript
const categoryConfig = {
  music: { 
    icon: Headphones, 
    color: 'hsl(270 50% 50%)',  // Purple
    label: 'Music'
  },
  movies: { 
    icon: Film, 
    color: 'hsl(0 50% 50%)',    // Red
    label: 'Movies'
  },
  books: { 
    icon: BookOpen, 
    color: 'hsl(220 60% 45%)',  // Blue
    label: 'Books'
  },
  art: { 
    icon: Image, 
    color: 'hsl(160 50% 45%)',  // Teal
    label: 'Art'
  },
  podcasts: { 
    icon: Mic, 
    color: 'hsl(40 60% 50%)',   // Orange
    label: 'Podcasts'
  }
};
```

### Archetype Descriptions

```javascript
const archetypeDescriptions = {
  'The Minimalist': 'Clean taste. Thoughtful content. You prefer focused, high-signal media.',
  'The Omnivore': 'Diverse interests. Broad curiosity. You consume content across all spectrums.',
  'The Creative': 'Artistic vision. Design-driven. You seek inspiration and creative expression.',
  'The Intellectual': 'Deep thinker. Knowledge seeker. You value substance and insight.',
  'The Explorer': 'Curious mind. Open to discovery. You embrace new experiences and perspectives.'
};
```

### Score Calculation

The component calculates normalized scores from answer counts:

1. **Raw Scores**: Count number of selections per category
2. **Normalization**: Scale to 0-10 based on maximum score
3. **Visualization**: Display in radar chart and progress bars

```javascript
// Example calculation
const rawScores = {
  music: 5,      // User selected 5 music options
  movies: 3,     // User selected 3 movie options
  books: 4,      // etc.
  art: 2,
  podcasts: 1
};

const maxScore = 5; // Maximum selections

const normalizedScores = {
  music: 10,     // (5/5) * 10 = 10
  movies: 6,     // (3/5) * 10 = 6
  books: 8,      // (4/5) * 10 = 8
  art: 4,        // (2/5) * 10 = 4
  podcasts: 2    // (1/5) * 10 = 2
};
```

### Share Functionality

The share button uses the Web Share API when available, falling back to clipboard copy:

```javascript
const handleShare = () => {
  const text = `My Taste DNA: ${tasteDNA.archetype}\nMusic: ${tasteDNA.music}\nMovies: ${tasteDNA.movies}\nBooks: ${tasteDNA.books}`;
  
  if (navigator.share) {
    navigator.share({ text });
  } else {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  }
};
```

### Usage Example

```javascript
<TasteDNACard
  tasteDNA={{
    archetype: 'The Minimalist',
    music: 'Jazz',
    movies: 'Sci-Fi',
    books: 'Philosophy',
    art: 'Minimalism',
    podcasts: 'Tech'
  }}
  answers={{
    music: ['Jazz', 'Classical'],
    movies: ['Sci-Fi'],
    books: ['Philosophy', 'Fiction'],
    art: ['Minimalism'],
    podcasts: ['Tech']
  }}
  onContinue={() => navigate('/feed')}
/>
```

---

## Data Integration

### Current Implementation (Static)

The current implementation uses static data from `src/data/onboardingQuestions.js`:

```javascript
import { onboardingQuestions, generateTasteDNA } from '@/data/onboardingQuestions';
```

### Future Backend Integration

For backend integration, the components will need to:

1. **Fetch Questions**: Call API to get Section 1 questions
2. **Submit Section 1**: Send answers and receive Section 2 questions
3. **Complete Quiz**: Submit all answers and receive generated DNA
4. **Handle Loading**: Show loading states during API calls
5. **Handle Errors**: Display error messages and retry options

**Example API Integration:**

```javascript
import { vibeGraphAPI } from '@/services/api';

const OnboardingPage = ({ onComplete }) => {
  const [phase, setPhase] = useState('section1');
  const [sessionId, setSessionId] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const startQuiz = async () => {
      try {
        const response = await vibeGraphAPI.quiz.startSection1();
        setSessionId(response.sessionId);
        setQuestions(response.questions);
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    startQuiz();
  }, []);

  // ... rest of implementation
};
```

---

## Styling and Animations

### Design Tokens

```css
/* Typography */
--text-28: 28px;      /* Large headings */
--text-13: 13px;      /* Body text */
--text-11: 11px;      /* Small labels */

/* Colors */
--background: hsl(0 0% 5%);
--foreground: hsl(0 0% 95%);
--surface: hsl(0 0% 10%);
--muted-foreground: hsl(0 0% 55%);

/* Transitions */
--duration-180: 180ms;
--ease-out: cubic-bezier(0.33, 1, 0.68, 1);
```

### Animations

**Fade In Up:**
```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

**Hover Lift:**
```css
.hover-lift:hover {
  transform: translateY(-2px);
  transition: transform 180ms ease-out;
}
```

---

## Accessibility

### Keyboard Navigation

- All interactive elements are keyboard accessible
- Tab order follows visual flow
- Enter/Space activates buttons and tiles

### Screen Readers

- Semantic HTML elements used throughout
- Progress announced via aria-live regions
- Button states clearly communicated

### Color Contrast

- All text meets WCAG AA standards
- Interactive elements have sufficient contrast
- Focus indicators are visible

---

## Testing

### Unit Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import OnboardingPage from './OnboardingPage';

test('advances to next question on Next click', () => {
  const onComplete = vi.fn();
  render(<OnboardingPage onComplete={onComplete} />);
  
  // Select an option
  const option = screen.getByText('Jazz');
  fireEvent.click(option);
  
  // Click Next
  const nextButton = screen.getByText('Next');
  fireEvent.click(nextButton);
  
  // Verify question changed
  expect(screen.getByText(/Question 2/)).toBeInTheDocument();
});
```

### Integration Tests

```javascript
test('completes full onboarding flow', async () => {
  const onComplete = vi.fn();
  render(<OnboardingPage onComplete={onComplete} />);
  
  // Answer all questions
  for (let i = 0; i < 5; i++) {
    const option = screen.getAllByRole('button')[0];
    fireEvent.click(option);
    
    const nextButton = screen.getByText(i === 4 ? 'Finish' : 'Next');
    fireEvent.click(nextButton);
  }
  
  // Verify DNA card shown
  expect(screen.getByText(/Your Taste DNA/)).toBeInTheDocument();
  
  // Complete onboarding
  const enterButton = screen.getByText('Enter Feed');
  fireEvent.click(enterButton);
  
  expect(onComplete).toHaveBeenCalled();
});
```

---

## Performance Considerations

- **Lazy Loading**: Radar chart library loaded on demand
- **Memoization**: Use `useMemo` for score calculations
- **Debouncing**: Option clicks debounced to prevent rapid state updates
- **Animation Performance**: CSS transforms used for smooth animations

---

## Future Enhancements

- [ ] Add question skip functionality
- [ ] Implement answer editing (go back to previous questions)
- [ ] Add progress save/resume capability
- [ ] Support for image-based options
- [ ] Animated transitions between questions
- [ ] Social sharing with custom graphics
- [ ] A/B testing for question variations
- [ ] Analytics tracking for completion rates

---

## Related Documentation

- [Frontend README](../README.md)
- [API Service Documentation](../services/api.md)
- [Design System](../DESIGN_SYSTEM.md)
- [Onboarding System Overview](../ONBOARDING_SYSTEM.md)
