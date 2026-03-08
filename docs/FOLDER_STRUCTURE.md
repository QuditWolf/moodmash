# Folder Structure

## Complete Project Structure

```
vibegraph-app/
├── node_modules/              # Dependencies (auto-generated)
├── public/                    # Static assets
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx       # ✨ NEW - Left navigation
│   │   ├── FeedPage.jsx      # ✨ NEW - Main feed container
│   │   ├── FeedSection.jsx   # ✨ NEW - Section with masonry grid
│   │   ├── MediaCard.jsx     # ✨ NEW - Placeholder card
│   │   ├── SectionHeader.jsx # ✨ NEW - Section title component
│   │   └── [old components]  # Previous components (unused)
│   ├── App.jsx               # ✨ UPDATED - Main app layout
│   ├── main.jsx              # ✨ UPDATED - Entry point
│   └── index.css             # ✨ NEW - Tailwind + custom styles
├── index.html                # HTML entry point
├── package.json              # Dependencies
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # ✨ NEW - Tailwind config
├── postcss.config.js         # ✨ NEW - PostCSS config
├── README.md                 # ✨ NEW - Full documentation
├── QUICKSTART.md             # ✨ NEW - Quick start guide
├── SETUP.md                  # ✨ NEW - Setup instructions
├── COMPONENTS.md             # ✨ NEW - Component reference
├── VISUAL_GUIDE.md           # ✨ NEW - Design specs
├── PROJECT_SUMMARY.md        # ✨ NEW - Project overview
└── FOLDER_STRUCTURE.md       # ✨ NEW - This file
```

## Active Files (What You Need)

### Core Application
```
src/
├── App.jsx                    # Main layout (Sidebar + Feed)
├── main.jsx                   # React entry point
├── index.css                  # Tailwind + custom styles
└── components/
    ├── Sidebar.jsx            # Navigation sidebar
    ├── FeedPage.jsx           # Feed container
    ├── FeedSection.jsx        # Section component
    ├── MediaCard.jsx          # Card component
    └── SectionHeader.jsx      # Header component
```

### Configuration
```
tailwind.config.js             # Tailwind setup
postcss.config.js              # PostCSS setup
vite.config.js                 # Vite setup
package.json                   # Dependencies
```

### Documentation
```
README.md                      # Main documentation
QUICKSTART.md                  # Quick start
SETUP.md                       # Setup guide
COMPONENTS.md                  # Component docs
VISUAL_GUIDE.md                # Design specs
PROJECT_SUMMARY.md             # Overview
FOLDER_STRUCTURE.md            # This file
```

## Unused Files (Can Ignore)

These are from the previous implementation and are not used in the new Tailwind version:

```
src/
├── components/
│   ├── Button/               # Old component
│   ├── Card/                 # Old component
│   ├── EmptyState/           # Old component
│   ├── FeedCard/             # Old component (replaced by MediaCard)
│   ├── FileUpload/           # Old component
│   ├── Input/                # Old component
│   ├── Loader/               # Old component
│   ├── Modal/                # Old component
│   ├── Navbar/               # Old component (removed)
│   └── ProtectedRoute.jsx    # Old component (auth removed)
├── contexts/
│   ├── AuthContext.jsx       # Old (auth removed)
│   └── ThemeContext.jsx      # Old (using Tailwind dark mode)
├── layouts/
│   ├── AuthLayout.jsx        # Old (auth removed)
│   └── DashboardLayout.jsx   # Old (simplified)
├── pages/
│   ├── Dashboard.jsx         # Old page
│   ├── DiscoverList.jsx      # Old page
│   ├── Login.jsx             # Old page (auth removed)
│   ├── Signup.jsx            # Old page (auth removed)
│   ├── Profile.jsx           # Old page
│   ├── Notifications.jsx     # Old page
│   ├── NotFound.jsx          # Old page
│   └── Feed.jsx              # Old (replaced by FeedPage component)
├── services/
│   └── api.js                # Old (no backend)
├── styles/
│   └── index.css             # Old (replaced by src/index.css)
└── utils/
    └── helpers.js            # Old utilities
```

## Component Hierarchy

```
App
├── Sidebar
│   ├── Logo
│   ├── Navigation Items
│   │   ├── Feed (active)
│   │   ├── Explore
│   │   ├── Moodboards
│   │   ├── Vibes
│   │   └── Profile
│   └── Settings
└── FeedPage
    ├── Header (sticky)
    └── Sections (multiple)
        ├── Music Section
        │   ├── SectionHeader
        │   └── MediaCard (12x)
        ├── Movies Section
        │   ├── SectionHeader
        │   └── MediaCard (10x)
        ├── Art Section
        │   ├── SectionHeader
        │   └── MediaCard (14x)
        ├── Fashion Section
        │   ├── SectionHeader
        │   └── MediaCard (8x)
        └── Books Section
            ├── SectionHeader
            └── MediaCard (9x)
```

## File Sizes (Approximate)

```
src/App.jsx                    ~300 bytes
src/main.jsx                   ~200 bytes
src/index.css                  ~2 KB
src/components/Sidebar.jsx     ~2 KB
src/components/FeedPage.jsx    ~2.5 KB
src/components/FeedSection.jsx ~600 bytes
src/components/MediaCard.jsx   ~1.5 KB
src/components/SectionHeader.jsx ~400 bytes
```

Total active code: ~10 KB (very lightweight!)

## Dependencies Size

```
node_modules/                  ~150 MB (typical)
├── react                      ~300 KB
├── react-dom                  ~1 MB
├── tailwindcss                ~3 MB
├── lucide-react               ~2 MB
├── framer-motion              ~500 KB
└── [other dependencies]
```

## Build Output

After running `npm run build`:

```
dist/
├── assets/
│   ├── index-[hash].js        # Bundled JavaScript
│   └── index-[hash].css       # Bundled CSS
└── index.html                 # HTML entry
```

Typical sizes:
- JavaScript: ~150 KB (minified + gzipped)
- CSS: ~10 KB (purged + minified)
- Total: ~160 KB

## Git Structure

```
.git/                          # Git repository
.gitignore                     # Git ignore rules
```

Ignored files (in .gitignore):
- node_modules/
- dist/
- .env
- *.log

## Development Files

```
.vscode/                       # VS Code settings (optional)
.eslintrc.js                   # ESLint config (optional)
.prettierrc                    # Prettier config (optional)
```

## Environment Files

```
.env.example                   # Example environment variables
.env                           # Actual environment variables (gitignored)
```

## Documentation Files

All documentation is in Markdown format:

```
README.md                      # 📘 Main documentation (start here)
QUICKSTART.md                  # ⚡ Quick start (2 minutes)
SETUP.md                       # 🔧 Detailed setup
COMPONENTS.md                  # 🧩 Component reference
VISUAL_GUIDE.md                # 🎨 Design specifications
PROJECT_SUMMARY.md             # 📊 Project overview
FOLDER_STRUCTURE.md            # 📁 This file
```

## Import Paths

All imports use relative paths:

```javascript
// In App.jsx
import Sidebar from './components/Sidebar';
import FeedPage from './components/FeedPage';

// In FeedSection.jsx
import SectionHeader from './SectionHeader';
import MediaCard from './MediaCard';

// In FeedPage.jsx
import FeedSection from './FeedSection';
```

No path aliases configured (keeping it simple).

## CSS Structure

```
src/index.css
├── @import (Google Fonts)
├── @tailwind base
├── @tailwind components
├── @tailwind utilities
├── @layer base (CSS variables)
│   ├── :root (light mode)
│   └── .dark (dark mode)
└── @layer utilities (custom utilities)
    └── .masonry-grid (masonry layout)
```

## Configuration Files

### tailwind.config.js
- Content paths
- Theme extensions
- Color system
- Font families

### postcss.config.js
- Tailwind plugin
- Autoprefixer plugin

### vite.config.js
- React plugin
- Build settings
- Dev server settings

### package.json
- Dependencies
- Scripts (dev, build, preview)
- Project metadata

## Scripts

```json
{
  "dev": "vite",              // Start dev server
  "build": "vite build",      // Build for production
  "preview": "vite preview",  // Preview production build
  "lint": "eslint ..."        // Lint code
}
```

## Clean Project Structure

For a fresh start, you only need:

```
vibegraph-app/
├── src/
│   ├── components/
│   │   ├── Sidebar.jsx
│   │   ├── FeedPage.jsx
│   │   ├── FeedSection.jsx
│   │   ├── MediaCard.jsx
│   │   └── SectionHeader.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

Everything else is optional or auto-generated.

## Recommended VS Code Extensions

```
- Tailwind CSS IntelliSense
- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- ESLint
```

## File Naming Conventions

- **Components**: PascalCase (e.g., `MediaCard.jsx`)
- **Utilities**: camelCase (e.g., `helpers.js`)
- **Styles**: kebab-case (e.g., `index.css`)
- **Config**: kebab-case (e.g., `tailwind.config.js`)
- **Docs**: UPPERCASE (e.g., `README.md`)

## Import Order Convention

```javascript
// 1. External dependencies
import React from 'react';
import { motion } from 'framer-motion';

// 2. Internal components
import Sidebar from './components/Sidebar';
import FeedPage from './components/FeedPage';

// 3. Styles
import './index.css';
```

---

This structure keeps the project clean, organized, and easy to navigate! 🎯
