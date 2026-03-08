# Feed Page Structure

## Overview
A clean, minimal React feed page UI for a social cultural platform with Pinterest-style cards and sectioned content.

## Components Created

### 1. Feed Page (`src/pages/Feed.jsx`)
- Main feed container with header
- Displays multiple content sections (Music, Movies, Art, Books)
- Uses mock data for demonstration
- Smooth fade-in animation

### 2. FeedSection (`src/components/FeedSection/FeedSection.jsx`)
- Section container with title and "View All" button
- Responsive grid layout
- Staggered animation for cards
- Adapts to different screen sizes

### 3. FeedCard (`src/components/FeedCard/FeedCard.jsx`)
- Pinterest-style card with large image
- Category tag and title
- Hover effects (lift and scale)
- 3:4 aspect ratio for images
- Rounded corners and subtle shadow

## Layout Structure

```
┌─────────────────────────────────────────┐
│  Navbar (existing)                      │
├──────────┬──────────────────────────────┤
│          │  Feed Header                 │
│          │  - Title                     │
│          │  - Description               │
│          ├──────────────────────────────┤
│ Sidebar  │  Section: Music              │
│          │  ┌────┬────┬────┬────┐      │
│ - Logo   │  │Card│Card│Card│Card│      │
│ - Feed   │  └────┴────┴────┴────┘      │
│ - Explore├──────────────────────────────┤
│ - Mood   │  Section: Movies             │
│ - Vibes  │  ┌────┬────┬────┬────┐      │
│ - Profile│  │Card│Card│Card│Card│      │
│          │  └────┴────┴────┴────┘      │
│          ├──────────────────────────────┤
│          │  Section: Art & Pictures     │
│          │  ┌────┬────┬────┬────┐      │
│          │  │Card│Card│Card│Card│      │
│          │  └────┴────┴────┴────┘      │
│          ├──────────────────────────────┤
│          │  Section: Books              │
│          │  ┌────┬────┬────┐           │
│          │  │Card│Card│Card│           │
│          │  └────┴────┴────┘           │
└──────────┴──────────────────────────────┘
```

## Features

### Sidebar Updates
- Added "VibeGraph" logo at top
- Updated navigation items:
  - Feed (new, with Layers icon)
  - Explore
  - Moodboards
  - Vibes
  - Profile

### Responsive Design
- Desktop: 4 columns grid
- Tablet: 3 columns grid
- Mobile: 2 columns grid
- Fluid card sizing with `minmax(280px, 1fr)`

### Styling
- Minimal, clean aesthetic
- Neutral color palette from existing design system
- Dark mode support (inherited from theme)
- Smooth transitions and hover effects
- Pinterest-inspired card layout

## Mock Data
Located in `src/pages/Feed.jsx`:
- Music: 4 items (Jazz, Electronic, Acoustic, Rock)
- Movies: 4 items (Drama, Sci-Fi, Noir, Indie)
- Art: 4 items (Abstract, Minimalism, Street Art, Contemporary)
- Books: 3 items (Fiction, Poetry, Philosophy)

Uses Unsplash placeholder images for demonstration.

## Usage

Navigate to `/feed` to see the feed page. The route is now the default landing page after login.

## Customization

### Adding New Sections
```jsx
<FeedSection 
  title="Your Section Title" 
  items={yourMockData}
/>
```

### Modifying Card Layout
Edit `src/components/FeedSection/FeedSection.css`:
```css
.feed-section-grid {
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-xl);
}
```

### Changing Card Aspect Ratio
Edit `src/components/FeedCard/FeedCard.css`:
```css
.feed-card-image {
  aspect-ratio: 3 / 4; /* Change to 1 / 1 for square, 16 / 9 for wide */
}
```

## Next Steps (Not Implemented)
- Backend integration
- Real data fetching
- Infinite scroll
- Filtering and sorting
- User interactions (like, save, share)
- Detail view for cards
