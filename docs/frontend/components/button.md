# Button Component Documentation

## Overview

The Button component is a versatile, animated button with multiple variants, sizes, and states. Built with Framer Motion for smooth interactions.

**Location:** `src/components/Button/Button.jsx`

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `node` | - | Button content (text, icons, etc.) |
| `variant` | `string` | `'primary'` | Visual style variant |
| `size` | `string` | `'md'` | Button size |
| `fullWidth` | `boolean` | `false` | Whether button spans full container width |
| `disabled` | `boolean` | `false` | Disables button interaction |
| `loading` | `boolean` | `false` | Shows loading spinner |
| `leftIcon` | `node` | - | Icon to display on left side |
| `rightIcon` | `node` | - | Icon to display on right side |
| `onClick` | `function` | - | Click handler |
| `type` | `string` | `'button'` | HTML button type |
| `className` | `string` | `''` | Additional CSS classes |

## Variants

### Primary
Default button style with prominent appearance.

```jsx
<Button variant="primary">
  Click Me
</Button>
```

**Styling:**
- Background: White
- Text: Black
- Hover: Slight scale up (1.02x)
- Active: Slight scale down (0.98x)

### Secondary
Less prominent, outlined style.

```jsx
<Button variant="secondary">
  Cancel
</Button>
```

**Styling:**
- Background: Transparent
- Border: White with low opacity
- Text: White
- Hover: Border brightens

### Ghost
Minimal style with no background or border.

```jsx
<Button variant="ghost">
  Learn More
</Button>
```

**Styling:**
- Background: Transparent
- No border
- Text: Muted foreground
- Hover: Background appears

### Danger
For destructive actions.

```jsx
<Button variant="danger">
  Delete
</Button>
```

**Styling:**
- Background: Red
- Text: White
- Hover: Darker red

## Sizes

### Small (`sm`)
Compact button for tight spaces.

```jsx
<Button size="sm">Small</Button>
```

**Dimensions:**
- Padding: 8px 16px
- Font size: 12px
- Height: 32px

### Medium (`md`)
Default size for most use cases.

```jsx
<Button size="md">Medium</Button>
```

**Dimensions:**
- Padding: 12px 24px
- Font size: 14px
- Height: 40px

### Large (`lg`)
Prominent button for primary actions.

```jsx
<Button size="lg">Large</Button>
```

**Dimensions:**
- Padding: 16px 32px
- Font size: 16px
- Height: 48px

## States

### Disabled
Button is non-interactive and visually muted.

```jsx
<Button disabled>
  Disabled Button
</Button>
```

**Behavior:**
- No hover effects
- Cursor: not-allowed
- Opacity: 0.5
- onClick not triggered

### Loading
Shows spinner and disables interaction.

```jsx
<Button loading>
  Processing...
</Button>
```

**Behavior:**
- Spinner replaces icons
- Button text remains visible
- Disabled state applied
- onClick not triggered

## Icons

### Left Icon
Icon displayed before button text.

```jsx
import { Plus } from 'lucide-react';

<Button leftIcon={<Plus size={16} />}>
  Add Item
</Button>
```

### Right Icon
Icon displayed after button text.

```jsx
import { ArrowRight } from 'lucide-react';

<Button rightIcon={<ArrowRight size={16} />}>
  Continue
</Button>
```

### Both Icons
Icons on both sides.

```jsx
import { Download, ExternalLink } from 'lucide-react';

<Button 
  leftIcon={<Download size={16} />}
  rightIcon={<ExternalLink size={16} />}
>
  Export
</Button>
```

## Full Width

Button spans entire container width.

```jsx
<Button fullWidth>
  Full Width Button
</Button>
```

## Usage Examples

### Basic Button

```jsx
import Button from '@/components/Button';

function MyComponent() {
  const handleClick = () => {
    console.log('Button clicked!');
  };

  return (
    <Button onClick={handleClick}>
      Click Me
    </Button>
  );
}
```

### Form Submit Button

```jsx
import Button from '@/components/Button';
import { Send } from 'lucide-react';

function ContactForm() {
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await submitForm();
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <Button 
        type="submit" 
        loading={loading}
        rightIcon={<Send size={16} />}
        fullWidth
      >
        Send Message
      </Button>
    </form>
  );
}
```

### Button Group

```jsx
import Button from '@/components/Button';

function ActionButtons() {
  return (
    <div className="flex gap-3">
      <Button variant="secondary">
        Cancel
      </Button>
      <Button variant="primary">
        Save Changes
      </Button>
    </div>
  );
}
```

### Conditional Disabled State

```jsx
import Button from '@/components/Button';

function SaveButton({ hasChanges, isSaving }) {
  return (
    <Button 
      disabled={!hasChanges || isSaving}
      loading={isSaving}
      onClick={handleSave}
    >
      {isSaving ? 'Saving...' : 'Save'}
    </Button>
  );
}
```

## Animations

The Button component uses Framer Motion for smooth interactions:

### Hover Animation
```javascript
whileHover={{ scale: 1.02 }}
```
- Scales button to 102% on hover
- Smooth transition (default 0.2s)
- Only active when not disabled or loading

### Tap Animation
```javascript
whileTap={{ scale: 0.98 }}
```
- Scales button to 98% on click
- Provides tactile feedback
- Only active when not disabled or loading

### Loading Spinner
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

## Styling

### CSS Classes

The component generates classes based on props:

```javascript
// Example: Primary medium button
"btn btn-primary btn-md"

// Example: Secondary small full-width button
"btn btn-secondary btn-sm btn-full"

// Example: Disabled loading button
"btn btn-primary btn-md btn-disabled btn-loading"
```

### Custom Styling

Add custom classes via `className` prop:

```jsx
<Button className="my-custom-class">
  Custom Button
</Button>
```

### CSS Variables

Override default styles using CSS variables:

```css
.btn {
  --btn-primary-bg: white;
  --btn-primary-text: black;
  --btn-secondary-border: rgba(255, 255, 255, 0.2);
  --btn-transition: 180ms ease-out;
}
```

## Accessibility

### Keyboard Navigation
- Focusable via Tab key
- Activated via Enter or Space
- Focus indicator visible

### Screen Readers
- Button role automatically applied
- Disabled state announced
- Loading state should include aria-label

**Recommended:**
```jsx
<Button 
  loading={isLoading}
  aria-label={isLoading ? 'Loading, please wait' : 'Submit form'}
>
  Submit
</Button>
```

### Color Contrast
- All variants meet WCAG AA standards
- Disabled state maintains readable contrast
- Focus indicators are clearly visible

## Testing

### Unit Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

test('calls onClick when clicked', () => {
  const handleClick = vi.fn();
  render(<Button onClick={handleClick}>Click Me</Button>);
  
  fireEvent.click(screen.getByText('Click Me'));
  expect(handleClick).toHaveBeenCalledTimes(1);
});

test('does not call onClick when disabled', () => {
  const handleClick = vi.fn();
  render(<Button onClick={handleClick} disabled>Click Me</Button>);
  
  fireEvent.click(screen.getByText('Click Me'));
  expect(handleClick).not.toHaveBeenCalled();
});

test('shows loading spinner when loading', () => {
  render(<Button loading>Loading</Button>);
  expect(screen.getByText('Loading')).toBeInTheDocument();
  expect(document.querySelector('.spinner')).toBeInTheDocument();
});
```

## Performance

- Framer Motion animations are GPU-accelerated
- Component is lightweight (~2KB gzipped)
- No unnecessary re-renders
- Memoize onClick handlers in parent components

## Best Practices

### Do's ✅
- Use semantic button types (`submit`, `button`, `reset`)
- Provide loading states for async actions
- Use appropriate variants for visual hierarchy
- Include icons for better UX
- Disable buttons during processing

### Don'ts ❌
- Don't use buttons for navigation (use Link instead)
- Don't nest interactive elements inside buttons
- Don't use vague labels like "Click Here"
- Don't forget to handle loading states
- Don't use too many primary buttons on one screen

## Related Components

- [Link Button](./link-button.md) - For navigation
- [Icon Button](./icon-button.md) - Icon-only buttons
- [Button Group](./button-group.md) - Multiple buttons together

## Related Documentation

- [Design System](../DESIGN_SYSTEM.md)
- [Animation Guidelines](../ANIMATION_GUIDELINES.md)
- [Accessibility Guide](../ACCESSIBILITY.md)
