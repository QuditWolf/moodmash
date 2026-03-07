# Onboarding System Documentation

## Overview

A Spotify/X-style onboarding flow that collects user taste signals through visual tile selection before entering the main feed.

## User Flow

```
App Load → Check localStorage
  ↓
  ├─ Has taste_profile → Skip to Feed
  └─ No taste_profile → Show Onboarding
       ↓
       Question 1-10 (Visual tile selection)
       ↓
       Taste DNA Summary Card
       ↓
       Store in localStorage → Enter Feed
```

## Components

### OnboardingPage
**Location**: `src/components/onboarding/OnboardingPage.jsx`

Main orchestrator component that manages:
- Question progression
- Answer state management
- Taste DNA generation
- localStorage persistence

**Props:**
- `onComplete`: Callback when onboarding finishes

**State:**
```javascript
{
  currentQuestionIndex: 0,
  answers: {
    music: ['Indie Rock', 'Lo-fi'],
    movies: ['Sci-Fi', 'Psychological'],
    // ... other categories
  },
  showTasteDNA: false,
  tasteDNA: null
}
```

### QuestionScreen
**Location**: `src/components/onboarding/QuestionScreen.jsx`

Displays individual question with tile grid.

**Props:**
- `question`: Question object from onboardingQuestions
- `currentIndex`: Current question number (0-based)
- `totalQuestions`: Total number of questions
- `selectedOptions`: Array of selected option strings
- `onToggleOption`: Handler for tile selection
- `onNext`: Handler for next button

**Features:**
- Progress bar at top
- Question title (text-28)
- Responsive tile grid (2/3/4 columns)
- Next/Finish button (disabled until selection)

### OptionTile
**Location**: `src/components/onboarding/OptionTile.jsx`

Individual selectable tile component.

**Props:**
- `label`: Option text
- `selected`: Boolean selection state
- `onClick`: Click handler

**States:**
- Default: `bg-surface/50 border-white/10`
- Hover: `hover:bg-surface/80 hover:border-white/20 hover:-translate-y-0.5`
- Selected: `bg-surface/80 border-white/20` + check icon

### TasteDNACard
**Location**: `src/components/onboarding/TasteDNACard.jsx`

Summary card showing user's taste profile.

**Props:**
- `tasteDNA`: Generated taste DNA object
- `onContinue`: Handler for continue button

**Features:**
- Archetype display
- Top 3 selections per category
- Share functionality (native share API or clipboard)
- Continue to Feed button

### ProgressBar
**Location**: `src/components/onboarding/ProgressBar.jsx`

Minimal progress indicator.

**Props:**
- `current`: Current question number
- `total`: Total questions

**Display:**
- "Question X of Y" text
- Percentage
- Animated progress bar

## Data Structure

### onboardingQuestions
**Location**: `src/data/onboardingQuestions.js`

Array of 10 question objects:

```javascript
{
  id: 'music',           // Unique identifier
  title: 'Pick music you vibe with',
  category: 'music',     // Category for grouping
  options: [             // 12 selectable options
    'Indie Rock',
    'Hip Hop',
    // ...
  ]
}
```

**Categories:**
1. Music
2. Movies
3. Books
4. Art
5. Podcasts
6. Articles
7. Creative interests
8. Content mood
9. Content format
10. Discovery style

### Taste DNA Generation

**Function**: `generateTasteDNA(answers)`

Generates archetype and top selections:

**Archetypes:**
- The Minimalist (< 15 selections)
- The Omnivore (> 30 selections)
- The Creative (high art/creative)
- The Intellectual (high articles/books)
- The Explorer (default)

**Output:**
```javascript
{
  archetype: 'The Explorer',
  music: 'Indie Rock / Lo-fi / Electronic',
  movies: 'Sci-Fi / Psychological / Thriller',
  books: 'Philosophy / Startups / Psychology',
  art: 'Abstract / Minimalism / Digital Art',
  podcasts: 'Tech Talks / Design / Startups'
}
```

## Storage

### localStorage Key: `taste_profile`

**Structure:**
```javascript
{
  answers: {
    music: ['Indie Rock', 'Lo-fi'],
    movies: ['Sci-Fi', 'Psychological'],
    // ... all categories
  },
  tasteDNA: {
    archetype: 'The Explorer',
    music: 'Indie Rock / Lo-fi / Electronic',
    // ... other categories
  },
  completedAt: '2024-03-07T12:00:00.000Z'
}
```

**Usage:**
```javascript
// Check if onboarding completed
const profile = localStorage.getItem('taste_profile');
if (profile) {
  const data = JSON.parse(profile);
  // Use data.answers or data.tasteDNA
}

// Clear onboarding (for testing)
localStorage.removeItem('taste_profile');
```

## Design System Compliance

### Colors
- Background: `#000000` (pure black)
- Tiles: `bg-surface/50` with `border-white/10`
- Selected: `bg-surface/80` with `border-white/20`
- Text: Existing foreground/muted-foreground tokens

### Typography
- Question title: `text-28` (28px)
- Option tiles: `text-13` (13px)
- Progress: `text-13` (13px)
- DNA labels: `text-11` (11px uppercase)
- Font: IBM Plex Mono (inherited)

### Spacing
- Container padding: `px-6 py-12`
- Tile grid gap: `gap-3`
- Section spacing: `mb-8`, `mb-12`
- Follows existing spacing scale

### Interactions
- Tile hover: `hover:-translate-y-0.5`
- Transitions: `duration-180 ease-out`
- Button hover: `hover:-translate-y-0.5`
- Progress bar: `duration-300 ease-out`

### Responsive Grid
```css
grid-cols-2           /* Mobile */
sm:grid-cols-3        /* Tablet */
lg:grid-cols-4        /* Desktop */
```

## Integration with App

### App.jsx Changes

```javascript
// Added state management
const [showOnboarding, setShowOnboarding] = useState(true);
const [isLoading, setIsLoading] = useState(true);

// Check localStorage on mount
useEffect(() => {
  const tasteProfile = localStorage.getItem('taste_profile');
  if (tasteProfile) {
    setShowOnboarding(false);
  }
  setIsLoading(false);
}, []);

// Conditional rendering
if (showOnboarding) {
  return <OnboardingPage onComplete={handleOnboardingComplete} />;
}
```

**No changes to:**
- FeedPage component
- MediaCard component
- Sidebar component
- Global styles
- Color tokens
- Typography system

## Testing

### Test Onboarding Flow
1. Clear localStorage: `localStorage.removeItem('taste_profile')`
2. Refresh page
3. Should show onboarding

### Test Skip Onboarding
1. Complete onboarding once
2. Refresh page
3. Should skip directly to feed

### Test Answers Persistence
```javascript
// View stored answers
const profile = JSON.parse(localStorage.getItem('taste_profile'));
console.log(profile.answers);
console.log(profile.tasteDNA);
```

## Future Enhancements

### Backend Integration
Replace localStorage with API calls:

```javascript
// After onboarding completion
const response = await fetch('/api/taste-profile', {
  method: 'POST',
  body: JSON.stringify({ answers, tasteDNA })
});

// On app load
const response = await fetch('/api/taste-profile');
const profile = await response.json();
```

### Personalized Feed
Use taste profile to filter/sort feed items:

```javascript
const profile = JSON.parse(localStorage.getItem('taste_profile'));
const preferences = profile.answers;

// Filter feed based on preferences
const personalizedFeed = feedItems.filter(item => 
  preferences[item.category.toLowerCase()]?.length > 0
);
```

### Edit Profile
Add settings page to modify taste profile:

```javascript
// In settings/profile page
const profile = JSON.parse(localStorage.getItem('taste_profile'));
// Show editable form with current answers
// Update localStorage on save
```

### Analytics
Track onboarding completion and selections:

```javascript
// Track question completion
analytics.track('onboarding_question_completed', {
  questionId: question.id,
  selections: selectedOptions,
  questionIndex: currentIndex
});

// Track onboarding completion
analytics.track('onboarding_completed', {
  archetype: tasteDNA.archetype,
  totalSelections: Object.values(answers).flat().length
});
```

## Troubleshooting

### Onboarding shows every time
- Check localStorage is enabled
- Verify `taste_profile` key is being set
- Check browser console for errors

### Tiles not responding
- Verify Lucide React is installed: `npm install lucide-react`
- Check onClick handlers are connected

### Styling issues
- Ensure Tailwind is processing onboarding components
- Verify no CSS conflicts with existing styles
- Check responsive breakpoints match design system

### Progress bar not animating
- Verify transition classes are applied
- Check percentage calculation is correct
- Ensure width style is being updated

## File Structure

```
src/
├── components/
│   └── onboarding/
│       ├── OnboardingPage.jsx      # Main orchestrator
│       ├── QuestionScreen.jsx      # Question display
│       ├── OptionTile.jsx          # Selectable tile
│       ├── TasteDNACard.jsx        # Summary card
│       └── ProgressBar.jsx         # Progress indicator
├── data/
│   └── onboardingQuestions.js      # Questions + DNA logic
└── App.jsx                         # Updated with routing logic
```

## Summary

The onboarding system is fully integrated and follows all design system guidelines. It:
- ✓ Matches premium SaaS aesthetic
- ✓ Uses existing design tokens
- ✓ Maintains consistent interactions
- ✓ Works responsively
- ✓ Stores data locally
- ✓ Does not modify existing components
- ✓ Ready for backend integration
