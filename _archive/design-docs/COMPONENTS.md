# Component Reference

## Component Hierarchy

```
App
├── Sidebar
└── FeedPage
    └── FeedSection (multiple)
        ├── SectionHeader
        └── MediaCard (multiple)
```

## Sidebar

**Location**: `src/components/Sidebar.jsx`

### Props
None (static navigation)

### Features
- Fixed position (left side)
- App logo at top
- Navigation items with icons
- Active state styling
- Hover effects
- Settings button at bottom

### Structure
```jsx
<aside>
  <div> {/* Logo */}
  <nav> {/* Navigation items */}
  <div> {/* Footer (Settings) */}
</aside>
```

### Styling
- Width: 256px (16rem)
- Border right
- Full height
- Background: card color

### Customization
```javascript
const navItems = [
  { icon: IconComponent, label: 'Label', active: boolean },
];
```

---

## FeedPage

**Location**: `src/components/FeedPage.jsx`

### Props
None (generates own data)

### Features
- Sticky header
- Multiple feed sections
- Mock data generation
- Responsive layout

### Structure
```jsx
<div>
  <header> {/* Sticky page header */}
  <div> {/* Feed sections container */}
    <FeedSection /> {/* Multiple sections */}
  </div>
</div>
```

### Mock Data Generator
```javascript
generateMockItems(category, count)
// Returns array of items with:
// - id
// - height (small/medium/large/xlarge)
// - tag
// - title
// - metadata
```

### Sections
- Music (12 items)
- Movies (10 items)
- Art (14 items)
- Fashion (8 items)
- Books (9 items)

---

## FeedSection

**Location**: `src/components/FeedSection.jsx`

### Props
```typescript
{
  title: string;      // Section title
  items: Array<{      // Array of items
    id: string;
    height: string;
    tag: string;
    title: string;
    metadata: boolean;
  }>;
}
```

### Features
- Section header with count
- Masonry grid layout
- Responsive columns

### Structure
```jsx
<section>
  <SectionHeader />
  <div className="masonry-grid">
    <MediaCard /> {/* Multiple cards */}
  </div>
</section>
```

### Usage
```jsx
<FeedSection 
  title="Music" 
  items={musicItems}
/>
```

---

## SectionHeader

**Location**: `src/components/SectionHeader.jsx`

### Props
```typescript
{
  title: string;    // Section title
  count?: number;   // Optional item count
}
```

### Features
- Display font for title
- Count badge
- "View all" button
- Flexbox layout

### Structure
```jsx
<div>
  <div> {/* Title + count */}
    <h2>{title}</h2>
    <span>{count}</span>
  </div>
  <button>View all</button>
</div>
```

### Usage
```jsx
<SectionHeader title="Music" count={12} />
```

---

## MediaCard

**Location**: `src/components/MediaCard.jsx`

### Props
```typescript
{
  height?: 'small' | 'medium' | 'large' | 'xlarge';  // Default: 'medium'
  title: string;
  tag: string;
  metadata?: boolean;
}
```

### Features
- Variable heights for masonry effect
- Gradient placeholder background
- Shimmer loading animation
- Skeleton text placeholders
- Tag badge
- Hover effects
- Rounded corners
- Soft shadow

### Height Variants
```javascript
small:  'h-48'  // 192px
medium: 'h-64'  // 256px
large:  'h-80'  // 320px
xlarge: 'h-96'  // 384px
```

### Structure
```jsx
<div className="masonry-grid-item">
  <div> {/* Card container */}
    <div> {/* Placeholder image area */}
      <div /> {/* Shimmer effect */}
      <div /> {/* Hover overlay */}
    </div>
    <div> {/* Card content */}
      <span>{tag}</span>
      <div> {/* Title placeholders */}
      {metadata && <div />} {/* Metadata placeholders */}
    </div>
  </div>
</div>
```

### Usage
```jsx
<MediaCard 
  height="large"
  title="Jazz Collection"
  tag="Jazz"
  metadata={true}
/>
```

### Styling Classes
- `masonry-grid-item`: Prevents column breaks
- `group`: Enables group-hover effects
- Gradient: `from-muted to-muted/50`
- Shadow: `shadow-sm` → `hover:shadow-md`
- Border: `border-border` → `hover:border-foreground/20`

---

## Masonry Grid

**Location**: `src/index.css`

### CSS Classes
```css
.masonry-grid {
  column-count: 4;
  column-gap: 1.5rem;
}

.masonry-grid-item {
  break-inside: avoid;
  margin-bottom: 1.5rem;
}
```

### Responsive Breakpoints
- **Desktop (>1280px)**: 4 columns
- **Laptop (1024-1280px)**: 3 columns
- **Tablet (640-1024px)**: 2 columns
- **Mobile (<640px)**: 1 column

### How It Works
1. Parent has `column-count`
2. Children have `break-inside: avoid`
3. Items flow into columns automatically
4. Different heights create masonry effect

---

## Animations

### Shimmer Effect
```css
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.animate-shimmer {
  animation: shimmer 2s infinite;
}
```

### Pulse Effect
Built-in Tailwind: `animate-pulse`

### Hover Transitions
```css
transition-all duration-200
transition-colors duration-150
```

---

## Color System

### Semantic Tokens
- `background`: Page background
- `foreground`: Primary text
- `card`: Card background
- `muted`: Subtle backgrounds
- `muted-foreground`: Secondary text
- `border`: Border color
- `accent`: Hover backgrounds
- `secondary`: Active states

### Usage
```jsx
className="bg-background text-foreground"
className="bg-card border-border"
className="text-muted-foreground"
```

### Dark Mode
All colors automatically adapt when `dark` class is on `<html>`

---

## Typography

### Font Families
- **Display**: `font-display` (Instrument Serif)
- **Body**: `font-sans` (Inter)

### Usage
```jsx
<h1 className="font-display text-3xl">Title</h1>
<p className="font-sans text-sm">Body text</p>
```

### Font Sizes
- `text-xs`: 0.75rem
- `text-sm`: 0.875rem
- `text-base`: 1rem
- `text-lg`: 1.125rem
- `text-xl`: 1.25rem
- `text-2xl`: 1.5rem
- `text-3xl`: 1.875rem

---

## Spacing

### Padding/Margin Scale
- `p-1`: 0.25rem (4px)
- `p-2`: 0.5rem (8px)
- `p-3`: 0.75rem (12px)
- `p-4`: 1rem (16px)
- `p-6`: 1.5rem (24px)
- `p-8`: 2rem (32px)

### Gap
- `gap-2`: 0.5rem
- `gap-3`: 0.75rem
- `gap-4`: 1rem

---

## Responsive Utilities

### Breakpoints
- `sm:`: 640px
- `md:`: 768px
- `lg:`: 1024px
- `xl:`: 1280px
- `2xl:`: 1536px

### Usage
```jsx
className="grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4"
```

---

## Best Practices

### Component Design
1. Keep components small and focused
2. Use props for customization
3. Use Tailwind classes directly
4. Avoid inline styles
5. Use semantic HTML

### Styling
1. Use design tokens (colors, spacing)
2. Maintain consistent spacing
3. Use hover states for interactivity
4. Support dark mode
5. Keep animations subtle

### Performance
1. Use CSS for animations
2. Avoid unnecessary re-renders
3. Use semantic HTML for accessibility
4. Optimize images (when added)
5. Lazy load content (when needed)

---

## Extending Components

### Add New Card Type
```jsx
// In MediaCard.jsx
const CardVariant = ({ variant }) => {
  if (variant === 'featured') {
    return <div className="col-span-2">...</div>;
  }
  return <div>...</div>;
};
```

### Add New Section Type
```jsx
// In FeedSection.jsx
const FeedSection = ({ title, items, layout = 'masonry' }) => {
  if (layout === 'grid') {
    return <div className="grid grid-cols-4">...</div>;
  }
  return <div className="masonry-grid">...</div>;
};
```

### Add Interactions
```jsx
// In MediaCard.jsx
const MediaCard = ({ onClick, ...props }) => {
  return (
    <div onClick={onClick} className="cursor-pointer">
      ...
    </div>
  );
};
```
