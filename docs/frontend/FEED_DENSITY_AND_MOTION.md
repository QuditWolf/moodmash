# Feed Density Modes & Motion System Documentation

## Overview

The feed now supports three density modes (Visual, Grid, Compact), scroll reveal animations, and smooth scrolling throughout the application. All enhancements maintain the premium SaaS aesthetic.

---

## Part 1: Feed Density Modes

### Three Layout Options

**1. Visual Mode (Masonry)**
- Default mode
- Pinterest-style masonry layout
- Variable card heights
- Optimal for discovery

**2. Grid Mode (Structured)**
- Traditional grid layout
- Fixed column structure
- Predictable card placement
- Clean and organized

**3. Compact Mode (List)**
- Efficient list view
- Horizontal card layout
- Small thumbnails
- Maximum information density

---

## Visual Mode (Masonry)

### Layout Structure

```jsx
<div className="columns-1 sm:columns-2 lg:columns-3 xl:columns-4 gap-6">
  {feedItems.map((item) => (
    <RevealOnScroll key={item.id}>
      <FeedItem item={item} variant={item.variant} />
    </RevealOnScroll>
  ))}
</div>
```

### Characteristics

**Container:**
- `columns-1` (mobile)
- `sm:columns-2` (tablet)
- `lg:columns-3` (desktop)
- `xl:columns-4` (large desktop)
- `gap-6` (24px between columns)

**Cards:**
- Flow vertically in columns
- Variable heights
- No gaps or empty space
- Natural masonry behavior

**Best For:**
- Visual discovery
- Mixed content types
- Browsing and exploration
- Pinterest-style experience

---

## Grid Mode (Structured)

### Layout Structure

```jsx
<div className="grid grid-cols-12 gap-6">
  {feedItems.map((item) => (
    <div className="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3">
      <RevealOnScroll>
        <FeedItem item={item} variant={item.variant} />
      </RevealOnScroll>
    </div>
  ))}
</div>
```

### Characteristics

**Container:**
- `grid grid-cols-12` (12-column grid)
- `gap-6` (24px gaps)

**Cards:**
- `col-span-12` (mobile: 1 per row)
- `sm:col-span-6` (tablet: 2 per row)
- `lg:col-span-4` (desktop: 3 per row)
- `xl:col-span-3` (large: 4 per row)

**Best For:**
- Structured browsing
- Predictable layout
- Equal card heights
- Traditional grid feel

---

## Compact Mode (List)

### Layout Structure

```jsx
<div className="flex flex-col gap-4">
  {feedItems.map((item) => (
    <RevealOnScroll key={item.id}>
      <CompactCard {...item} />
    </RevealOnScroll>
  ))}
</div>
```

### CompactCard Component

**Structure:**
```
┌────────────────────────────────────┐
│ [Thumb] Title                      │
│         Source            [Category]│
└────────────────────────────────────┘
```

**Layout:**
```jsx
<div className="flex gap-4 p-4 border border-white/10 rounded-lg bg-surface/50">
  {/* Thumbnail */}
  <div className="flex-shrink-0">
    <img className="w-20 h-24 object-cover rounded-md" />
  </div>

  {/* Content */}
  <div className="flex-1 flex flex-col justify-between">
    <div>
      <h3 className="text-14">{title}</h3>
      <p className="text-11 text-muted-foreground">{source}</p>
    </div>
    <div className="category-badge">{category}</div>
  </div>
</div>
```

**Characteristics:**
- Horizontal card layout
- Small thumbnail (80x96px)
- Compact spacing
- Efficient information display

**Best For:**
- Quick scanning
- Maximum content per screen
- List-style browsing
- Efficient navigation

---

## Feed Mode Switcher

### Implementation

**Location:** Feed header (top-right)

**Icons:**
- Grid: `LayoutGrid` (structured grid)
- Visual: `Columns` (masonry)
- Compact: `List` (list view)

**Button Styling:**

**Inactive:**
```jsx
className="p-2 rounded-md border border-white/10 hover:bg-surface/50 transition-all duration-160"
```

**Active:**
```jsx
className="p-2 rounded-md border bg-surface border-white/20 transition-all duration-160"
```

**Code:**
```jsx
<div className="flex items-center gap-2">
  <button
    onClick={() => setFeedMode('grid')}
    className={`p-2 rounded-md border transition-all duration-160 ${
      feedMode === 'grid'
        ? 'bg-surface border-white/20'
        : 'border-white/10 hover:bg-surface/50'
    }`}
  >
    <LayoutGrid className="w-4 h-4 text-foreground" strokeWidth={1.5} />
  </button>
  {/* ... other buttons */}
</div>
```

### State Management

```jsx
const [feedMode, setFeedMode] = useState('visual');
```

**Default:** `'visual'` (masonry mode)

**Options:**
- `'visual'` - Masonry layout
- `'grid'` - Structured grid
- `'compact'` - List view

---

## Scroll Reveal Animation

### RevealOnScroll Component

**Purpose:** Animate cards as they enter viewport

**Implementation:**
```jsx
const RevealOnScroll = ({ children }) => {
  const ref = useRef();
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true);
        }
      },
      { threshold: 0.15 }
    );

    if (ref.current) observer.observe(ref.current);

    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`transition-all duration-[220ms] ease-out ${
        visible
          ? "opacity-100 translate-y-0"
          : "opacity-0 translate-y-3"
      }`}
    >
      {children}
    </div>
  );
};
```

### Animation Specifications

**Initial State:**
- `opacity-0` (invisible)
- `translate-y-3` (12px down)

**Final State:**
- `opacity-100` (fully visible)
- `translate-y-0` (original position)

**Transition:**
- Duration: `220ms`
- Easing: `ease-out`
- Trigger: When 15% of element is visible

### IntersectionObserver Settings

```javascript
{
  threshold: 0.15  // Trigger when 15% visible
}
```

**Why 15%:**
- Early enough to feel responsive
- Late enough to avoid premature triggers
- Smooth, natural reveal timing

### Usage

Wrap any feed item:
```jsx
<RevealOnScroll>
  <MediaCard {...item} />
</RevealOnScroll>
```

---

## Smooth Scrolling

### Implementation

**Global CSS:**
```css
html {
  scroll-behavior: smooth;
}
```

### Effect

- Smooth transitions when scrolling
- Applies to all scroll events
- Native browser implementation
- No JavaScript overhead

### Benefits

- Fluid navigation
- Premium feel
- Better UX
- Reduced jarring movements

---

## Design System Compliance

### Maintained Elements

✓ True black background `#000000`
✓ Surface layers `bg-surface/50`
✓ Borders `border-white/10`
✓ IBM Plex Mono typography
✓ Subtle transitions (160-220ms)
✓ Minimal aesthetic
✓ No shadows or glow
✓ Consistent spacing

### New Elements (Compliant)

✓ Mode switcher buttons (minimal)
✓ Scroll reveal (subtle, 220ms)
✓ Smooth scrolling (native)
✓ Compact card layout (clean)
✓ All within design system

---

## Responsive Behavior

### Visual Mode

**Mobile (<640px):**
- 1 column
- Full width cards
- Vertical stacking

**Tablet (640px - 1023px):**
- 2 columns
- Balanced layout
- Good content density

**Desktop (1024px - 1279px):**
- 3 columns
- Optimal viewing
- Rich content display

**Large (1280px+):**
- 4 columns
- Maximum density
- Wide screen optimization

### Grid Mode

**Mobile (<640px):**
- 1 card per row
- Full width
- Vertical scroll

**Tablet (640px - 1023px):**
- 2 cards per row
- Balanced grid
- Clean structure

**Desktop (1024px - 1279px):**
- 3 cards per row
- Standard grid
- Good spacing

**Large (1280px+):**
- 4 cards per row
- Dense grid
- Maximum content

### Compact Mode

**All Breakpoints:**
- Single column list
- Horizontal cards
- Consistent layout
- Efficient scrolling

---

## Performance Considerations

### IntersectionObserver

**Advantages:**
- Native browser API
- Efficient viewport detection
- No scroll event listeners
- Automatic cleanup

**Performance:**
- Minimal CPU usage
- No layout thrashing
- Smooth animations
- Battery efficient

### Smooth Scrolling

**Native Implementation:**
- Browser-optimized
- GPU-accelerated
- No JavaScript overhead
- Consistent across devices

### Animation Timing

**220ms Duration:**
- Fast enough to feel responsive
- Slow enough to be noticeable
- Smooth, not jarring
- Premium feel

---

## User Experience

### Mode Selection

**Visual Mode:**
- Best for discovery
- Engaging layout
- Variable content
- Exploration focus

**Grid Mode:**
- Best for browsing
- Predictable structure
- Equal emphasis
- Organization focus

**Compact Mode:**
- Best for scanning
- Maximum efficiency
- Quick navigation
- Information focus

### Animation Feel

**Scroll Reveal:**
- Cards "wake up" as you scroll
- Subtle, not distracting
- Adds life to the feed
- Premium, polished feel

**Smooth Scrolling:**
- Fluid navigation
- Reduced motion sickness
- Better focus tracking
- Professional experience

---

## Customization

### Adjust Reveal Threshold

```jsx
const observer = new IntersectionObserver(
  ([entry]) => {
    if (entry.isIntersecting) {
      setVisible(true);
    }
  },
  { threshold: 0.25 }  // Trigger at 25% visible
);
```

### Adjust Animation Duration

```jsx
className={`transition-all duration-[300ms] ease-out ${...}`}
```

### Adjust Animation Distance

```jsx
visible
  ? "opacity-100 translate-y-0"
  : "opacity-0 translate-y-6"  // 24px instead of 12px
```

### Change Default Mode

```jsx
const [feedMode, setFeedMode] = useState('grid');  // Start with grid
```

### Persist Mode Selection

```jsx
const [feedMode, setFeedMode] = useState(
  localStorage.getItem('feedMode') || 'visual'
);

useEffect(() => {
  localStorage.setItem('feedMode', feedMode);
}, [feedMode]);
```

---

## Accessibility

### Mode Switcher

**ARIA Labels:**
```jsx
<button aria-label="Grid mode">
  <LayoutGrid />
</button>
```

**Keyboard Navigation:**
- Tab to focus buttons
- Enter/Space to activate
- Clear visual focus states

**Visual Feedback:**
- Active state clearly indicated
- Hover states for feedback
- Consistent button sizing

### Scroll Reveal

**Respects Motion Preferences:**

Add to RevealOnScroll:
```jsx
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

return (
  <div
    ref={ref}
    className={prefersReducedMotion ? '' : `transition-all duration-[220ms] ease-out ${...}`}
  >
    {children}
  </div>
);
```

---

## Future Enhancements

### Save Mode Preference

```jsx
// Save to localStorage
useEffect(() => {
  localStorage.setItem('feedMode', feedMode);
}, [feedMode]);

// Load on mount
useEffect(() => {
  const saved = localStorage.getItem('feedMode');
  if (saved) setFeedMode(saved);
}, []);
```

### Keyboard Shortcuts

```jsx
useEffect(() => {
  const handleKeyPress = (e) => {
    if (e.key === '1') setFeedMode('grid');
    if (e.key === '2') setFeedMode('visual');
    if (e.key === '3') setFeedMode('compact');
  };

  window.addEventListener('keypress', handleKeyPress);
  return () => window.removeEventListener('keypress', handleKeyPress);
}, []);
```

### Stagger Animation

```jsx
<RevealOnScroll delay={index * 50}>
  <MediaCard />
</RevealOnScroll>
```

### Fade-Out on Scroll Up

```jsx
const [scrollDirection, setScrollDirection] = useState('down');

useEffect(() => {
  let lastScroll = 0;
  
  const handleScroll = () => {
    const currentScroll = window.scrollY;
    setScrollDirection(currentScroll > lastScroll ? 'down' : 'up');
    lastScroll = currentScroll;
  };

  window.addEventListener('scroll', handleScroll);
  return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

---

## Testing Checklist

- [ ] Visual mode displays masonry layout
- [ ] Grid mode displays structured grid
- [ ] Compact mode displays list view
- [ ] Mode switcher buttons work
- [ ] Active mode is visually indicated
- [ ] Cards animate on scroll
- [ ] Animation is smooth (220ms)
- [ ] Smooth scrolling works globally
- [ ] Responsive at all breakpoints
- [ ] Performance is good (no lag)
- [ ] Keyboard navigation works
- [ ] ARIA labels are present

---

## Summary

The feed now supports three density modes (Visual, Grid, Compact) with a minimal mode switcher in the header. Cards animate subtly as they enter the viewport using IntersectionObserver, and smooth scrolling is enabled globally. All enhancements maintain the premium SaaS aesthetic with subtle transitions, minimal styling, and no heavy animations.

**Key Features:**
- 3 feed modes (Visual, Grid, Compact)
- Mode switcher with Lucide icons
- Scroll reveal animation (220ms, 12px translate)
- Smooth scrolling (native CSS)
- IntersectionObserver (15% threshold)
- Responsive at all breakpoints
- Design system compliant
- Accessible and performant
