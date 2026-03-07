# Premium Design System - Senior UX Refinement

## Philosophy
This is a production-ready, system-driven interface for technical founders. Every decision is intentional. No visual noise. No Dribbble aesthetics. Pure function.

---

## TRUE BLACK FOUNDATION

### Background Layers
```css
--background: #000000           /* Pure black - No tint */
--surface: #0A0A0A             /* Barely lifted - 4% */
--surface-elevated: #111111     /* Elevated - 7% */
```

**Critical:**
- No bluish tint
- No gray wash
- No color cast
- Monochrome only

### Why True Black?
- Reduces eye strain in dark environments
- Creates maximum contrast for text
- Feels technical and focused
- Matches Notion's dark mode philosophy
- Premium developer tool aesthetic

---

## SUBTLE GRID SYSTEM

### Layout Grid Overlay
```css
background-image: 
  linear-gradient(to right, rgba(255,255,255,0.02) 1px, transparent 1px),
  linear-gradient(to bottom, rgba(255,255,255,0.02) 1px, transparent 1px);
background-size: 80px 80px;
```

**Purpose:**
- Reinforces structure (not decorative)
- Creates visual rhythm
- Guides eye movement
- Ensures alignment

### 12-Column Grid
- Max width: 1280px (max-w-7xl)
- Gutter: 24px (gap-6)
- Columns: 12
- Everything snaps to grid

**Implementation:**
```jsx
<div className="mx-auto max-w-7xl px-6">
  {/* Content aligned to 12-column grid */}
</div>
```

---

## TYPOGRAPHY SYSTEM

### Font Stack
```css
font-family: 'IBM Plex Mono', 'JetBrains Mono', monospace;
```

### Scale (Monospace Only)
```
9px  - text-[9px]   - Metadata, tiny labels
10px - text-[10px]  - Badges, secondary
11px - text-[11px]  - Body, buttons, nav
12px - text-xs      - Headings
```

### Letter Spacing
```css
tracking-tighter: -0.02em  /* Headings */
tracking-tight: -0.011em   /* Body */
```

### Weight Hierarchy
```
300 - Light (unused)
400 - Normal (body text)
500 - Medium (headings)
600 - Semibold (unused - too heavy)
```

**Rules:**
- Never use bold (600+)
- Use size + spacing for hierarchy
- Tight tracking for technical feel
- Monospace everywhere

---

## SPACING SCALE

### Consistent Scale (4px base)
```
4px  - gap-1    - Tight spacing
8px  - gap-2    - Default spacing
12px - gap-3    - Medium spacing
16px - gap-4    - Large spacing
24px - gap-6    - Section spacing
32px - gap-8    - Major spacing
48px - gap-12   - Extra large
64px - gap-16   - Section breaks
```

### Padding Standards
```
Cards:    p-3 (12px)
Buttons:  px-2 py-2 (8px)
Sidebar:  px-2 (8px horizontal)
Header:   px-6 (24px)
Content:  px-6 py-8 (24px/32px)
```

**Critical:**
- No inconsistent padding
- Everything aligns to 4px grid
- Breathing room between elements
- Vertical rhythm maintained

---

## SIDEBAR REFINEMENT

### Structure
```
Logo:       h-14 (56px)
Separator:  1px
Navigation: flex-1
Separator:  1px
Footer:     py-3 (12px)
```

### Nav Item Specs
```jsx
<Button
  variant="ghost"
  className="h-8 px-2 gap-3 text-[11px]"
>
  <Icon className="h-[14px] w-[14px]" strokeWidth={1.5} />
  <span>Label</span>
</Button>
```

**Spacing:**
- Height: 32px (h-8)
- Padding: 8px horizontal
- Gap: 12px (icon to text)
- Margin: 4px between items

### Active State
```css
.accent-bar::before {
  width: 2px;
  background: hsl(var(--accent));
}
.active-bg {
  background: hsl(var(--surface));
}
```

**Visual:**
- 2px left accent line
- Subtle background tint (surface color)
- No block highlight
- Functional, not decorative

---

## CARD SYSTEM

### Structure
```jsx
<Card className="p-0 bg-surface/50">
  <div className="h-64"> {/* Image */} </div>
  <div className="p-3 space-y-2"> {/* Content */} </div>
</Card>
```

### Specs
- Border: 1px at 8% opacity
- Border radius: 8px (rounded-lg)
- Background: surface/50 (embedded feel)
- Padding: 12px (p-3)
- No shadows

### Image Heights
```
small:  192px (h-48)
medium: 256px (h-64)
large:  320px (h-80)
xlarge: 384px (h-96)
```

### Hover State
```css
hover:border-border-hover
hover:scale-[1.01]
hover:bg-background/[0.02]
```

**Subtle:**
- 1% scale (barely noticeable)
- 2% background overlay
- Border opacity increase
- 200ms transition

---

## HEADER REFINEMENT

### Structure
```jsx
<header className="h-12 border-b border-border">
  <div className="flex items-center justify-between px-6">
    <h1 className="text-[11px]">Feed</h1>
    <div className="flex items-center gap-3">
      <Button variant="ghost" size="icon">
        <Search />
      </Button>
      <Avatar />
    </div>
  </div>
</header>
```

### Specs
- Height: 48px (h-12) - Reduced from 64px
- Padding: 24px horizontal
- Border: 1px bottom
- Background: background/95 with blur
- Sticky position

**Alignment:**
- Title left-aligned
- Actions right-aligned
- Vertically centered
- Snaps to grid

---

## COMPONENT SPECS

### Button
```jsx
<Button variant="ghost" size="default">
  Label
</Button>
```

**Variants:**
- `default` - Surface bg, border
- `ghost` - Transparent, hover surface
- `link` - Text only

**Sizes:**
- `sm` - h-7, px-2, text-[10px]
- `default` - h-8, px-3, text-[11px]
- `lg` - h-9, px-4
- `icon` - h-8, w-8

### Badge
```jsx
<Badge variant="default">Label</Badge>
```

**Specs:**
- Text: 9px uppercase
- Padding: px-1.5 py-0.5
- Border: 1px
- Radius: 4px
- Tracking: wider

### Avatar
```jsx
<Avatar>
  <AvatarFallback>VG</AvatarFallback>
</Avatar>
```

**Specs:**
- Size: 28px (h-7 w-7)
- Radius: 6px (rounded-md)
- Background: surface
- Text: 10px

---

## INTERACTION PRINCIPLES

### Transitions
```css
duration-150  /* Quick feedback */
duration-200  /* Standard */
```

### Hover States
- Background: +2% opacity
- Border: +4% opacity
- Text: muted → foreground
- Scale: 1.01 (subtle)

### Focus States
```css
focus-visible:ring-1
focus-visible:ring-accent/30
focus-visible:outline-none
```

### Active States
- Accent bar (2px left)
- Surface background
- Foreground text
- No heavy highlight

---

## MASONRY GRID

### Breakpoints
```
Desktop (>1280px):  4 columns
Laptop (1024-1280): 3 columns
Tablet (640-1024):  2 columns
Mobile (<640px):    1 column
```

### Specs
- Column gap: 24px
- Row gap: 24px (margin-bottom)
- Break inside: avoid
- Precise alignment

---

## COLOR USAGE

### Text Hierarchy
```
foreground:        98% - Primary text
muted-foreground:  50% - Secondary text
subtle-foreground: 35% - Tertiary text
```

### Borders
```
border:       8%  - Default
border-hover: 12% - Hover state
grid-line:    6%  - Structural grid
```

### Accent (Use Sparingly)
```
accent:        #5B9DD9 - Active states only
accent-subtle: Darker  - Very subtle hints
```

**Rules:**
- Accent only for active states
- No accent in body text
- No accent in decorative elements
- Functional use only

---

## IMPLEMENTATION CHECKLIST

- [x] TRUE BLACK (#000000) - No tint
- [x] Subtle grid overlay (2% opacity)
- [x] 12-column grid system
- [x] Monospace typography (IBM Plex Mono)
- [x] Consistent spacing (4/8/12/16/24)
- [x] Sidebar vertical rhythm fixed
- [x] Perfect icon/text alignment
- [x] 2px accent bar active state
- [x] Embedded card feeling
- [x] Reduced header height (48px)
- [x] Subtle hover states (2% change)
- [x] No shadows
- [x] No gradients
- [x] No flashy animations
- [x] Production-ready code

---

## DESIGN PRINCIPLES

### Do's
✓ System-driven decisions
✓ Functional over decorative
✓ Subtle over flashy
✓ Aligned to grid
✓ Consistent spacing
✓ Monospace everywhere
✓ True black background
✓ Minimal hover effects

### Don'ts
✗ No color tints
✗ No heavy shadows
✗ No gradients
✗ No glassmorphism
✗ No neon accents
✗ No random spacing
✗ No heavy bold
✗ No visual noise

---

## TARGET AESTHETIC

**Feels like:**
- Notion (dark mode)
- Linear (structure)
- Supabase (technical)
- Vercel (minimal)

**Feels:**
- Expensive
- Intentional
- Calm
- Technical
- Production-ready
- Developer-first

**Does NOT feel like:**
- Template
- Dribbble concept
- Consumer app
- Flashy startup
- Generic dashboard

---

## TECHNICAL IMPLEMENTATION

### File Structure
```
src/
├── components/
│   ├── ui/
│   │   ├── card.jsx       - Embedded cards
│   │   ├── button.jsx     - Subtle buttons
│   │   ├── badge.jsx      - Minimal badges
│   │   ├── separator.jsx  - 1px dividers
│   │   └── avatar.jsx     - Small avatars
│   ├── Sidebar.jsx        - Perfect spacing
│   ├── FeedPage.jsx       - Grid system
│   ├── FeedSection.jsx    - Section layout
│   ├── MediaCard.jsx      - Embedded cards
│   └── SectionHeader.jsx  - Minimal headers
├── App.jsx
└── index.css              - True black theme
```

### Theme Tokens
```css
:root {
  --background: 0 0% 0%;
  --surface: 0 0% 4%;
  --surface-elevated: 0 0% 7%;
  --foreground: 0 0% 98%;
  --muted-foreground: 0 0% 50%;
  --subtle-foreground: 0 0% 35%;
  --border: 0 0% 8%;
  --border-hover: 0 0% 12%;
  --grid-line: 0 0% 6%;
  --accent: 217 50% 55%;
  --radius: 0.5rem;
}
```

---

## QUALITY STANDARDS

This design system represents:
- Senior-level UX thinking
- Production-ready code
- $25M funded quality
- Technical founder audience
- System-driven approach
- Intentional decisions
- No compromises

Every pixel is intentional.
Every spacing value is consistent.
Every interaction is subtle.
Every element serves a purpose.

This is not a template.
This is a system.
