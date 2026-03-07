# Premium SaaS Feed Application

A modern, dark-themed content discovery feed built with React, Tailwind CSS, and premium design principles inspired by Notion, Linear, and Supabase.

## Design Philosophy

This application follows a **premium SaaS aesthetic** with these core principles:

- **True Black Background**: Pure `#000000` with subtle surface variations
- **Monospace Typography**: IBM Plex Mono for technical, developer-first feel
- **Subtle Interactions**: 180-200ms transitions with `cubic-bezier(0.16, 1, 0.3, 1)` easing
- **High Density**: Compact spacing, maximum information per viewport
- **Structural Grid**: 12-column responsive grid system with proper alignment
- **Minimal Styling**: No heavy shadows, no gradients, no glow effects

---

## Visual Design System

### Color Palette

```css
/* Background */
--background: #000000 (pure black)
--surface: hsl(0 0% 4%)
--surface-elevated: hsl(0 0% 7%)

/* Text */
--foreground: hsl(0 0% 98%) (primary text)
--muted-foreground: hsl(0 0% 55%) (secondary text)
--subtle-foreground: hsl(0 0% 40%) (tertiary text)

/* Borders */
--border: hsl(0 0% 10%)
--border-hover: hsl(0 0% 15%)

/* Category Colors (Muted) */
Music: hsl(270 50% 50%)
Book: hsl(220 60% 45%)
Movie: hsl(0 50% 50%)
Artwork: hsl(160 50% 45%)
Podcast: hsl(40 60% 50%)
Article: hsl(0 0% 40%)
```

### Typography Scale

```css
.text-11 { font-size: 11px; line-height: 1.4; }
.text-12 { font-size: 12px; line-height: 1.4; }
.text-13 { font-size: 13px; line-height: 1.4; }
.text-14 { font-size: 14px; line-height: 1.4; }
.text-16 { font-size: 16px; line-height: 1.4; }
.text-18 { font-size: 18px; line-height: 1.3; }
.text-28 { font-size: 28px; line-height: 1.2; }
```

**Font**: IBM Plex Mono (weights: 300, 400, 500, 600)
- Letter spacing: `-0.011em` (body), `-0.02em` (headings)
- Font features: `"liga" 0, "calt" 0` (disable ligatures)

### Spacing Scale

Use consistent spacing values:
- `4px` / `8px` / `12px` / `16px` / `24px` / `32px`
- Tailwind: `1` / `2` / `3` / `4` / `6` / `8`

---

## Layout System

### Grid Structure

**12-Column Responsive Grid**
```jsx
<div className="grid grid-cols-12 gap-6">
  {/* Cards use col-span */}
</div>
```

**Responsive Column Spans:**
- Desktop (1280px+): `col-span-3` (4 cards per row)
- Laptop (1024px): `col-span-4` (3 cards per row)
- Tablet (768px): `col-span-6` (2 cards per row)
- Mobile (<768px): `col-span-12` (1 card per row)

**Container:**
- Max width: `max-w-7xl`
- Horizontal padding: `px-6`
- Centered: `mx-auto`

---

## Component Patterns

### Card Component

**Structure:**
```
┌─────────────────────┐
│                     │
│      Image          │ 4:5 aspect ratio
│                     │
├─────────────────────┤
│ Title    [Category] │ Title + Badge
│ Source              │ Link
└─────────────────────┘
```

**Styling:**
- Background: `bg-surface/50`
- Border: `border border-white/10`
- Rounded: `rounded-lg`
- Padding: `p-6`
- Vertical spacing: `space-y-3`

**Hover States:**
- Card: `hover:bg-surface/80 hover:-translate-y-0.5`
- Image: `group-hover:scale-[1.02]`
- Transition: `180ms ease-out`

### Category Badge

**Styling:**
- Padding: `px-2.5 py-1`
- Font: `text-11 uppercase tracking-wide`
- Border: `1px solid` with muted accent color
- Background: 10% opacity of accent color
- Rounded: `rounded`

**Colors by Category:**
```jsx
Music: purple (270° 50% 50%)
Book: blue (220° 60% 45%)
Movie: red (0° 50% 50%)
Artwork: emerald (160° 50% 45%)
Podcast: amber (40° 60% 50%)
Article: gray (0° 0% 40%)
```

### Header Component

**Structure:**
- Sticky: `sticky top-0 z-10`
- Height: `h-16`
- Border: `border-b border-white/10`
- Background: `bg-background/95 backdrop-blur-sm`

---

## Interaction Design

### Transitions

**Standard Easing:**
```css
cubic-bezier(0.16, 1, 0.3, 1)
```

**Timing:**
- Quick interactions: `160ms`
- Standard: `180ms`
- Image transforms: `200ms`

### Hover Effects

**Cards:**
- Subtle lift: `translateY(-2px)` or `-translate-y-0.5`
- Background shift: 2% lighter
- No shadows, no glow

**Images:**
- Scale: `1.02` (very subtle)
- Smooth transform

**Links:**
- Color shift: `text-muted-foreground` → `text-foreground`
- Duration: `160ms`

### Active States

**Press:**
- Scale: `0.99`
- Immediate feedback

---

## Content Guidelines

### Feed Items

**Categories:**
- Music
- Book
- Movie
- Artwork
- Podcast
- Article

**Image Requirements:**
- Aspect ratio: 4:5
- Quality: High resolution (800px+ width)
- Format: JPG/PNG
- Loading: Lazy load with `loading="lazy"`

**Text Content:**
- Title: 2 lines max (`line-clamp-2`)
- Source: Single line, no truncation
- No metadata (views/time removed for cleaner look)

---

## Technical Stack

### Core Technologies
- **React 18**: Component framework
- **Vite**: Build tool and dev server
- **Tailwind CSS 3.4.1**: Utility-first styling
- **Lucide React**: Icon library

### UI Components
- Custom card components
- shadcn/ui base components (Avatar, Button, Separator)

### Styling Approach
- Tailwind utility classes
- CSS custom properties for theming
- No CSS-in-JS
- No styled-components

---

## Development Guidelines

### Component Structure

**File Organization:**
```
src/
├── components/
│   ├── MediaCard.jsx       # Feed card component
│   ├── FeedPage.jsx        # Main feed layout
│   └── ui/                 # Base UI components
├── contexts/               # React contexts
├── pages/                  # Page components
└── styles/                 # Global styles
```

### Naming Conventions

**Components:**
- PascalCase: `MediaCard`, `FeedPage`
- Descriptive names: `MediaCard` not `Card`

**CSS Classes:**
- Utility-first: Use Tailwind classes
- Custom utilities in `@layer utilities`
- Semantic naming for custom classes

### Code Style

**React:**
```jsx
// Functional components with arrow functions
const MediaCard = ({ title, category, image, source }) => {
  return (
    <div className="...">
      {/* Content */}
    </div>
  );
};
```

**Tailwind:**
```jsx
// Group related utilities
className="flex items-center gap-2"

// Responsive modifiers
className="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3"

// State modifiers
className="hover:bg-surface/80 transition-all duration-180"
```

---

## Building New Features

### Adding New Card Types

1. Define category color in `categoryColors` object
2. Add to `categories` array in feed generator
3. Provide image collection and titles
4. Maintain 4:5 aspect ratio for images

### Creating New Pages

**Follow this structure:**
```jsx
const NewPage = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-10 border-b border-white/10">
        {/* Header content */}
      </header>

      {/* Content */}
      <div className="py-6 px-6">
        <div className="max-w-7xl mx-auto">
          {/* Page content */}
        </div>
      </div>
    </div>
  );
};
```

### Adding Interactions

**Hover states:**
```jsx
className="transition-all duration-180 ease-out hover:bg-surface/80"
```

**Image hover:**
```jsx
className="group"  // Parent
className="group-hover:scale-[1.02]"  // Image
```

**Link hover:**
```jsx
className="hover:text-foreground transition-colors duration-160"
```

---

## Design Principles for New UI

### Do's ✓

- Use pure black `#000000` background
- Apply subtle borders `border-white/10`
- Use monospace typography (IBM Plex Mono)
- Keep transitions between 160-200ms
- Use `cubic-bezier(0.16, 1, 0.3, 1)` easing
- Maintain high information density
- Apply subtle hover states (2% lighter, 2px lift)
- Use muted accent colors (50% saturation max)
- Keep rounded corners subtle (`rounded-lg` max)
- Align to 12-column grid system

### Don'ts ✗

- No heavy shadows or elevation
- No gradients (except subtle surface variations)
- No glow effects
- No neon colors
- No bold/heavy font weights (500 max)
- No large gaps (6 = 24px max)
- No floating card feeling
- No dramatic animations
- No border radius on grid layouts
- No approximations (use exact spacing scale)

---

## Accessibility

### Color Contrast
- Text on black: `hsl(0 0% 98%)` meets WCAG AA
- Muted text: `hsl(0 0% 55%)` for secondary content
- Borders: `white/10` visible but subtle

### Interactive Elements
- All clickable elements have hover states
- Focus states inherit from Tailwind defaults
- Sufficient touch targets (44px minimum)

### Images
- All images have `alt` attributes
- Lazy loading for performance
- Fallback backgrounds for missing images

---

## Performance Optimization

### Image Loading
```jsx
loading="lazy"  // Native lazy loading
```

### Transitions
- Use `transform` and `opacity` (GPU accelerated)
- Avoid animating `width`, `height`, `margin`

### Grid Rendering
- Fixed column counts reduce layout shifts
- Gap-based spacing (no margin calculations)

---

## Future Enhancements

### Potential Features
- Infinite scroll / pagination
- Filter by category
- Search functionality
- User preferences (saved items)
- Dark/light mode toggle (currently dark only)
- Keyboard navigation
- Grid/list view toggle

### Maintaining Design Consistency
When adding features, always:
1. Reference this README for design tokens
2. Use existing component patterns
3. Match interaction timing (180ms standard)
4. Test responsive behavior at all breakpoints
5. Maintain monospace typography
6. Keep true black background
7. Use subtle, premium interactions

---

## Quick Reference

### Common Patterns

**Card Grid:**
```jsx
<div className="grid grid-cols-12 gap-6">
  <div className="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3">
    <Card />
  </div>
</div>
```

**Premium Button:**
```jsx
<button className="hover:bg-surface/50 transition-all duration-160">
  Click me
</button>
```

**Category Badge:**
```jsx
<div className="px-2.5 py-1 rounded text-11 uppercase tracking-wide"
     style={{ backgroundColor: '...', color: '...', border: '...' }}>
  Category
</div>
```

**Page Container:**
```jsx
<div className="py-6 px-6">
  <div className="max-w-7xl mx-auto">
    {/* Content */}
  </div>
</div>
```

---

## Support

For questions about design decisions or implementation details, refer to:
- `DESIGN_SYSTEM.md` - Complete design token reference
- `PREMIUM_DESIGN_SYSTEM.md` - Premium interaction patterns
- `STRUCTURAL_SYSTEM.md` - Grid and layout system
- `COMPONENTS.md` - Component API documentation

---

**Built with precision. Designed for developers.**
