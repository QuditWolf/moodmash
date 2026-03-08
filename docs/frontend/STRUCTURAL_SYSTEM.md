# Structural Design System - Engineered, Not Styled

## Philosophy
This is a grid-based, system-driven interface. Every element snaps to a functional 12-column grid. Typography follows a consistent scale. Interactions are premium and intentional. This is engineered, not styled.

---

## FUNCTIONAL GRID SYSTEM

### 12-Column Grid Implementation
```css
.grid-container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
}
```

**Critical:**
- Grid is FUNCTIONAL, not decorative
- Visual grid lines align EXACTLY with layout columns
- Cards snap to column spans (col-span-3, col-span-4, col-span-6, col-span-12)
- Gutter spacing: 24px (consistent across breakpoints)
- Max width: 1280px (max-w-7xl)

### Visual Grid Overlay
```css
.grid-overlay::before {
  background-image: repeating-linear-gradient(
    to right,
    transparent,
    transparent calc((100% - (11 * 24px)) / 12),
    hsl(var(--grid-line)) calc((100% - (11 * 24px)) / 12),
    ...
  );
}
```

**Purpose:**
- Shows actual column structure
- Aligns with layout math
- Resolution-aware
- Helps verify alignment

### Column Span System
```jsx
<MediaCard colSpan={3} />  // 3 columns (25%)
<MediaCard colSpan={4} />  // 4 columns (33%)
<MediaCard colSpan={6} />  // 6 columns (50%)
<MediaCard colSpan={12} /> // 12 columns (100%)
```

**Responsive Logic:**
```
Desktop (1440+):  col-span-3 (4 cards per row)
Laptop (1280):    col-span-3 (4 cards per row)
Tablet (1024):    col-span-4 (3 cards per row)
Mobile (768):     col-span-6 (2 cards per row)
Mobile (640):     col-span-12 (1 card per row)
```

---

## TYPOGRAPHY SCALE

### Consistent Scale
```
12px - text-12 - Metadata, small labels
14px - text-14 - Body text, buttons, nav
16px - text-16 - Card titles
18px - text-18 - Section titles
24px - text-24 - Page titles
32px - text-32 - Hero titles (unused)
```

### Implementation
```css
.text-12 { font-size: 12px; line-height: 1.5; }
.text-14 { font-size: 14px; line-height: 1.5; }
.text-16 { font-size: 16px; line-height: 1.5; }
.text-18 { font-size: 18px; line-height: 1.4; }
.text-24 { font-size: 24px; line-height: 1.3; }
.text-32 { font-size: 32px; line-height: 1.2; }
```

### Usage
```jsx
<h1 className="text-24">Page Title</h1>
<h2 className="text-18">Section Title</h2>
<h3 className="text-16">Card Title</h3>
<p className="text-14">Body text</p>
<span className="text-12">Metadata</span>
```

### Hierarchy Rules
- Use size + spacing for hierarchy
- Not color alone
- Maintain mono font
- Tight tracking for headings (-0.02em)
- Normal tracking for body (-0.011em)

---

## PREMIUM HOVER INTERACTIONS

### Card Hover
```css
.card-hover {
  transition: all 180ms cubic-bezier(0.16, 1, 0.3, 1);
}

.card-hover:hover {
  transform: translateY(-2px);
  background: hsl(var(--surface-elevated));
  border-color: hsl(var(--border-hover));
}
```

**Effect:**
- Subtle elevation (-2px translateY)
- Background shift (surface → surface-elevated)
- Border opacity increase
- 180ms cubic-bezier(0.16, 1, 0.3, 1)

### Image Hover
```css
.image-hover {
  transition: transform 200ms cubic-bezier(0.16, 1, 0.3, 1);
}

.image-hover:hover {
  transform: scale(1.015);
}
```

**Effect:**
- Very subtle scale (1.5% max)
- 200ms premium easing
- No glow, no bounce

### Sidebar Item Hover
```jsx
className="hover:bg-surface/50 hover:text-foreground transition-all duration-180 ease-premium"
```

**Effect:**
- Subtle background tint (surface/50)
- Text color shift (muted → foreground)
- Icon opacity shift
- 180ms premium easing

### Button Hover
```jsx
className="hover:bg-surface-elevated transition-all duration-180 ease-premium"
```

**Effect:**
- Background shift
- No scale, no glow
- Smooth transition

---

## SPACING SYSTEM

### Consistent Scale (4px base)
```
4px  - gap-1    - Tight
8px  - gap-2    - Default
12px - gap-3    - Medium
16px - gap-4    - Large
24px - gap-6    - Section
32px - gap-8    - Major
48px - gap-12   - Extra
64px - gap-16   - Breaks
```

### Component Padding
```
Cards:     p-4 (16px)
Buttons:   px-4 py-2 (16px/8px)
Sidebar:   px-3 (12px)
Header:    px-6 (24px)
Container: px-6 (24px)
Sections:  mb-24 (96px)
```

---

## RESPONSIVE BREAKPOINTS

### Defined Breakpoints
```
1440+ - Desktop XL
1280  - Desktop
1024  - Laptop
768   - Tablet
640   - Mobile
```

### Grid Behavior
```jsx
// Desktop (1440+, 1280)
<MediaCard colSpan={3} /> // 4 per row

// Laptop (1024)
<MediaCard colSpan={4} /> // 3 per row

// Tablet (768)
<MediaCard colSpan={6} /> // 2 per row

// Mobile (640)
<MediaCard colSpan={12} /> // 1 per row
```

### Implementation
```css
@media (max-width: 1024px) {
  .col-span-3 { grid-column: span 4; }
}

@media (max-width: 768px) {
  .col-span-3 { grid-column: span 6; }
}

@media (max-width: 640px) {
  .col-span-3 { grid-column: span 12; }
}
```

---

## CARD SYSTEM

### Structure
```jsx
<Card className="card-hover">
  <div className="aspect-video">
    <img className="image-hover" />
  </div>
  <div className="p-4 space-y-3">
    <Badge />
    <h3 className="text-16" />
    <div className="text-12" />
  </div>
</Card>
```

### Specs
- Aspect ratio: 16:9 (aspect-video)
- Padding: 16px (p-4)
- Spacing: 12px (space-y-3)
- Border: 1px at 10% opacity
- Border radius: 8px (rounded-lg)
- Background: surface/80

### Alignment
- All cards snap to grid columns
- Equal internal padding
- Baseline alignment across rows
- No floating elements

---

## SIDEBAR SYSTEM

### Structure
```
Logo:       h-16 (64px)
Separator:  1px
Navigation: flex-1
Separator:  1px
Footer:     py-4 (16px)
```

### Nav Item
```jsx
<Button
  variant="ghost"
  className="h-10 px-3 gap-3 text-14"
>
  <Icon className="h-4 w-4" />
  <span>Label</span>
</Button>
```

**Specs:**
- Height: 40px (h-10)
- Padding: 12px horizontal
- Gap: 12px (icon to text)
- Font: 14px
- Icon: 16px

### Active State
```css
.accent-bar::before {
  width: 2px;
  background: hsl(var(--accent));
}
```

**Visual:**
- 2px left accent line
- Surface background
- Foreground text
- No heavy highlight

---

## HEADER SYSTEM

### Structure
```jsx
<header className="h-16 border-b">
  <div className="max-w-7xl mx-auto px-6">
    <div className="flex items-center justify-between">
      <h1 className="text-24">Title</h1>
      <div className="flex items-center gap-4">
        <Button />
        <Avatar />
      </div>
    </div>
  </div>
</header>
```

### Specs
- Height: 64px (h-16)
- Padding: 24px horizontal
- Border: 1px bottom
- Background: background/95 with blur
- Sticky position
- Aligned to grid

---

## INTERACTION TIMING

### Easing Function
```css
cubic-bezier(0.16, 1, 0.3, 1)
```

**Premium easing:**
- Smooth acceleration
- Natural deceleration
- Feels engineered
- Used by Notion, Linear, Uber

### Duration
```
160ms - Quick feedback
180ms - Standard interactions
200ms - Image transforms
```

### Implementation
```jsx
className="transition-all duration-180 ease-premium"
```

---

## LAYOUT DISCIPLINE

### Container
```jsx
<div className="mx-auto max-w-7xl px-6">
  {/* Content */}
</div>
```

**Specs:**
- Max width: 1280px (max-w-7xl)
- Padding: 24px horizontal
- Centered with auto margins

### Grid Container
```jsx
<div className="grid-container">
  {/* 12-column grid */}
</div>
```

**Specs:**
- 12 columns
- 24px gutter
- Max width: 1280px
- Padding: 24px

### Sidebar Width
```
256px (w-64)
```

**Grid math:**
- Respects 4px base
- Aligns with spacing scale
- Fixed position

---

## COMPONENT SPECS

### Button
```jsx
<Button variant="ghost" size="default">
  Label
</Button>
```

**Sizes:**
- sm: h-8, px-3, text-12
- default: h-9, px-4, text-14
- lg: h-10, px-5, text-14
- icon: h-9, w-9

**Variants:**
- default: Surface bg, border
- ghost: Transparent, hover surface
- link: Text only

### Badge
```jsx
<Badge variant="default">Label</Badge>
```

**Specs:**
- Text: 12px uppercase
- Padding: px-2 py-1
- Border: 1px
- Radius: 6px

### Avatar
```jsx
<Avatar>
  <AvatarFallback>VG</AvatarFallback>
</Avatar>
```

**Specs:**
- Size: 28px (h-7 w-7)
- Radius: 6px
- Background: surface
- Text: 12px

---

## QUALITY STANDARDS

### Structural
- [x] Functional 12-column grid
- [x] Visual grid aligns with layout
- [x] Cards snap to column spans
- [x] Responsive column logic
- [x] Consistent gutter spacing
- [x] No floating elements

### Typography
- [x] Consistent scale (12/14/16/18/24/32)
- [x] Proper hierarchy
- [x] Monospace everywhere
- [x] Tight tracking for headings
- [x] Readable sizes

### Interactions
- [x] Premium hover effects
- [x] Subtle elevation (-2px)
- [x] Background shifts (2%)
- [x] Border opacity increase
- [x] 180ms cubic-bezier easing
- [x] Icon opacity transitions
- [x] Image scale (1.015)

### Spacing
- [x] Consistent scale (4/8/12/16/24/32)
- [x] Equal card padding
- [x] Aligned baselines
- [x] Vertical rhythm
- [x] No arbitrary values

### System
- [x] Grid-driven layout
- [x] Resolution-aware
- [x] Scalable to complex UIs
- [x] Production-ready
- [x] Engineered, not styled

---

## TARGET AESTHETIC

**Feels like:**
- Notion (structure)
- Linear (interactions)
- Supabase (technical)
- Vercel (minimal)
- Uber (premium easing)
- Cred (subtle elevation)

**Feels:**
- Engineered
- System-driven
- Grid-intelligent
- Interaction-aware
- Premium
- Calm
- Intentional
- Series B quality

**Does NOT feel:**
- Styled
- Cosmetic
- Template
- Dribbble
- Consumer
- Flashy

---

## SCALABILITY

This system scales to:
- Dashboards
- Analytics
- Tables
- Complex layouts
- Multi-column content
- Nested grids
- Responsive designs

Built for long-term product evolution.

---

This is a structural system, not a visual theme.
Every decision is functional.
Every element serves the grid.
Every interaction is intentional.
