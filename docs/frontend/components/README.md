# Frontend Components Documentation

## Overview

This directory contains documentation for all React components in the VibeGraph frontend application. Components are organized by category and documented with props, usage examples, and best practices.

## Component Categories

### Core UI Components

Basic building blocks used throughout the application.

- **[Button](./button.md)** - Versatile button with variants, sizes, and states
- **[Card](./card.md)** - Flexible container with hover effects
- **[Input](./input.md)** - Form input fields with validation
- **[Modal](./modal.md)** - Dialog and modal overlays
- **[Loader](./loader.md)** - Loading indicators and spinners

### Navigation Components

Components for app navigation and routing.

- **[Navbar](./navbar.md)** - Top navigation bar with theme toggle and user actions
- **[Sidebar](./sidebar.md)** - Side navigation panel
- **[MobileNav](./mobile-nav.md)** - Mobile navigation menu
- **[Breadcrumbs](./breadcrumbs.md)** - Breadcrumb navigation

### Onboarding Components

Components for the adaptive quiz and onboarding flow.

- **[OnboardingPage](./onboarding.md#onboardingpage)** - Main onboarding container
- **[QuestionScreen](./onboarding.md#questionscreen)** - Question display and selection
- **[OptionTile](./onboarding.md#optiontile)** - Selectable option tile
- **[ProgressBar](./onboarding.md#progressbar)** - Progress indicator
- **[TasteDNACard](./onboarding.md#tastednacard)** - Taste profile results display

See [Onboarding Components Documentation](./onboarding.md) for complete details.

### Feed Components

Components for content feed and discovery.

- **[FeedCard](./feed-card.md)** - Content card for feed items
- **[FeedSection](./feed-section.md)** - Grouped feed content
- **[MediaCard](./media-card.md)** - Media content display
- **[VideoCard](./video-card.md)** - Video content with playback
- **[CompactCard](./compact-card.md)** - Compact content card

### Form Components

Components for forms and user input.

- **[Input](./input.md)** - Text input fields
- **[FileUpload](./file-upload.md)** - File upload component
- **[Select](./select.md)** - Dropdown select
- **[Checkbox](./checkbox.md)** - Checkbox input
- **[Radio](./radio.md)** - Radio button input

### Utility Components

Helper components for common patterns.

- **[EmptyState](./empty-state.md)** - Empty state displays
- **[RevealOnScroll](./reveal-on-scroll.md)** - Scroll-triggered animations
- **[ProtectedRoute](./protected-route.md)** - Authentication-protected routes
- **[SectionHeader](./section-header.md)** - Section title headers

## Component Structure

Each component follows a consistent structure:

```
ComponentName/
├── ComponentName.jsx      # Component implementation
├── ComponentName.css      # Component styles
├── ComponentName.test.jsx # Unit tests
└── index.js              # Export file
```

## Documentation Format

Each component documentation includes:

1. **Overview** - Brief description and location
2. **Props** - Complete prop table with types and descriptions
3. **Usage Examples** - Code examples for common use cases
4. **Variants/States** - Different visual styles and states
5. **Styling** - CSS classes and customization
6. **Animations** - Framer Motion animations
7. **Accessibility** - Keyboard navigation and screen reader support
8. **Testing** - Unit test examples
9. **Best Practices** - Do's and don'ts
10. **Related Components** - Links to related docs

## Quick Reference

### Most Used Components

```jsx
// Button
import Button from '@/components/Button';
<Button variant="primary" onClick={handleClick}>Click Me</Button>

// Card
import Card from '@/components/Card';
<Card hoverable><h3>Title</h3><p>Content</p></Card>

// Input
import Input from '@/components/Input';
<Input label="Email" type="email" value={email} onChange={setEmail} />

// Modal
import Modal from '@/components/Modal';
<Modal isOpen={isOpen} onClose={handleClose}>Content</Modal>

// Navbar
import Navbar from '@/components/Navbar';
<Navbar />
```

### Component Imports

All components are exported from the main index:

```jsx
// Individual imports
import Button from '@/components/Button';
import Card from '@/components/Card';

// Grouped import
import { Button, Card, Input } from '@/components';
```

## Design Principles

### Consistency
- All components follow the same design system
- Consistent prop naming conventions
- Unified animation patterns

### Accessibility
- Keyboard navigation support
- Screen reader compatibility
- WCAG AA color contrast
- Focus indicators

### Performance
- Lightweight components
- GPU-accelerated animations
- Lazy loading where appropriate
- Memoization for expensive operations

### Flexibility
- Customizable via props
- Extensible via className
- Composable architecture
- Variant system for different styles

## Component Guidelines

### Creating New Components

1. **Plan the API** - Define props and behavior
2. **Build the Component** - Implement with React
3. **Add Styles** - Use Tailwind or CSS modules
4. **Add Animations** - Use Framer Motion
5. **Write Tests** - Unit and integration tests
6. **Document** - Create documentation file
7. **Export** - Add to component index

### Component Checklist

- [ ] Props are well-defined with PropTypes or TypeScript
- [ ] Component is accessible (keyboard, screen reader)
- [ ] Responsive design implemented
- [ ] Animations are smooth and purposeful
- [ ] Error states handled gracefully
- [ ] Loading states implemented
- [ ] Unit tests written
- [ ] Documentation created
- [ ] Storybook story added (if applicable)

## Testing Components

### Unit Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import Button from './Button';

test('renders button with text', () => {
  render(<Button>Click Me</Button>);
  expect(screen.getByText('Click Me')).toBeInTheDocument();
});

test('calls onClick when clicked', () => {
  const handleClick = vi.fn();
  render(<Button onClick={handleClick}>Click</Button>);
  fireEvent.click(screen.getByText('Click'));
  expect(handleClick).toHaveBeenCalled();
});
```

### Integration Tests

```javascript
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Navbar from './Navbar';

test('navbar renders with all elements', () => {
  render(
    <BrowserRouter>
      <Navbar />
    </BrowserRouter>
  );
  
  expect(screen.getByText('VibeGraph')).toBeInTheDocument();
  expect(screen.getByRole('button')).toBeInTheDocument();
});
```

## Styling Approach

### Tailwind CSS

Most components use Tailwind utility classes:

```jsx
<div className="flex items-center gap-4 p-6 bg-surface rounded-lg">
  <h3 className="text-lg font-medium">Title</h3>
</div>
```

### CSS Modules

Complex components use CSS modules:

```jsx
import styles from './Button.module.css';

<button className={styles.button}>Click</button>
```

### Framer Motion

Animations use Framer Motion:

```jsx
import { motion } from 'framer-motion';

<motion.div
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
  Content
</motion.div>
```

## Common Patterns

### Controlled Components

```jsx
function MyForm() {
  const [value, setValue] = useState('');
  
  return (
    <Input 
      value={value} 
      onChange={(e) => setValue(e.target.value)} 
    />
  );
}
```

### Compound Components

```jsx
<Card>
  <Card.Header>
    <Card.Title>Title</Card.Title>
  </Card.Header>
  <Card.Body>
    Content
  </Card.Body>
  <Card.Footer>
    <Button>Action</Button>
  </Card.Footer>
</Card>
```

### Render Props

```jsx
<DataFetcher url="/api/data">
  {({ data, loading, error }) => (
    loading ? <Loader /> : <DataDisplay data={data} />
  )}
</DataFetcher>
```

## Resources

### Internal Documentation
- [Frontend README](../README.md)
- [Design System](../DESIGN_SYSTEM.md)
- [API Services](../services/api.md)
- [State Management](../STATE_MANAGEMENT.md)

### External Resources
- [React Documentation](https://react.dev)
- [Framer Motion](https://www.framer.com/motion/)
- [Tailwind CSS](https://tailwindcss.com)
- [Radix UI](https://www.radix-ui.com)

## Contributing

When adding or updating components:

1. Follow existing patterns and conventions
2. Write comprehensive documentation
3. Add unit tests
4. Ensure accessibility compliance
5. Update this index if adding new categories
6. Submit PR with component and docs

## Support

For questions or issues with components:
- Check component documentation first
- Review design system guidelines
- Ask in #frontend-dev channel
- Create issue with component label
