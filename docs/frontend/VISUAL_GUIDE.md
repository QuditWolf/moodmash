# Visual Design Guide

## Layout Overview

```
┌─────────────────────────────────────────────────────────────┐
│  ┌──────────┐  ┌──────────────────────────────────────────┐ │
│  │          │  │  Your Feed                               │ │
│  │ VibeGraph│  │  Discover and explore cultural moments   │ │
│  │          │  └──────────────────────────────────────────┘ │
│  ├──────────┤  ┌──────────────────────────────────────────┐ │
│  │ Feed  ●  │  │  Music                              (12) │ │
│  │ Explore  │  ├──────────────────────────────────────────┤ │
│  │Moodboards│  │  ┌────┐ ┌────┐ ┌────┐ ┌────┐           │ │
│  │ Vibes    │  │  │    │ │    │ │    │ │    │           │ │
│  │ Profile  │  │  │ M  │ │ L  │ │ S  │ │ XL │           │ │
│  │          │  │  │    │ │    │ │    │ │    │           │ │
│  │          │  │  └────┘ └────┘ └────┘ │    │           │ │
│  │          │  │  ┌────┐ ┌────┐ ┌────┐ │    │           │ │
│  │          │  │  │ S  │ │ M  │ │ L  │ └────┘           │ │
│  │          │  │  └────┘ └────┘ │    │ ┌────┐           │ │
│  │          │  │  ┌────┐ ┌────┐ └────┘ │ M  │           │ │
│  │          │  │  │ L  │ │ S  │ ┌────┐ └────┘           │ │
│  │          │  │  │    │ └────┘ │ XL │                  │ │
│  │          │  │  └────┘         │    │                  │ │
│  │          │  │                 └────┘                  │ │
│  │          │  ├──────────────────────────────────────────┤ │
│  │          │  │  Movies                             (10) │ │
│  │          │  ├──────────────────────────────────────────┤ │
│  │          │  │  [Similar masonry grid]                  │ │
│  ├──────────┤  └──────────────────────────────────────────┘ │
│  │ Settings │                                               │
│  └──────────┘                                               │
└─────────────────────────────────────────────────────────────┘
```

## Color Palette

### Light Mode
```
Background:    #FFFFFF (white)
Foreground:    #0A0A0A (near black)
Card:          #FFFFFF (white)
Muted:         #F5F5F5 (light gray)
Border:        #E5E5E5 (gray)
Accent:        #F5F5F5 (light gray)
```

### Dark Mode
```
Background:    #0A0A0A (near black)
Foreground:    #FAFAFA (off white)
Card:          #0A0A0A (near black)
Muted:         #262626 (dark gray)
Border:        #262626 (dark gray)
Accent:        #262626 (dark gray)
```

## Typography Scale

```
Page Title:     32px / 2rem      (font-display)
Section Title:  24px / 1.5rem    (font-display)
Body Large:     16px / 1rem      (font-sans)
Body:           14px / 0.875rem  (font-sans)
Small:          12px / 0.75rem   (font-sans)
```

## Spacing System

```
xs:   4px
sm:   8px
md:   16px
lg:   24px
xl:   32px
2xl:  48px
3xl:  64px
```

## Component Anatomy

### MediaCard
```
┌─────────────────────┐
│                     │
│   [Gradient BG]     │  ← Placeholder image area
│   with shimmer      │     (variable height)
│                     │
├─────────────────────┤
│ [Tag]               │  ← Category badge
│                     │
│ ████████            │  ← Title placeholder
│ ██████              │     (skeleton loading)
│                     │
│ ███ • ████          │  ← Metadata
└─────────────────────┘
```

### Card Heights
```
Small:   192px (h-48)
Medium:  256px (h-64)
Large:   320px (h-80)
XLarge:  384px (h-96)
```

### Sidebar Item
```
┌─────────────────────┐
│ [Icon] Label        │  ← Normal state
└─────────────────────┘

┌─────────────────────┐
│ [Icon] Label        │  ← Hover state
└─────────────────────┘  (background: accent)

┌─────────────────────┐
│ [Icon] Label        │  ← Active state
└─────────────────────┘  (background: secondary)
```

## Masonry Grid Behavior

### Desktop (4 columns)
```
┌──┐ ┌──┐ ┌──┐ ┌──┐
│ 1│ │ 2│ │ 3│ │ 4│
└──┘ │  │ └──┘ │  │
┌──┐ │  │ ┌──┐ │  │
│ 5│ └──┘ │ 6│ └──┘
└──┘ ┌──┐ │  │ ┌──┐
┌──┐ │ 7│ └──┘ │ 8│
│ 9│ └──┘ ┌──┐ └──┘
└──┘      │10│
          └──┘
```

### Tablet (2 columns)
```
┌──┐ ┌──┐
│ 1│ │ 2│
└──┘ │  │
┌──┐ │  │
│ 3│ └──┘
│  │ ┌──┐
└──┘ │ 4│
┌──┐ └──┘
│ 5│ ┌──┐
└──┘ │ 6│
     └──┘
```

### Mobile (1 column)
```
┌──┐
│ 1│
└──┘
┌──┐
│ 2│
│  │
└──┘
┌──┐
│ 3│
└──┘
```

## Hover States

### Card Hover
```
Before:
- Shadow: sm (subtle)
- Border: border color
- Scale: 1

After:
- Shadow: md (elevated)
- Border: foreground/20
- Scale: 1 (no scale)
- Overlay: foreground/5
```

### Button Hover
```
Before:
- Background: transparent
- Text: muted-foreground

After:
- Background: accent
- Text: foreground
- Transition: 150ms
```

## Animations

### Shimmer Effect
```
Duration: 2s
Timing: infinite
Effect: Gradient moves left to right
```

### Pulse Effect
```
Duration: 2s
Timing: infinite
Effect: Opacity 100% → 50% → 100%
```

### Hover Transitions
```
Duration: 200ms
Timing: ease-in-out
Properties: all
```

## Responsive Breakpoints

```
Mobile:     < 640px   (1 column)
Tablet:     640-1024  (2 columns)
Laptop:     1024-1280 (3 columns)
Desktop:    > 1280px  (4 columns)
```

## Accessibility

### Focus States
- 2px outline
- Primary color
- 2px offset
- Visible on keyboard navigation

### Color Contrast
- Text on background: 4.5:1 minimum
- Muted text: 3:1 minimum
- Interactive elements: 3:1 minimum

### Touch Targets
- Minimum: 44x44px
- Sidebar items: 48px height
- Buttons: 40px minimum

## Design Principles

### Minimalism
- Plenty of whitespace
- Neutral colors
- Clean typography
- Subtle shadows

### Consistency
- Uniform spacing
- Consistent borders
- Predictable hover states
- Semantic colors

### Hierarchy
- Clear section titles
- Visual grouping
- Size variation
- Color contrast

### Responsiveness
- Mobile-first approach
- Fluid layouts
- Flexible grids
- Touch-friendly

## Component States

### MediaCard
```
Default:  Normal appearance
Hover:    Elevated shadow, border highlight
Active:   (Not implemented)
Loading:  Shimmer + pulse animations
```

### Navigation Item
```
Default:  Muted text, no background
Hover:    Accent background, foreground text
Active:   Secondary background, foreground text
Focus:    Outline ring
```

## Grid Specifications

### Masonry Grid
```
Column Gap:    24px (1.5rem)
Row Gap:       24px (1.5rem)
Column Width:  Auto (equal)
Item Margin:   0 0 24px 0
```

### Card Padding
```
Image Area:    0 (no padding)
Content Area:  16px (1rem)
```

### Section Spacing
```
Between Sections:  64px (4rem)
Section Header:    24px bottom margin
```

## Icon Specifications

### Sizes
```
Navigation:  20px (1.25rem)
Inline:      16px (1rem)
Large:       24px (1.5rem)
```

### Stroke Width
```
Default:     2px
Thin:        1.5px
Bold:        2.5px
```

## Shadow System

```
sm:  0 1px 2px rgba(0,0,0,0.05)
md:  0 4px 6px rgba(0,0,0,0.1)
lg:  0 10px 15px rgba(0,0,0,0.1)
xl:  0 20px 25px rgba(0,0,0,0.1)
```

## Border Radius

```
sm:  6px   (0.375rem)
md:  8px   (0.5rem)
lg:  12px  (0.75rem)
xl:  16px  (1rem)
full: 9999px
```

## Z-Index Layers

```
Base:       0
Sidebar:    10
Header:     10
Dropdown:   20
Modal:      30
Tooltip:    40
```
