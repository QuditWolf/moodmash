# Premium SaaS Design System

## Overview
Production-ready design system inspired by Linear, Vercel, Supabase, and Notion. Dark mode only, monospace typography, intentional spacing.

---

## Color Palette

### Background Layers
```css
--background: #0B0F14        /* Base background */
--surface: #11161C           /* Elevated surface */
--surface-elevated: #151A21  /* Highest elevation */
```

### Text Colors
```css
--foreground: Near white     /* Primary text */
--muted-foreground: 55%      /* Secondary text */
--subtle-foreground: 40%     /* Tertiary text */
```

### Borders
```css
--border: rgba(255,255,255,0.06)     /* Default border */
--border-hover: rgba(255,255,255,0.1) /* Hover state */
```

### Accent
```css
--accent: #4C9AFF           /* Muted blue */
--accent-muted: Darker blue /* Subtle variant */
```

---

## Typography

### Font Family
- **Primary**: JetBrains Mono (monospace)
- **Weight**: 300 (light), 400 (regular), 500 (medium), 600 (semibold)
- **Letter spacing**: -0.01em (tight)

### Scale
```
text-[10px]  - Metadata, badges
text-xs      - Body text, buttons
text-sm      - Headings, titles
text-base    - Large headings
```

### Hierarchy
- Use size + spacing (not color) for hierarchy
- Restrained weights (avoid heavy bold)
- Slight letter spacing for headings

---

## Spacing Scale

Consistent spacing based on 4px grid:

```
4px   - gap-1
6px   - gap-1.5
8px   - gap-2
12px  - gap-3
16px  - gap-4
24px  - gap-6
32px  - gap-8
48px  - gap-12
64px  - gap-16
96px  - gap-24
```

---

## Layout

### Grid System
- 12-column grid base
- Max width: `max-w-7xl` (1280px)
- Horizontal padding: `px-8` (32px)
- Vertical padding: `py-12` (48px)

### Sidebar
- Width: 256px (w-64)
- Fixed position
- Border right: 1px
- Background: surface

### Content Area
- Margin left: 256px (ml-64)
- Max width: 1280px
- Centered with auto margins

---

## Components

### Card
```jsx
<Card className="p-6">
  <CardHeader>
    <CardTitle>Title</CardTitle>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>
```

**Specs:**
- Border: 1px solid border
- Border radius: 12px (rounded-xl)
- Padding: 24px (p-6)
- Hover: border-hover
- Transition: 200ms

### Button
```jsx
<Button variant="ghost" size="sm">
  Label
</Button>
```

**Variants:**
- `default` - Surface elevated background
- `ghost` - Transparent, hover surface
- `link` - Underline on hover

**Sizes:**
- `sm` - h-8, px-3, text-xs
- `default` - h-9, px-4
- `lg` - h-10, px-8
- `icon` - h-9, w-9

### Badge
```jsx
<Badge variant="default">Label</Badge>
```

**Specs:**
- Text: 10px uppercase
- Padding: px-2 py-0.5
- Border radius: 6px (rounded-md)
- Letter spacing: wider

### Avatar
```jsx
<Avatar>
  <AvatarFallback>VG</AvatarFallback>
</Avatar>
```

**Specs:**
- Size: 32px (h-8 w-8)
- Border radius: 8px (rounded-lg)
- Background: surface-elevated

---

## Interactions

### Transitions
- Duration: 150-200ms
- Easing: Default (ease-in-out)
- Properties: colors, transform, opacity

### Hover States
- Buttons: bg-surface-elevated
- Cards: border-border-hover
- Links: text-foreground

### Focus States
- Ring: 1px accent/50
- Outline: none
- Visible on keyboard navigation

### Active States
- Sidebar: 2px left accent bar
- No background highlight
- Text: foreground color

---

## Masonry Grid

### Breakpoints
```css
Desktop (>1280px):  4 columns
Laptop (1024-1280): 3 columns
Tablet (640-1024):  2 columns
Mobile (<640px):    1 column
```

### Specs
- Column gap: 24px (1.5rem)
- Row gap: 24px (1.5rem)
- Break inside: avoid

---

## Sidebar Navigation

### Structure
```
Logo (h-16)
Separator
Navigation (flex-1)
Separator
Footer
```

### Nav Items
- Button variant: ghost
- Icon: 16px, stroke 1.5
- Text: xs
- Gap: 12px
- Padding: px-3 py-2
- Active: 2px left accent bar

---

## Header

### Structure
```
Height: 64px (h-16)
Border bottom: 1px
Background: background/95 with backdrop blur
Padding: px-8
```

### Layout
- Left: Title
- Right: Search + Avatar
- Sticky position

---

## Feed Cards

### Structure
```
Image (variable height)
Content (p-4)
  - Badge
  - Title (text-xs)
  - Metadata (text-[10px])
```

### Image Heights
```
small:  192px (h-48)
medium: 256px (h-64)
large:  320px (h-80)
xlarge: 384px (h-96)
```

### Hover Effect
- Image: scale-[1.02]
- Overlay: bg-background/5
- Border: border-hover
- Duration: 200ms

---

## Best Practices

### Do's
✓ Use consistent spacing scale
✓ Maintain 12-column grid
✓ Use monospace font everywhere
✓ Keep transitions subtle (150-200ms)
✓ Use semantic color tokens
✓ Constrain content to max-w-7xl
✓ Use shadcn components
✓ Keep borders subtle (0.06 opacity)

### Don'ts
✗ No gradients
✗ No heavy shadows
✗ No glassmorphism
✗ No neon colors
✗ No inconsistent padding
✗ No heavy bold weights
✗ No flashy animations
✗ No bright accent colors

---

## File Structure

```
src/
├── components/
│   ├── ui/
│   │   ├── card.jsx
│   │   ├── button.jsx
│   │   ├── badge.jsx
│   │   ├── separator.jsx
│   │   └── avatar.jsx
│   ├── Sidebar.jsx
│   ├── FeedPage.jsx
│   ├── FeedSection.jsx
│   ├── MediaCard.jsx
│   └── SectionHeader.jsx
├── App.jsx
└── index.css
```

---

## Implementation Checklist

- [x] Dark mode only theme
- [x] Monospace typography (JetBrains Mono)
- [x] Premium color palette
- [x] shadcn/ui components
- [x] Consistent spacing scale
- [x] 12-column grid system
- [x] Max-w-7xl constraint
- [x] Subtle borders (0.06 opacity)
- [x] 150-200ms transitions
- [x] Accent bar active states
- [x] Minimal header
- [x] Premium card design
- [x] Masonry grid layout
- [x] Production-ready code

---

## Inspiration Sources

- **Linear**: Clean sidebar, subtle active states
- **Vercel**: Minimal header, monospace typography
- **Supabase**: Dark theme, muted colors
- **Notion**: Card layouts, spacing

---

This design system creates a production-ready, developer-first SaaS interface that feels intentional and premium.
