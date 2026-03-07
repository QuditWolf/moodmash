# Masonry Layout System Documentation

## Overview

The feed has been converted from a CSS Grid with row-spanning to a masonry-style columns layout. This eliminates vertical gaps caused by tall cards and creates a fluid, Pinterest-style discovery feed.

## Problem Solved

### Previous Issue (CSS Grid with row-span)

```
┌─────┬─────┬─────┬─────┐
│  N  │  N  │  T  │  N  │
│     │     │  A  │     │
├─────┼─────┤  L  ├─────┤
│  N  │  N  │  L  │  N  │  ← Empty gaps here
│     │     │     │     │
└─────┴─────┴─────┴─────┘
```

**Problems:**
- `row-span-2` created fixed-height rows
- Tall cards left empty space in adjacent columns
- Layout felt rigid and broken
- Wasted vertical space

### Current Solution (CSS Columns Masonry)

```
┌─────┬─────┬─────┬─────┐
│  N  │  N  │  T  │  N  │
├─────┼─────┤  A  ├─────┤
│  N  │  N  │  L  │  N  │
├─────┼─────┤  L  ├─────┤
│  N  │  N  │     │  N  │  ← No gaps!
└─────┴─────┴─────┴─────┘
```

**Benefits:**
- Cards flow naturally without gaps
- Automatic height balancing
- Fluid, dynamic layout
- Similar to Pinterest/Are.na/Cosmos

## Implementation

### Container Layout

**Before (CSS Grid):**
```jsx
<div className="grid grid-cols-12 gap-6">
```

**After (CSS Columns):**
```jsx
<div className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6">
```

### Responsive Columns

```css
columns-1           /* Mobile: 1 column */
sm:columns-2        /* Tablet: 2 columns (640px+) */
lg:columns-3        /* Desktop: 3 columns (1024px+) */
xl:columns-4        /* Large: 4 columns (1280px+) */
```

### Card Wrapper

**FeedItem Component:**
```jsx
<div className="break-inside-avoid mb-6">
  <MediaCard {...item} />
</div>
```

**Key Classes:**
- `break-inside-avoid`: Prevents card from splitting across columns
- `mb-6`: Consistent 24px spacing between cards

### Removed Classes

**No longer needed:**
- ❌ `col-span-*` (grid column spanning)
- ❌ `row-span-*` (grid row spanning)
- ❌ Grid-based responsive classes

**Replaced with:**
- ✓ `break-inside-avoid` (masonry behavior)
- ✓ `mb-6` (vertical spacing)
- ✓ Column-based responsive layout

## How CSS Columns Work

### Column Layout Algorithm

1. Browser divides container into N columns
2. Content flows top-to-bottom in first column
3. When column fills, content continues in next column
4. Heights balance automatically

### Break Control

```css
break-inside-avoid  /* Don't split this element */
break-before-avoid  /* Don't break before this element */
break-after-avoid   /* Don't break after this element */
```

We use `break-inside-avoid` to keep each card intact.

### Gap Behavior

```css
gap-6  /* 24px gap between columns */
```

Combined with `mb-6` on cards for vertical spacing.

## Card Variants in Masonry

### Normal Cards
- Aspect ratio: 4:5
- Flows naturally in columns
- Standard height

### Featured Cards
- Aspect ratio: 16:9
- Wider but shorter
- Takes full column width

### Video Cards (Tall)
- Aspect ratio: 9:16
- Taller than normal cards
- No longer uses `row-span-2`
- Flows naturally without gaps

### Wide Cards
- Aspect ratio: 4:5
- Takes full column width
- Treated same as featured in masonry

## Responsive Behavior

### Mobile (<640px)
```
┌───────────┐
│     N     │
├───────────┤
│     T     │
│     A     │
│     L     │
│     L     │
├───────────┤
│     N     │
└───────────┘
```
- Single column
- All cards stack vertically
- Natural scrolling experience

### Tablet (640px - 1023px)
```
┌─────┬─────┐
│  N  │  N  │
├─────┼─────┤
│  T  │  N  │
│  A  ├─────┤
│  L  │  N  │
│  L  └─────┘
└─────┘
```
- 2 columns
- Cards distribute evenly
- Balanced heights

### Desktop (1024px - 1279px)
```
┌─────┬─────┬─────┐
│  N  │  N  │  T  │
├─────┼─────┤  A  │
│  N  │  N  │  L  │
├─────┼─────┤  L  │
│  N  │  N  │     │
└─────┴─────┴─────┘
```
- 3 columns
- Optimal for most screens
- Good content density

### Large Desktop (1280px+)
```
┌─────┬─────┬─────┬─────┐
│  N  │  N  │  T  │  N  │
├─────┼─────┤  A  ├─────┤
│  N  │  N  │  L  │  N  │
├─────┼─────┤  L  ├─────┤
│  N  │  N  │     │  N  │
└─────┴─────┴─────┴─────┘
```
- 4 columns
- Maximum content density
- Ideal for large displays

## Design System Compliance

### Maintained Elements

✓ True black background `#000000`
✓ Surface layers `bg-surface/50`
✓ Borders `border-white/10`
✓ IBM Plex Mono typography
✓ Subtle transitions (180-200ms)
✓ Card hover states
✓ Category colors
✓ Spacing scale (gap-6 = 24px)

### No Changes To

✓ MediaCard component
✓ VideoCard component
✓ Color palette
✓ Typography scale
✓ Interaction timing
✓ Border radius
✓ Padding values

## Performance

### Advantages

**CSS Columns:**
- Native browser layout algorithm
- GPU-accelerated
- No JavaScript calculations
- Efficient reflow on resize

**vs. JavaScript Masonry:**
- No external libraries needed
- No layout calculations in JS
- Faster initial render
- Better performance on mobile

### Browser Support

CSS Columns are well-supported:
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support

## Comparison with Other Layouts

### CSS Grid (Previous)
**Pros:**
- Precise control
- Explicit placement

**Cons:**
- Row-spanning creates gaps
- Fixed row heights
- Rigid layout

### CSS Columns (Current)
**Pros:**
- No vertical gaps
- Automatic balancing
- Fluid layout
- Simple implementation

**Cons:**
- Less control over exact placement
- Cards flow vertically first

### JavaScript Masonry (Alternative)
**Pros:**
- Precise control
- Horizontal-first flow

**Cons:**
- Requires library (Masonry.js, React-Masonry)
- JavaScript overhead
- More complex
- Performance cost

## Visual Examples

### Pinterest-Style Flow

The feed now behaves like Pinterest:
- Cards flow top-to-bottom in each column
- Heights balance automatically
- No wasted space
- Smooth scrolling experience

### Are.na-Style Discovery

Similar to Are.na blocks:
- Mixed content types
- Variable heights
- Clean, minimal aesthetic
- Focus on content

### Cosmos-Style Feed

Like Cosmos discovery:
- Dynamic layout
- Visual hierarchy
- Curated feel
- Modern design

## Customization

### Adjust Column Count

Change breakpoints:

```jsx
// More columns on desktop
<div className="columns-1 sm:columns-2 lg:columns-4 xl:columns-5 gap-6">

// Fewer columns (more spacious)
<div className="columns-1 sm:columns-2 lg:columns-2 xl:columns-3 gap-6">
```

### Adjust Gap Size

Change spacing between columns:

```jsx
// Tighter spacing
<div className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-4">

// Wider spacing
<div className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-8">
```

### Adjust Card Spacing

Change vertical spacing between cards:

```jsx
// Tighter
<div className="break-inside-avoid mb-4">

// Wider
<div className="break-inside-avoid mb-8">
```

## Known Limitations

### Column Flow Direction

Cards flow **vertically first**, then to next column:

```
Column 1: Card 1, Card 2, Card 3
Column 2: Card 4, Card 5, Card 6
Column 3: Card 7, Card 8, Card 9
```

This is different from horizontal-first flow:

```
Row 1: Card 1, Card 2, Card 3
Row 2: Card 4, Card 5, Card 6
Row 3: Card 7, Card 8, Card 9
```

**Impact:** Card order may feel different on wide screens.

**Solution:** If horizontal-first is required, use JavaScript masonry library.

### Column Balancing

Browser automatically balances column heights, which may cause:
- Cards to shift between columns on resize
- Slightly uneven column heights
- Different layouts on different screen sizes

**Impact:** Layout is fluid and dynamic.

**Solution:** This is expected behavior and creates a natural, organic feel.

## Migration Notes

### What Changed

**FeedItem.jsx:**
- Removed `variantClasses` object
- Removed grid column/row classes
- Added `break-inside-avoid mb-6` wrapper

**FeedPage.jsx:**
- Changed container from `grid grid-cols-12` to `columns-*`
- Removed grid-specific classes

**No changes to:**
- MediaCard component
- VideoCard component
- Card styling or interactions
- Image aspect ratios
- Hover states

### Testing Checklist

- [ ] Cards flow without vertical gaps
- [ ] Video cards display correctly
- [ ] Responsive behavior at all breakpoints
- [ ] Hover interactions still work
- [ ] No layout shifts on resize
- [ ] Performance is smooth
- [ ] Mobile experience is good

## Future Enhancements

### Horizontal-First Flow

If needed, implement JavaScript masonry:

```jsx
import Masonry from 'react-masonry-css';

<Masonry
  breakpointCols={{
    default: 4,
    1280: 4,
    1024: 3,
    640: 2,
    0: 1
  }}
  className="masonry-grid"
  columnClassName="masonry-column"
>
  {feedItems.map(item => <FeedItem key={item.id} item={item} />)}
</Masonry>
```

### Infinite Scroll

Add pagination with masonry:

```jsx
const [page, setPage] = useState(1);
const [items, setItems] = useState([]);

useEffect(() => {
  fetchItems(page).then(newItems => {
    setItems([...items, ...newItems]);
  });
}, [page]);
```

### Skeleton Loading

Show placeholders while loading:

```jsx
{isLoading && (
  <div className="break-inside-avoid mb-6">
    <div className="bg-surface/50 border border-white/10 rounded-lg h-64 animate-pulse" />
  </div>
)}
```

## Summary

The feed has been successfully converted from a CSS Grid with row-spanning to a masonry-style columns layout. This eliminates vertical gaps, creates a fluid discovery experience, and maintains the premium design system. The layout now behaves like Pinterest, Are.na, and Cosmos, with cards flowing naturally without wasted space.

**Key Changes:**
- Container: `grid grid-cols-12` → `columns-1 sm:columns-2 lg:columns-3 xl:columns-4`
- Cards: Grid classes → `break-inside-avoid mb-6`
- Removed: All `row-span-*` classes
- Result: No vertical gaps, fluid masonry layout
