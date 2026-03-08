# Variable Grid Layout System

## Overview

The feed now uses a dynamic variable grid layout that creates visual hierarchy and improves content discovery, similar to Instagram and Pinterest feeds. Cards randomly receive different layout variants while maintaining the premium design system.

## Layout Variants

### Normal Card
**Column Spans:**
- Mobile: `col-span-12` (full width)
- Tablet: `col-span-6` (2 per row)
- Desktop: `col-span-4` (3 per row)
- Large: `col-span-3` (4 per row)

**Image Aspect:** `4:5` (portrait)

**Frequency:** ~57% of cards (4 out of 7)

### Featured Card
**Column Spans:**
- Mobile: `col-span-12` (full width)
- Tablet: `col-span-12` (full width)
- Desktop: `col-span-8` (large)
- Large: `col-span-6` (half width)

**Image Aspect:** `16:9` (landscape)

**Frequency:** ~14% of cards (1 out of 7)

**Purpose:** Highlights important or high-quality content

### Tall Card
**Column Spans:**
- Mobile: `col-span-12` (full width)
- Tablet: `col-span-6` (2 per row)
- Desktop: `col-span-4` (3 per row)
- Large: `col-span-3` (4 per row)

**Image Aspect:** `4:5` (portrait)

**Frequency:** ~14% of cards (1 out of 7)

**Purpose:** Creates vertical rhythm variation

### Wide Card
**Column Spans:**
- Mobile: `col-span-12` (full width)
- Tablet: `col-span-12` (full width)
- Desktop: `col-span-6` (2 per row)
- Large: `col-span-6` (2 per row)

**Image Aspect:** `4:5` (portrait)

**Frequency:** ~14% of cards (1 out of 7)

**Purpose:** Creates horizontal emphasis

## Implementation

### FeedItem Component
**Location:** `src/components/FeedItem.jsx`

Wrapper component that applies layout variants to MediaCard:

```jsx
const FeedItem = ({ item, variant = 'normal' }) => {
  const variantClasses = {
    normal: 'col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3',
    featured: 'col-span-12 sm:col-span-12 lg:col-span-8 xl:col-span-6',
    tall: 'col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3',
    wide: 'col-span-12 sm:col-span-12 lg:col-span-6 xl:col-span-6'
  };

  const imageAspectClass = variant === 'featured' ? 'aspect-[16/9]' : 'aspect-[4/5]';

  return (
    <div className={variantClasses[variant]}>
      <MediaCard
        {...item}
        imageAspect={imageAspectClass}
        isFeatured={variant === 'featured'}
      />
    </div>
  );
};
```

### Random Variant Assignment

**Function:** `getRandomVariant()`

```javascript
const getRandomVariant = () => {
  const variants = ['normal', 'normal', 'normal', 'normal', 'featured', 'tall', 'wide'];
  return variants[Math.floor(Math.random() * variants.length)];
};
```

**Distribution:**
- 4x Normal (57%)
- 1x Featured (14%)
- 1x Tall (14%)
- 1x Wide (14%)

### MediaCard Updates

**New Props:**
- `imageAspect`: Dynamic aspect ratio class (default: `aspect-[4/5]`)
- `isFeatured`: Boolean flag for featured cards

**Changes:**
```jsx
// Before
<div className="relative overflow-hidden aspect-[4/5]">

// After
<div className={`relative overflow-hidden ${imageAspect}`}>
```

## Visual Rhythm

The variable grid creates a curated, dynamic feel:

```
┌─────┬─────┬─────┬─────┐
│  N  │  N  │  N  │  N  │  Normal cards (4:5)
├─────┴─────┴─────┴─────┤
│      Featured (16:9)   │  Large featured card
├─────┬─────┬─────┬─────┤
│  N  │  T  │  N  │  N  │  Tall card mixed in
├─────┴─────┴─────┴─────┤
│    Wide    │    Wide   │  Wide cards
└────────────┴───────────┘
```

## Responsive Behavior

### Mobile (<768px)
- All cards stack vertically
- Full width: `col-span-12`
- Maintains aspect ratios

### Tablet (768px - 1023px)
- Normal/Tall: 2 per row
- Featured/Wide: Full width
- Creates balanced layout

### Desktop (1024px - 1279px)
- Normal/Tall: 3 per row
- Featured: Large (8 columns)
- Wide: Half width (6 columns)

### Large Desktop (1280px+)
- Normal/Tall: 4 per row
- Featured: Half width (6 columns)
- Wide: Half width (6 columns)

## Design System Compliance

### Maintained Elements
✓ True black background `#000000`
✓ Surface layers `bg-surface/50`
✓ Borders `border-white/10`
✓ IBM Plex Mono typography
✓ Subtle transitions (180-200ms)
✓ Hover states (`hover:-translate-y-0.5`)
✓ 12-column grid system
✓ Gap spacing (`gap-6`)

### No Changes To
✓ MediaCard internal structure
✓ Category colors
✓ Typography scale
✓ Interaction timing
✓ Border radius
✓ Padding values

## Benefits

### Visual Hierarchy
- Featured cards draw attention to important content
- Variable sizes create focal points
- Breaks monotony of uniform grid

### Discovery
- Dynamic layout encourages exploration
- Different sizes suggest different content types
- More engaging than static grid

### Curation Feel
- Feels hand-picked and intentional
- Similar to Instagram/Pinterest discovery
- Premium, editorial aesthetic

### Flexibility
- Easy to adjust variant distribution
- Can add new variants
- Maintains responsive behavior

## Customization

### Adjust Variant Distribution

Change the frequency of variants:

```javascript
// More featured cards
const variants = ['normal', 'normal', 'featured', 'featured', 'tall', 'wide'];

// More uniform (less variation)
const variants = ['normal', 'normal', 'normal', 'normal', 'normal', 'featured'];

// More dynamic (more variation)
const variants = ['normal', 'featured', 'tall', 'wide'];
```

### Add New Variants

Create custom layout patterns:

```javascript
// In FeedItem.jsx
const variantClasses = {
  normal: 'col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3',
  featured: 'col-span-12 sm:col-span-12 lg:col-span-8 xl:col-span-6',
  tall: 'col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3',
  wide: 'col-span-12 sm:col-span-12 lg:col-span-6 xl:col-span-6',
  // New variant
  hero: 'col-span-12'  // Full width at all breakpoints
};
```

### Control Specific Cards

Assign variants based on content:

```javascript
// In generateUnifiedFeed
const getVariantForItem = (item, index) => {
  // First item is always featured
  if (index === 0) return 'featured';
  
  // Every 5th item is wide
  if (index % 5 === 0) return 'wide';
  
  // High-quality content gets featured
  if (item.quality === 'high') return 'featured';
  
  // Default to random
  return getRandomVariant();
};
```

## Performance

### No Impact
- Same number of components rendered
- No additional JavaScript overhead
- CSS Grid handles layout efficiently
- Images lazy load as before

### Optimization
- Variant assigned once during feed generation
- No runtime calculations
- Static class names (Tailwind optimized)

## Future Enhancements

### Smart Variant Assignment
- Use content type to determine variant
- Featured cards for high engagement content
- Tall cards for portrait images
- Wide cards for landscape images

### User Preferences
- Allow users to toggle grid density
- Save preferred layout style
- Adjust variant distribution based on taste profile

### Animation
- Subtle entrance animations per variant
- Stagger effect on scroll
- Smooth transitions when resizing

### Content-Aware
- Analyze image dimensions
- Assign optimal variant automatically
- Prevent layout shift

## Testing

### Visual Testing
1. Refresh page multiple times
2. Verify different layouts appear
3. Check responsive behavior at all breakpoints
4. Ensure no layout breaks

### Variant Distribution
```javascript
// Count variants in feed
const variantCounts = feedItems.reduce((acc, item) => {
  acc[item.variant] = (acc[item.variant] || 0) + 1;
  return acc;
}, {});
console.log(variantCounts);
```

### Responsive Testing
- Test at 375px (mobile)
- Test at 768px (tablet)
- Test at 1024px (desktop)
- Test at 1440px (large desktop)

## Summary

The variable grid layout system transforms the feed from a uniform grid into a dynamic, curated discovery experience while maintaining the premium design system. Cards randomly receive layout variants that create visual hierarchy and improve engagement, similar to modern social media discovery feeds.

**Key Features:**
- 4 layout variants (normal, featured, tall, wide)
- Random distribution with controlled frequency
- Responsive at all breakpoints
- No design system changes
- Easy to customize and extend
