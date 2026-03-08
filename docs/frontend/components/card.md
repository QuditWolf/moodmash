# Card Component Documentation

## Overview

The Card component is a flexible container with multiple variants and optional hover effects. Built with Framer Motion for smooth animations.

**Location:** `src/components/Card/Card.jsx`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `node` | - | Card content |
| `variant` | `string` | `'default'` | Visual style variant |
| `hoverable` | `boolean` | `false` | Enables hover lift animation |
| `className` | `string` | `''` | Additional CSS classes |
| `onClick` | `function` | - | Click handler (makes card clickable) |

## Variants

### Default
Standard card with subtle background and border.

```jsx
<Card variant="default">
  <p>Card content</p>
</Card>
```

**Styling:**
- Background: Semi-transparent surface
- Border: White with low opacity
- Padding: 24px

### Elevated
Card with prominent shadow for emphasis.

```jsx
<Card variant="elevated">
  <p>Important content</p>
</Card>
```

**Styling:**
- Background: Solid surface
- Shadow: Medium elevation
- Border: None

### Outlined
Minimal card with border only.

```jsx
<Card variant="outlined">
  <p>Outlined content</p>
</Card>
```

**Styling:**
- Background: Transparent
- Border: Prominent white border
- Padding: 24px

### Flat
No background or border, just spacing.

```jsx
<Card variant="flat">
  <p>Flat content</p>
</Card>
```

**Styling:**
- Background: None
- Border: None
- Padding: 24px

## Hover Effects

### Hoverable Card
Lifts on hover with shadow enhancement.

```jsx
<Card hoverable>
  <h3>Hover over me</h3>
  <p>I'll lift up!</p>
</Card>
```

**Animation:**
- Translates up 4px on hover
- Shadow increases to XL
- Smooth transition (200ms)

### Clickable Card
Interactive card with tap animation.

```jsx
<Card onClick={() => console.log('Clicked!')}>
  <h3>Click me</h3>
  <p>I'm interactive!</p>
</Card>
```

**Animation:**
- Hover: Lifts up 4px
- Tap: Scales to 98%
- Cursor: pointer

## Usage Examples

### Basic Card

```jsx
import Card from '@/components/Card';

function MyComponent() {
  return (
    <Card>
      <h2>Card Title</h2>
      <p>Card content goes here.</p>
    </Card>
  );
}
```

### Interactive Card

```jsx
import Card from '@/components/Card';
import { useNavigate } from 'react-router-dom';

function ContentCard({ item }) {
  const navigate = useNavigate();

  return (
    <Card 
      hoverable 
      onClick={() => navigate(`/item/${item.id}`)}
    >
      <img src={item.image} alt={item.title} />
      <h3>{item.title}</h3>
      <p>{item.description}</p>
    </Card>
  );
}
```

### Card Grid

```jsx
import Card from '@/components/Card';

function CardGrid({ items }) {
  return (
    <div className="grid grid-cols-3 gap-4">
      {items.map(item => (
        <Card key={item.id} hoverable>
          <h3>{item.title}</h3>
          <p>{item.description}</p>
        </Card>
      ))}
    </div>
  );
}
```

### Card with Header and Footer

```jsx
import Card from '@/components/Card';
import Button from '@/components/Button';

function ProfileCard({ user }) {
  return (
    <Card variant="elevated">
      <div className="card-header">
        <img src={user.avatar} alt={user.name} />
        <h3>{user.name}</h3>
      </div>
      
      <div className="card-body">
        <p>{user.bio}</p>
      </div>
      
      <div className="card-footer">
        <Button variant="secondary" fullWidth>
          View Profile
        </Button>
      </div>
    </Card>
  );
}
```

### Nested Cards

```jsx
import Card from '@/components/Card';

function Dashboard() {
  return (
    <Card variant="elevated">
      <h2>Dashboard</h2>
      
      <div className="grid grid-cols-2 gap-4 mt-4">
        <Card variant="outlined">
          <h3>Stats</h3>
          <p>1,234 views</p>
        </Card>
        
        <Card variant="outlined">
          <h3>Activity</h3>
          <p>42 actions</p>
        </Card>
      </div>
    </Card>
  );
}
```

## Animations

### Hover Animation
```javascript
whileHover={{ 
  y: -4, 
  boxShadow: 'var(--shadow-xl)' 
}}
```

**Behavior:**
- Translates card up by 4px
- Enhances shadow for depth
- Smooth easing function

### Tap Animation
```javascript
whileTap={{ scale: 0.98 }}
```

**Behavior:**
- Scales card to 98% on click
- Provides tactile feedback
- Only active when onClick is provided

## Styling

### CSS Classes

Generated classes based on props:

```javascript
// Default card
"card card-default"

// Hoverable elevated card
"card card-elevated card-hoverable"

// Clickable outlined card
"card card-outlined card-clickable"
```

### Custom Styling

Add custom classes:

```jsx
<Card className="my-custom-card">
  Content
</Card>
```

### CSS Variables

```css
.card {
  --card-bg: rgba(255, 255, 255, 0.05);
  --card-border: rgba(255, 255, 255, 0.1);
  --card-padding: 24px;
  --card-radius: 12px;
  --card-transition: 200ms ease-out;
}
```

## Accessibility

### Keyboard Navigation
- Clickable cards are focusable via Tab
- Activated via Enter or Space
- Focus indicator visible

### Screen Readers
- Use semantic HTML inside cards
- Add aria-label for clickable cards without text
- Ensure heading hierarchy is maintained

**Example:**
```jsx
<Card 
  onClick={handleClick}
  aria-label="View user profile"
>
  <img src={user.avatar} alt="" />
  <h3>{user.name}</h3>
</Card>
```

### Color Contrast
- All variants meet WCAG AA standards
- Text maintains readable contrast
- Interactive states are clearly visible

## Testing

### Unit Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import Card from './Card';

test('renders children', () => {
  render(<Card>Test Content</Card>);
  expect(screen.getByText('Test Content')).toBeInTheDocument();
});

test('calls onClick when clicked', () => {
  const handleClick = vi.fn();
  render(<Card onClick={handleClick}>Click Me</Card>);
  
  fireEvent.click(screen.getByText('Click Me'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

test('applies hoverable class', () => {
  const { container } = render(<Card hoverable>Content</Card>);
  expect(container.firstChild).toHaveClass('card-hoverable');
});
```

## Performance

- Lightweight component (~1KB gzipped)
- Framer Motion animations are GPU-accelerated
- No unnecessary re-renders
- Efficient class name generation

## Best Practices

### Do's ✅
- Use appropriate variants for visual hierarchy
- Enable hoverable for interactive content
- Maintain consistent padding across cards
- Use semantic HTML inside cards
- Group related content in cards

### Don'ts ❌
- Don't nest too many cards (max 2 levels)
- Don't make entire card clickable if only part should be
- Don't use cards for every piece of content
- Don't forget hover states for interactive cards
- Don't use conflicting variants

## Common Patterns

### Content Card
```jsx
<Card hoverable onClick={handleClick}>
  <img src={image} alt={title} />
  <h3>{title}</h3>
  <p>{description}</p>
  <div className="card-meta">
    <span>{author}</span>
    <span>{date}</span>
  </div>
</Card>
```

### Stat Card
```jsx
<Card variant="elevated">
  <div className="stat-value">{value}</div>
  <div className="stat-label">{label}</div>
  <div className="stat-change">{change}</div>
</Card>
```

### Action Card
```jsx
<Card variant="outlined">
  <Icon size={32} />
  <h3>{title}</h3>
  <p>{description}</p>
  <Button variant="ghost">Learn More</Button>
</Card>
```

## Related Components

- [FeedCard](./feed-card.md) - Specialized card for feed items
- [MediaCard](./media-card.md) - Card for media content
- [VideoCard](./video-card.md) - Card for video content

## Related Documentation

- [Design System](../DESIGN_SYSTEM.md)
- [Layout Guidelines](../LAYOUT_GUIDELINES.md)
- [Animation Guidelines](../ANIMATION_GUIDELINES.md)
