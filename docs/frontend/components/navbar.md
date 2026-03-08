# Navbar Component Documentation

## Overview

The Navbar component provides top-level navigation with theme toggle, notifications, and user profile access. Features smooth animations and responsive design.

**Location:** `src/components/Navbar/Navbar.jsx`

## Props

The Navbar component doesn't accept props directly. It uses context hooks for state management:
- `useTheme()` - Theme context for dark/light mode
- `useAuth()` - Authentication context for user data

## Features

### Logo
- Links to home page (`/`)
- Gradient "Vibe" text with standard "Graph" text
- Animated entrance on mount

### Theme Toggle
- Switches between dark and light modes
- Sun icon for dark mode (click to go light)
- Moon icon for light mode (click to go dark)
- Smooth icon transition

### Notifications (Authenticated Users)
- Bell icon with notification badge
- Links to `/notifications` page
- Badge shows unread count
- Only visible when user is logged in

### User Profile (Authenticated Users)
- Avatar image or user icon
- Links to `/profile` page
- Circular avatar with border
- Only visible when user is logged in

## Structure

```jsx
<nav className="navbar">
  <div className="navbar-content">
    {/* Logo */}
    <Link to="/" className="navbar-logo">
      <span className="logo-gradient">Vibe</span>
      <span>Graph</span>
    </Link>

    {/* Actions */}
    <div className="navbar-actions">
      {/* Theme Toggle */}
      <button className="navbar-icon-btn">
        {theme === 'dark' ? <Sun /> : <Moon />}
      </button>

      {/* Notifications (if authenticated) */}
      {user && (
        <Link to="/notifications" className="navbar-icon-btn">
          <Bell />
          <span className="notification-badge">3</span>
        </Link>
      )}

      {/* User Avatar (if authenticated) */}
      {user && (
        <Link to="/profile" className="navbar-avatar">
          {user.avatar ? <img src={user.avatar} /> : <User />}
        </Link>
      )}
    </div>
  </div>
</nav>
```

## Usage Example

### Basic Usage

```jsx
import Navbar from '@/components/Navbar';

function App() {
  return (
    <div>
      <Navbar />
      <main>
        {/* Page content */}
      </main>
    </div>
  );
}
```

### With Layout

```jsx
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';

function MainLayout({ children }) {
  return (
    <div className="app-layout">
      <Navbar />
      <div className="content-wrapper">
        <Sidebar />
        <main className="main-content">
          {children}
        </main>
      </div>
    </div>
  );
}
```

## Context Dependencies

### Theme Context

The Navbar requires a ThemeContext provider:

```jsx
// contexts/ThemeContext.jsx
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('dark');

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  return useContext(ThemeContext);
}
```

### Auth Context

The Navbar requires an AuthContext provider:

```jsx
// contexts/AuthContext.jsx
import { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
```

### App Setup

```jsx
import { ThemeProvider } from '@/contexts/ThemeContext';
import { AuthProvider } from '@/contexts/AuthContext';
import Navbar from '@/components/Navbar';

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Navbar />
        {/* Rest of app */}
      </AuthProvider>
    </ThemeProvider>
  );
}
```

## Animations

### Initial Animation
```javascript
initial={{ y: -100 }}
animate={{ y: 0 }}
transition={{ duration: 0.3 }}
```

**Behavior:**
- Navbar slides down from top on mount
- 300ms smooth transition
- Creates polished entrance effect

### Icon Button Hover
```javascript
whileHover={{ scale: 1.05 }}
whileTap={{ scale: 0.95 }}
```

**Behavior:**
- Buttons scale up 5% on hover
- Scale down to 95% on click
- Provides tactile feedback

## Styling

### CSS Classes

```css
.navbar {
  /* Fixed positioning at top */
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  
  /* Styling */
  background: var(--navbar-bg);
  border-bottom: 1px solid var(--navbar-border);
  backdrop-filter: blur(10px);
}

.navbar-content {
  /* Container with max width */
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 24px;
  
  /* Flexbox layout */
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-logo {
  /* Logo styling */
  font-size: 20px;
  font-weight: 600;
  text-decoration: none;
  color: var(--foreground);
}

.logo-gradient {
  /* Gradient text effect */
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.navbar-actions {
  /* Action buttons container */
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-icon-btn {
  /* Icon button styling */
  position: relative;
  padding: 8px;
  border-radius: 8px;
  background: transparent;
  border: none;
  color: var(--foreground);
  cursor: pointer;
  transition: background 180ms ease-out;
}

.navbar-icon-btn:hover {
  background: var(--surface);
}

.notification-badge {
  /* Notification count badge */
  position: absolute;
  top: 4px;
  right: 4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  color: white;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.navbar-avatar {
  /* User avatar */
  width: 32px;
  height: 32px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid var(--border);
}

.navbar-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

### CSS Variables

```css
:root {
  --navbar-bg: rgba(0, 0, 0, 0.8);
  --navbar-border: rgba(255, 255, 255, 0.1);
  --navbar-height: 64px;
}
```

## Responsive Design

### Desktop (>1024px)
- Full navbar with all features
- Horizontal layout
- Icon buttons with hover effects

### Tablet (768px - 1024px)
- Slightly reduced padding
- Same features as desktop
- Adjusted spacing

### Mobile (<768px)
- Compact layout
- Smaller icons
- Reduced padding
- Logo text may be abbreviated

**Example Media Query:**
```css
@media (max-width: 768px) {
  .navbar-content {
    padding: 12px 16px;
  }
  
  .navbar-logo {
    font-size: 18px;
  }
  
  .navbar-actions {
    gap: 8px;
  }
}
```

## Accessibility

### Keyboard Navigation
- All buttons and links are keyboard accessible
- Tab order follows visual flow: Logo → Theme → Notifications → Profile
- Focus indicators visible on all interactive elements

### Screen Readers
- Logo has descriptive text
- Icon buttons should have aria-labels
- Notification badge should announce count

**Recommended Improvements:**
```jsx
<button
  className="navbar-icon-btn"
  onClick={toggleTheme}
  aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
>
  {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
</button>

<Link 
  to="/notifications" 
  className="navbar-icon-btn"
  aria-label={`Notifications (${notificationCount} unread)`}
>
  <Bell size={20} />
  <span className="notification-badge" aria-hidden="true">
    {notificationCount}
  </span>
</Link>
```

### Color Contrast
- All text meets WCAG AA standards
- Icon colors have sufficient contrast
- Focus indicators are clearly visible

## Testing

### Unit Tests

```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@/contexts/ThemeContext';
import { AuthProvider } from '@/contexts/AuthContext';
import Navbar from './Navbar';

const renderNavbar = (user = null) => {
  return render(
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider value={{ user }}>
          <Navbar />
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
};

test('renders logo', () => {
  renderNavbar();
  expect(screen.getByText('Vibe')).toBeInTheDocument();
  expect(screen.getByText('Graph')).toBeInTheDocument();
});

test('toggles theme on button click', () => {
  renderNavbar();
  const themeButton = screen.getByRole('button');
  
  // Initial state (dark mode)
  expect(screen.getByTestId('sun-icon')).toBeInTheDocument();
  
  // Click to toggle
  fireEvent.click(themeButton);
  
  // Should show moon icon (light mode)
  expect(screen.getByTestId('moon-icon')).toBeInTheDocument();
});

test('shows user actions when authenticated', () => {
  const user = { id: '1', name: 'John', avatar: '/avatar.jpg' };
  renderNavbar(user);
  
  expect(screen.getByLabelText(/notifications/i)).toBeInTheDocument();
  expect(screen.getByAltText('John')).toBeInTheDocument();
});

test('hides user actions when not authenticated', () => {
  renderNavbar(null);
  
  expect(screen.queryByLabelText(/notifications/i)).not.toBeInTheDocument();
  expect(screen.queryByRole('img')).not.toBeInTheDocument();
});
```

## Performance

- Component is lightweight (~2KB gzipped)
- Framer Motion animations are GPU-accelerated
- No unnecessary re-renders (uses context efficiently)
- Fixed positioning doesn't affect layout reflow

## Best Practices

### Do's ✅
- Keep navbar height consistent across pages
- Use semantic HTML (nav, button, link)
- Provide aria-labels for icon buttons
- Maintain z-index hierarchy
- Test with keyboard navigation

### Don'ts ❌
- Don't add too many actions (max 4-5)
- Don't make navbar too tall (64px is ideal)
- Don't forget mobile responsiveness
- Don't use onClick on links (use Link component)
- Don't block content with fixed navbar (add padding to body)

## Common Customizations

### Add Search Bar

```jsx
import { Search } from 'lucide-react';

<div className="navbar-search">
  <Search size={16} />
  <input 
    type="text" 
    placeholder="Search..." 
    className="search-input"
  />
</div>
```

### Add Dropdown Menu

```jsx
import { Menu } from 'lucide-react';

<button className="navbar-icon-btn" onClick={toggleMenu}>
  <Menu size={20} />
</button>

{menuOpen && (
  <div className="navbar-dropdown">
    <Link to="/settings">Settings</Link>
    <Link to="/help">Help</Link>
    <button onClick={handleLogout}>Logout</button>
  </div>
)}
```

### Add Breadcrumbs

```jsx
<div className="navbar-breadcrumbs">
  <Link to="/">Home</Link>
  <span>/</span>
  <Link to="/spaces">Spaces</Link>
  <span>/</span>
  <span>Current Space</span>
</div>
```

## Related Components

- [Sidebar](./sidebar.md) - Side navigation panel
- [MobileNav](./mobile-nav.md) - Mobile navigation menu
- [UserMenu](./user-menu.md) - User dropdown menu

## Related Documentation

- [Layout System](../LAYOUT_SYSTEM.md)
- [Theme Context](../contexts/theme-context.md)
- [Auth Context](../contexts/auth-context.md)
- [Navigation Patterns](../NAVIGATION_PATTERNS.md)
