# Video Card System Documentation

## Overview

The feed now supports short-form video content through a dedicated VideoCard component. Tall layout variants automatically render as vertical video cards, creating a Reels/TikTok/Shorts-style experience within the premium SaaS aesthetic.

## VideoCard Component

**Location:** `src/components/VideoCard.jsx`

A specialized card component for displaying short-form video content with a vertical 9:16 aspect ratio.

### Visual Structure

```
┌─────────────────────────┐
│                         │
│   VIDEO THUMBNAIL       │
│      (9:16)             │
│                         │
│         ▶               │  Play indicator
│                         │
│   [VIDEO]               │  Video badge
│                         │
├─────────────────────────┤
│ Title        [Category] │
│ Source                  │
└─────────────────────────┘
```

### Key Features

**1. Vertical Aspect Ratio**
- `aspect-[9/16]` - Portrait orientation
- Optimized for mobile-first video content
- Matches Reels/TikTok/Shorts format

**2. Play Indicator**
- Centered play icon using Lucide `Play`
- Subtle backdrop: `bg-black/40 backdrop-blur-sm`
- Icon size: `w-6 h-6`
- Filled white icon with 80% opacity
- Minimal, non-intrusive design

**3. Video Badge**
- Top-left corner label
- Text: "VIDEO" in uppercase
- Style: `text-11 uppercase tracking-wide`
- Background: `bg-black/50 backdrop-blur-sm`
- Border: `border-white/10`
- Clearly identifies video content

**4. Hover Interactions**
- Card: `hover:bg-surface/80 hover:-translate-y-0.5`
- Thumbnail: `group-hover:scale-[1.02]`
- Transition: `duration-180 ease-out` (card), `duration-200 ease-out` (image)
- Consistent with existing MediaCard behavior

### Component Props

```jsx
<VideoCard
  title="Studio Session – Lo-fi Beats"
  category="Music"
  image="https://..."
  source="YouTube"
/>
```

**Props:**
- `title` (string): Video title
- `category` (string): Content category (Music, Movie, etc.)
- `image` (string): Video thumbnail URL
- `source` (string): Platform source (YouTube, TikTok, Instagram, Vimeo)

## Integration with Feed

### FeedItem Component Updates

**Location:** `src/components/FeedItem.jsx`

The FeedItem wrapper now conditionally renders VideoCard for tall variants:

```jsx
// Tall cards render as video cards
if (variant === 'tall') {
  return (
    <div className={variantClasses[variant]}>
      <VideoCard {...item} />
    </div>
  );
}
```

### Grid Layout

**Tall Video Cards:**
```css
col-span-12           /* Mobile: Full width */
sm:col-span-6         /* Tablet: 2 per row */
lg:col-span-4         /* Desktop: 3 per row */
xl:col-span-3         /* Large: 4 per row */
row-span-2            /* Double height */
```

The `row-span-2` makes video cards twice the height of normal cards, creating visual prominence.

## Feed Data Structure

### Video Items

When `variant === 'tall'`, the feed generates video-specific data:

```javascript
{
  id: "item-5",
  type: "video",
  category: "Music",
  title: "Studio Session – Lo-fi Beats",
  image: "https://images.unsplash.com/photo-...",
  source: "YouTube",
  variant: "tall"
}
```

### Video Sources

Supported platforms:
- YouTube
- TikTok
- Instagram
- Vimeo

Randomly assigned to video items.

### Video Thumbnails

**Image Collection:** `imageCollections.videos`

Curated vertical images from Unsplash:
```javascript
videos: [
  'https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800&q=80',
  'https://images.unsplash.com/photo-1574169208507-84376144848b?w=800&q=80',
  'https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800&q=80',
  'https://images.unsplash.com/photo-1492691527719-9d1e07e534b4?w=800&q=80',
]
```

### Video Titles

**Title Collection:** `titles.videos`

```javascript
videos: [
  'Studio Session – Lo-fi Beats',
  'Behind the Scenes',
  'Creative Process',
  'Day in the Life'
]
```

## Design System Compliance

### Maintained Elements

✓ True black background `#000000`
✓ Surface layers `bg-surface/50`
✓ Borders `border-white/10`
✓ IBM Plex Mono typography
✓ Subtle transitions (180-200ms)
✓ Category color system
✓ Hover states and interactions
✓ Responsive grid behavior

### No Changes To

✓ Existing MediaCard component
✓ Color palette
✓ Typography scale
✓ Spacing system
✓ Border radius values
✓ Transition timing

## Visual Comparison

### MediaCard (Normal)
- Aspect ratio: 4:5 (portrait)
- No play indicator
- No video badge
- Standard content card

### MediaCard (Featured)
- Aspect ratio: 16:9 (landscape)
- Larger size (6 columns)
- No play indicator
- Emphasized content card

### VideoCard (Tall)
- Aspect ratio: 9:16 (vertical)
- Play indicator centered
- "VIDEO" badge top-left
- Double height (row-span-2)
- Short-form video content

## Responsive Behavior

### Mobile (<768px)
- All cards stack vertically
- Video cards: `col-span-12`
- Full width, maintains 9:16 ratio
- Play indicator remains visible

### Tablet (768px - 1023px)
- Video cards: `col-span-6` (2 per row)
- Vertical format preserved
- Balanced with other content

### Desktop (1024px - 1279px)
- Video cards: `col-span-4` (3 per row)
- Integrated into grid flow
- Double height creates visual interest

### Large Desktop (1280px+)
- Video cards: `col-span-3` (4 per row)
- Seamless grid integration
- Maintains vertical emphasis

## Usage Examples

### Basic Video Card

```jsx
<VideoCard
  title="Midnight Jazz Session"
  category="Music"
  image="https://images.unsplash.com/photo-..."
  source="YouTube"
/>
```

### In Feed Context

```jsx
{feedItems.map((item) => (
  <FeedItem
    key={item.id}
    item={item}
    variant={item.variant}
  />
))}
```

The FeedItem automatically renders VideoCard when `variant === 'tall'`.

## Customization

### Adjust Play Icon

Change icon size or style:

```jsx
// Larger icon
<Play className="w-8 h-8 text-white/80 fill-white/80" strokeWidth={0} />

// Different background
<div className="bg-white/20 rounded-full p-4 backdrop-blur-md">
  <Play className="w-6 h-6 text-white" strokeWidth={0} />
</div>
```

### Modify Video Badge

Change badge text or position:

```jsx
// Different text
<div className="...">
  Reel
</div>

// Different position (top-right)
<div className="absolute top-3 right-3">
  <div className="...">
    Video
  </div>
</div>
```

### Add Duration Badge

Display video length:

```jsx
// Add to VideoCard props
duration="2:34"

// Render in component
<div className="absolute bottom-3 right-3">
  <div className="text-11 px-2 py-1 rounded bg-black/70 backdrop-blur-sm text-white/90 font-mono">
    {duration}
  </div>
</div>
```

### Custom Aspect Ratios

Change video format:

```jsx
// Square format (1:1)
<div className="relative overflow-hidden aspect-square">

// Wider vertical (3:4)
<div className="relative overflow-hidden aspect-[3/4]">

// Ultra vertical (9:21)
<div className="relative overflow-hidden aspect-[9/21]">
```

## Future Enhancements

### Video Playback

Add actual video support:

```jsx
<video
  src={videoUrl}
  poster={image}
  className="w-full h-full object-cover"
  controls={false}
  loop
  muted
  playsInline
/>
```

### Auto-play on Hover

Play video preview on hover:

```jsx
const [isHovered, setIsHovered] = useState(false);

<div
  onMouseEnter={() => setIsHovered(true)}
  onMouseLeave={() => setIsHovered(false)}
>
  <video
    ref={videoRef}
    onMouseEnter={() => videoRef.current?.play()}
    onMouseLeave={() => videoRef.current?.pause()}
  />
</div>
```

### View Count

Display engagement metrics:

```jsx
<div className="absolute bottom-3 left-3 flex items-center gap-1">
  <Eye className="w-3 h-3" />
  <span className="text-11 text-white/80">2.4M</span>
</div>
```

### Sound Indicator

Show audio status:

```jsx
<div className="absolute bottom-3 right-3">
  {isMuted ? (
    <VolumeX className="w-4 h-4 text-white/80" />
  ) : (
    <Volume2 className="w-4 h-4 text-white/80" />
  )}
</div>
```

### Creator Avatar

Display content creator:

```jsx
<div className="absolute bottom-3 left-3 flex items-center gap-2">
  <Avatar className="w-6 h-6">
    <AvatarImage src={creatorAvatar} />
  </Avatar>
  <span className="text-11 text-white/90">{creatorName}</span>
</div>
```

## Performance Considerations

### Image Loading

- Uses `loading="lazy"` for deferred loading
- Optimized Unsplash URLs with `w=800&q=80`
- Reduces initial page load

### Transition Performance

- Uses GPU-accelerated properties (`transform`, `opacity`)
- Avoids layout-triggering properties
- Smooth 60fps animations

### Grid Layout

- CSS Grid handles layout efficiently
- No JavaScript calculations
- Responsive without media query JavaScript

## Accessibility

### Play Indicator

- Visible play icon indicates video content
- Clear visual affordance
- No reliance on color alone

### Video Badge

- Text label "VIDEO" provides context
- High contrast against background
- Readable at all sizes

### Keyboard Navigation

Future enhancement:
```jsx
<div
  tabIndex={0}
  role="button"
  aria-label={`Play video: ${title}`}
  onKeyPress={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handlePlay();
    }
  }}
>
```

## Testing

### Visual Testing

1. Verify video cards appear in feed
2. Check 9:16 aspect ratio maintained
3. Confirm play indicator centered
4. Validate video badge visible
5. Test hover interactions

### Responsive Testing

- Mobile (375px): Full width, vertical
- Tablet (768px): 2 per row
- Desktop (1024px): 3 per row
- Large (1440px): 4 per row

### Variant Distribution

Check that tall variants render as video cards:

```javascript
const tallCards = feedItems.filter(item => item.variant === 'tall');
console.log('Video cards:', tallCards.length);
```

## Summary

The VideoCard component extends the feed with short-form video support while maintaining the premium SaaS aesthetic. Tall layout variants automatically render as vertical video cards with play indicators and video badges, creating a modern, dynamic feed experience similar to Instagram Reels or TikTok, but with the minimal, developer-focused design of Linear and Notion.

**Key Features:**
- 9:16 vertical aspect ratio
- Centered play indicator
- Video badge label
- Consistent hover interactions
- Seamless grid integration
- Responsive at all breakpoints
- No design system changes
