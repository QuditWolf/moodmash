# VibeGraph - Minimal Feed UI

A clean, minimal React feed page UI with shadcn-style design system, Tailwind CSS, and masonry layout.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open your browser to `http://localhost:5173`

## 📁 Project Structure

```
src/
├── App.jsx                    # Main app layout
├── index.css                  # Tailwind + custom styles
├── main.jsx                   # Entry point
└── components/
    ├── Sidebar.jsx            # Left navigation sidebar
    ├── FeedPage.jsx           # Main feed container
    ├── FeedSection.jsx        # Section with masonry grid
    ├── SectionHeader.jsx      # Section title + count
    └── MediaCard.jsx          # Placeholder card component

tailwind.config.js             # Tailwind configuration
postcss.config.js              # PostCSS configuration
```

## 🎨 Design System

### Colors (shadcn-style)
- Uses HSL color system with CSS variables
- Full dark mode support
- Neutral, minimal palette
- Semantic color tokens (background, foreground, muted, accent, etc.)

### Typography
- **Display**: Instrument Serif (headings, logo)
- **Body**: Inter (UI text)
- Clean, readable hierarchy

### Layout
- **Sidebar**: Fixed 256px width
- **Feed**: Masonry grid (4 → 3 → 2 → 1 columns responsive)
- **Cards**: Variable heights for Pinterest-like feel

## 🧩 Components

### Sidebar
- Clean minimal navigation
- App logo at top
- Navigation items with icons
- Hover states
- Settings at bottom

### FeedPage
- Sticky header with title
- Multiple sections (Music, Movies, Art, Fashion, Books)
- Generates mock data automatically

### FeedSection
- Section header with title and count
- "View all" button
- Masonry grid layout

### MediaCard
- Placeholder blocks (no real images)
- Variable heights: small, medium, large, xlarge
- Skeleton loading effect
- Shimmer animation
- Tag badges
- Hover effects
- Rounded corners + soft shadows

### SectionHeader
- Section title
- Item count badge
- "View all" link

## 🎯 Features

### Masonry Layout
- CSS column-based masonry
- Responsive breakpoints
- Different card heights for visual interest
- No JavaScript required

### Placeholder Design
- Gradient backgrounds instead of images
- Skeleton text placeholders
- Shimmer loading animation
- Clean, minimal aesthetic

### Responsive
- **Desktop (1280px+)**: 4 columns
- **Laptop (1024px-1280px)**: 3 columns
- **Tablet (640px-1024px)**: 2 columns
- **Mobile (<640px)**: 1 column

### Dark Mode Ready
- Toggle by adding `dark` class to `<html>` element
- All colors adapt automatically
- Smooth transitions

## 🛠️ Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Lucide React** - Icons
- **Framer Motion** - Animations (already installed)

## 📊 Mock Data

Located in `src/components/FeedPage.jsx`:

```javascript
const sections = [
  { title: 'Music', items: 12 },
  { title: 'Movies', items: 10 },
  { title: 'Art', items: 14 },
  { title: 'Fashion', items: 8 },
  { title: 'Books', items: 9 },
];
```

Each item has:
- Random height (small/medium/large/xlarge)
- Category-specific tags
- Placeholder title
- Metadata indicators

## 🎨 Customization

### Change Masonry Columns
Edit `src/index.css`:
```css
.masonry-grid {
  column-count: 4; /* Change to 3 or 5 */
}
```

### Add New Section
Edit `src/components/FeedPage.jsx`:
```javascript
const sections = [
  // ... existing sections
  { title: 'Photography', items: generateMockItems('photography', 10) },
];
```

### Modify Card Heights
Edit `src/components/MediaCard.jsx`:
```javascript
const heightClasses = {
  small: 'h-48',   // 192px
  medium: 'h-64',  // 256px
  large: 'h-80',   // 320px
  xlarge: 'h-96',  // 384px
};
```

### Change Color Scheme
Edit `src/index.css` `:root` variables:
```css
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 3.9%;
  /* ... etc */
}
```

## 🌙 Enable Dark Mode

Add to your HTML or use JavaScript:
```javascript
document.documentElement.classList.add('dark');
```

## 🚫 What's NOT Included

- No backend/API
- No authentication
- No routing (single page)
- No real images
- No user interactions (likes, saves)
- No data fetching

This is a pure UI foundation ready to be extended.

## 📦 Dependencies

```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "lucide-react": "^0.344.0",
  "framer-motion": "^11.0.5"
}
```

```json
{
  "tailwindcss": "latest",
  "postcss": "latest",
  "autoprefixer": "latest"
}
```

## 🎯 Design Inspiration

- **Vercel**: Clean, minimal, premium feel
- **Linear**: Smooth interactions, subtle animations
- **shadcn/ui**: Component design patterns
- **Pinterest**: Masonry layout

## 📝 Next Steps

To extend this UI:

1. **Add real images**: Replace gradient placeholders
2. **Add routing**: React Router for navigation
3. **Add interactions**: Click handlers, likes, saves
4. **Add filtering**: Filter by category/tag
5. **Add search**: Search functionality
6. **Connect backend**: API integration
7. **Add infinite scroll**: Load more items
8. **Add detail views**: Modal or page for each item

## 🤝 Component Reusability

All components are designed to be:
- Self-contained
- Easy to extend
- Prop-driven
- Styled with Tailwind
- No external CSS files needed

## 📱 Mobile Optimized

- Touch-friendly tap targets
- Responsive typography
- Single column on mobile
- Optimized spacing

---

Built with ❤️ using React + Tailwind CSS
