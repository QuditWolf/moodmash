# True Structural Grid System - Mathematical Precision

## Philosophy
The grid IS the structure. Card edges ARE the grid lines. No decorative overlays. No approximations. Mathematical precision.

---

## STRUCTURAL GRID IMPLEMENTATION

### True 12-Column CSS Grid
```jsx
<div className="grid grid-cols-12 gap-4 max-w-7xl mx-auto px-6">
  {/* Cards */}
</div>
```

**Specs:**
- `grid-cols-12` - 12 equal columns
- `gap-4` - 16px gutter (both x and y)
- `max-w-7xl` - 1280px max width
- `mx-auto` - Centered
- `px-6` - 24px horizontal padding

### Column Span Logic
```jsx
<div className="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3">
  <MediaCard />
</div>
```

**Breakpoints:**
```
Mobile (<640px):   col-span-12 (1 column)  - 100%
Tablet (640px):    col-span-6  (2 columns) - 50%
Laptop (1024px):   col-span-4  (3 columns) - 33.33%
Desktop (1280px+): col-span-3  (4 columns) - 25%
```

### Grid Math
```
Container width: 1280px (max-w-7xl)
Padding: 24px × 2 = 48px
Available: 1280px - 48px = 1232px
Gap: 16px × 11 = 176px
Column width: (1232px - 176px) / 12 = 88px

Card width (col-span-3):
= 3 × 88px + 2 × 16px
= 264px + 32px
= 296px
```

### Alignment Rules
- **Vertical grid lines** = Card left and right edges
- **Horizontal grid lines** = Card top and bottom edges
- **No extra margin** inside grid cells
- **No padding** outside grid logic
- **Perfect snap** to column boundaries

---

## CARD STRUCTURE (High Density)

### Layout
```jsx
<Card className="p-0">
  <div className="aspect-[4/5]">
    <img />
  </div>
  <div className="p-2.5 space-y-1">
    <div className="flex justify-between">
      <h3 className="text-16 line-clamp-2" />
      <div className="category-label" />
    </div>
    <a className="text-13" />
    <div className="text-12" />
  </div>
</Card>
```

### Spacing
```
Card padding:     0 (no padding)
Image:            aspect-[4/5] (no margin)
Content padding:  10px (p-2.5)
Content spacing:  4px (space-y-1)
```

### Vertical Rhythm
```
Image bottom → Content top:  0px
Title → Source:              4px
Source → Metadata:           4px
```

---

## CATEGORY LABEL POSITION

### Correct Placement
```
[ Image ]
[ Title ........................ CATEGORY ]
[ Source ]
[ Metadata ]
```

**Implementation:**
```jsx
<div className="flex items-start justify-between gap-2">
  <h3 className="flex-1 line-clamp-2">Title</h3>
  <div className="flex-shrink-0 category-label">MUSIC</div>
</div>
```

**Specs:**
- Position: In content area, aligned with title
- Size: px-1.5 py-0.5 (6px/2px)
- Font: 11px uppercase
- Tracking: wide
- Colors: Muted per category

**NOT on image. In text row.**

---

## RESPONSIVE BEHAVIOR

### Breakpoint Logic
```
1440+: 4 cards (col-span-3) = 296px each
1280:  4 cards (col-span-3) = 296px each
1024:  3 cards (col-span-4) = 400px each
640:   2 cards (col-span-6) = 616px each
<640:  1 card  (col-span-12) = 100%
```

### Grid Recalculation
At each breakpoint, grid recalculates:
```
Available width = Container - Padding
Column width = (Available - Gaps) / 12
Card width = Columns × Column width + Gaps
```

**No rounding drift. Exact math.**

---

## UNIFIED FEED

### Single Continuous Stream
```jsx
const feedItems = generateUnifiedFeed(24);

<FeedSection items={feedItems} />
```

**No sections. No categories. One grid.**

### Mixed Content
```
Music → Book → Movie → Artwork → Podcast → Article
```

**Natural mixing in one intelligent stream.**

---

## SPACING SCALE

### Consistent Values
```
0px  - No spacing
4px  - gap-1, space-y-1
8px  - gap-2, space-y-2
10px - p-2.5
16px - gap-4, p-4
24px - gap-6, px-6
```

### Component Spacing
```
Grid gap:       16px (gap-4)
Card padding:   0px (p-0)
Content padding: 10px (p-2.5)
Content spacing: 4px (space-y-1)
Container padding: 24px (px-6)
Section padding: 24px (py-6)
```

---

## TYPOGRAPHY

### Scale
```
Page title:     28px (text-28)
Card title:     16px (text-16)
Source link:    13px (text-13)
Metadata:       12px (text-12)
Category label: 11px (text-11)
```

### Line Heights
```
28px: 1.2
18px: 1.3
16px: 1.4
13px: 1.4
12px: 1.4
11px: 1.4
```

**Tight but readable.**

---

## CATEGORY COLORS

### Muted Professional Palette
```css
Music:    hsl(270 50% 50%)  /* Muted purple */
Book:     hsl(220 60% 45%)  /* Deep blue */
Movie:    hsl(0 50% 50%)    /* Soft red */
Artwork:  hsl(160 50% 45%)  /* Emerald */
Podcast:  hsl(40 60% 50%)   /* Amber */
Article:  hsl(0 0% 40%)     /* Gray */
```

**Not neon. Muted. Professional.**

---

## INTERACTIONS

### Card Hover
```css
transform: translateY(-2px);
background: hsl(var(--surface-elevated));
border-color: hsl(var(--border-hover));
transition: 180ms cubic-bezier(0.16, 1, 0.3, 1);
```

### Card Press
```css
transform: scale(0.99);
```

### Image Hover
```css
transform: scale(1.01);
transition: 200ms cubic-bezier(0.16, 1, 0.3, 1);
```

### Link Hover
```css
.link-hover::after {
  width: 0 → 100%;
  transition: 200ms cubic-bezier(0.16, 1, 0.3, 1);
}
```

### Category Hover
```css
background-color: subtle tint shift;
transition: 160ms cubic-bezier(0.16, 1, 0.3, 1);
```

---

## GRID ALIGNMENT VERIFICATION

### Checklist
- [x] Card left edge = Grid column line
- [x] Card right edge = Grid column line
- [x] Card top edge = Grid row line
- [x] Card bottom edge = Grid row line
- [x] No extra margin in grid cells
- [x] No padding outside grid
- [x] Gap-4 (16px) consistent
- [x] Responsive spans maintain alignment
- [x] No rounding drift

### Mathematical Precision
```
Column width = (Container - Padding - Gaps) / 12
Card width = Columns × Column + (Columns - 1) × Gap
```

**Exact. Not approximate.**

---

## IMPLEMENTATION SUMMARY

### Tailwind Classes
```jsx
// Container
className="grid grid-cols-12 gap-4 max-w-7xl mx-auto px-6"

// Card wrapper
className="col-span-12 sm:col-span-6 lg:col-span-4 xl:col-span-3"

// Card
className="p-0 bg-surface/80"

// Image
className="aspect-[4/5]"

// Content
className="p-2.5 space-y-1"

// Title row
className="flex items-start justify-between gap-2"

// Title
className="text-16 line-clamp-2 flex-1"

// Category
className="flex-shrink-0 px-1.5 py-0.5 text-11"
```

### No Decorative Grid
- No background overlay
- No pseudo-element lines
- No visual approximation
- Grid IS the structure

---

## QUALITY STANDARDS

### Structural
- [x] True 12-column CSS Grid
- [x] Card edges ARE grid lines
- [x] No decorative overlay
- [x] Mathematical precision
- [x] Responsive spans
- [x] Consistent 16px gap
- [x] No rounding drift

### Density
- [x] Tight spacing (p-2.5, space-y-1)
- [x] No wasted space
- [x] Optimized vertical rhythm
- [x] Maximum information per viewport
- [x] Readable but compact

### Category Labels
- [x] In content area (not on image)
- [x] Aligned with title row
- [x] Muted professional colors
- [x] Compact rectangular
- [x] 11px uppercase

### Unified Feed
- [x] Single continuous stream
- [x] Mixed content types
- [x] No section breaks
- [x] One grid system

---

## TARGET AESTHETIC

**Feels like:**
- High-density discovery feed
- System-driven
- Grid-intelligent
- Mathematically precise
- Series B SaaS
- Built to scale

**Does NOT feel:**
- Decorative
- Approximate
- Visual overlay
- Template
- Cosmetic

---

This is structural.
The grid IS the layout.
Cards ARE grid units.
Everything snaps.
Mathematical precision.
No approximations.
