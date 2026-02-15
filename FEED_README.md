# VibeGraph Feed UI

A clean, minimal React feed page UI for a social cultural platform - UI only, no backend or authentication.

## Quick Start

```bash
npm install
npm run dev
```

Open your browser to the local dev server URL (typically `http://localhost:5173`)

## Structure

```
src/
├── App.jsx                    # Main app component (Sidebar + Feed)
├── App.css                    # App layout styles
├── pages/
│   ├── Feed.jsx              # Feed page with sections
│   └── Feed.css              # Feed page styles
├── components/
│   ├── Sidebar/
│   │   ├── Sidebar.jsx       # Left navigation sidebar
│   │   └── Sidebar.css       # Sidebar styles
│   ├── FeedCard/
│   │   ├── FeedCard.jsx      # Pinterest-style card
│   │   └── FeedCard.css      # Card styles
│   └── FeedSection/
│       ├── FeedSection.jsx   # Section with grid of cards
│       └── FeedSection.css   # Section styles
└── styles/
    └── index.css             # Global styles & design tokens
```

## Features

### Layout
- Fixed left sidebar with navigation
- Scrollable main feed area
- Fully responsive design

### Sidebar Navigation
- VibeGraph logo
- Main navigation: Feed, Explore, Moodboards, Vibes, Profile
- Category navigation: Books, Music, Films, Art
- Settings at bottom

### Feed Sections
- Music (4 items)
- Movies (4 items)
- Art & Pictures (4 items)
- Books (3 items)

### Card Design
- Pinterest-style layout
- Large images (3:4 aspect ratio)
- Category tags
- Smooth hover effects
- Responsive grid (4 → 3 → 2 columns)

## Design System

All styling uses CSS variables defined in `src/styles/index.css`:

- Colors: Neutral palette with vibrant accents
- Typography: Instrument Serif (display) + Inter (body)
- Spacing: Consistent scale from xs to 3xl
- Dark mode ready (toggle via `data-theme="dark"` on html element)

## Mock Data

Located in `src/pages/Feed.jsx` - uses Unsplash placeholder images.

## Customization

### Change Grid Columns
Edit `src/components/FeedSection/FeedSection.css`:
```css
.feed-section-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
}
```

### Change Card Aspect Ratio
Edit `src/components/FeedCard/FeedCard.css`:
```css
.feed-card-image {
  aspect-ratio: 3 / 4; /* or 1 / 1 for square */
}
```

### Add New Section
In `src/pages/Feed.jsx`:
```jsx
<FeedSection 
  title="Your Section" 
  items={yourData}
/>
```

## What's NOT Included

- No backend/API integration
- No authentication
- No routing (single page only)
- No state management
- No user interactions (likes, saves, etc.)
- No detail views

This is purely a UI foundation to build upon.

## Tech Stack

- React 18
- Vite
- Framer Motion (animations)
- Lucide React (icons)
- CSS Variables (styling)
