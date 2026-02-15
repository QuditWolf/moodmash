# Setup Guide

## Installation

### 1. Install Dependencies
```bash
npm install
```

This installs:
- React & React DOM
- Vite (build tool)
- Tailwind CSS
- PostCSS & Autoprefixer
- Lucide React (icons)
- Framer Motion (animations)

### 2. Run Development Server
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### 3. Build for Production
```bash
npm run build
```

Output will be in the `dist/` folder.

## File Overview

### Core Files
- `src/App.jsx` - Main app component (Sidebar + Feed layout)
- `src/main.jsx` - React entry point
- `src/index.css` - Tailwind directives + custom styles

### Components
- `Sidebar.jsx` - Left navigation (fixed position)
- `FeedPage.jsx` - Main feed container with sections
- `FeedSection.jsx` - Individual section with masonry grid
- `MediaCard.jsx` - Placeholder card with skeleton UI
- `SectionHeader.jsx` - Section title with count badge

### Configuration
- `tailwind.config.js` - Tailwind configuration with shadcn colors
- `postcss.config.js` - PostCSS configuration
- `vite.config.js` - Vite build configuration

## Key Features

### Masonry Layout
The masonry grid is CSS-based using `column-count`:
- No JavaScript required
- Responsive breakpoints
- Smooth transitions

### Placeholder Cards
Cards use:
- Gradient backgrounds (no images)
- Skeleton loading UI
- Shimmer animation effect
- Variable heights for visual interest

### Responsive Design
- Desktop: 4 columns
- Laptop: 3 columns
- Tablet: 2 columns
- Mobile: 1 column

### Dark Mode
Toggle dark mode by adding `dark` class to `<html>`:
```javascript
document.documentElement.classList.add('dark');
```

## Customization

### Add New Navigation Item
Edit `src/components/Sidebar.jsx`:
```javascript
const navItems = [
  // ... existing items
  { icon: YourIcon, label: 'New Item', active: false },
];
```

### Add New Feed Section
Edit `src/components/FeedPage.jsx`:
```javascript
const sections = [
  // ... existing sections
  { title: 'Your Section', items: generateMockItems('category', 10) },
];
```

### Change Colors
Edit `src/index.css` in the `:root` section:
```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  /* Modify HSL values */
}
```

### Modify Card Heights
Edit `src/components/MediaCard.jsx`:
```javascript
const heightClasses = {
  small: 'h-48',   // Tailwind class
  medium: 'h-64',
  large: 'h-80',
  xlarge: 'h-96',
};
```

## Troubleshooting

### Tailwind styles not working
1. Make sure `tailwind.config.js` exists
2. Check that `src/index.css` has `@tailwind` directives
3. Restart dev server

### Icons not showing
1. Verify `lucide-react` is installed: `npm list lucide-react`
2. Check import statements in components

### Masonry layout broken
1. Check browser support for CSS columns
2. Verify `.masonry-grid` class is applied
3. Check responsive breakpoints in `src/index.css`

## Browser Support

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Mobile browsers: ✅ Full support

CSS columns are widely supported.

## Performance

- Lightweight: No heavy dependencies
- Fast: Vite for instant HMR
- Optimized: Tailwind purges unused CSS
- Smooth: CSS-based animations

## Next Steps

1. Replace placeholder cards with real content
2. Add click handlers to cards
3. Implement routing for navigation
4. Connect to a backend API
5. Add user authentication
6. Implement search and filters
7. Add infinite scroll
8. Create detail views for items

## Resources

- [Tailwind CSS Docs](https://tailwindcss.com/docs)
- [Lucide Icons](https://lucide.dev/)
- [Vite Docs](https://vitejs.dev/)
- [React Docs](https://react.dev/)
- [shadcn/ui](https://ui.shadcn.com/) - Design inspiration

## Support

For issues or questions:
1. Check this guide
2. Review component code
3. Check browser console for errors
4. Verify all dependencies are installed
